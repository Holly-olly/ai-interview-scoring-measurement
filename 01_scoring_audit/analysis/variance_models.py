"""Variance models of the scoring audit: reliability and answer length for each scoring method.

Per method (human, TEAS, zero-shot) and scale, two Bayesian mixed models (bambi, Gaussian) on the score standardized
within method and scale, abstentions dropped:
  m0  y ~ 1 + (1|person_id) + (1|question_id)                  person x question G-study
  m1  y ~ 1 + log_tokens_z + (1|person_id) + (1|question_id)   with answer length
From m0: person share = person / (person + question + residual); E-rho2(6) = person / (person + residual / 6);
Phi(6) = person / (person + (question + residual) / 6); answers per person for Phi = .70. From m1: change in person
variance and the length slope. Posterior means with 95% intervals. Input: a CSV with one row per answer and the
columns response_id, person_id, question_id, n_tokens, <method>_<scale>.

  python variance_models.py [--data CSV] [--out CSV] [--work DIR] [--methods human teas zs] [--scales ...]
                            [--draws 2000] [--cores 1]
  -> ../results/variance_models.csv; work/person_effects.csv (person effects of m0, per person: keep local)
"""
import argparse
import logging
import warnings
from pathlib import Path

import arviz as az
import bambi as bmb
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
for _lg in ("pymc", "arviz", "bambi", "pytensor"):
    logging.getLogger(_lg).setLevel(logging.ERROR)

HERE = Path(__file__).resolve().parent
TOP = HERE.parent
DATA = TOP / "data" / "answers.csv"
OUT = TOP / "results" / "variance_models.csv"
WORK = HERE / "work"
METHODS = ["human", "teas", "zs"]
SCALES = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism", "answer_score",
          "interview_score"]
RE = "(1|person_id) + (1|question_id)"
SIGMAS = ["1|person_id_sigma", "1|question_id_sigma", "sigma"]
N_ANSWERS = 6
TARGET = 0.70


def fit(formula: str, data: pd.DataFrame, args):
    return bmb.Model(formula, data, family="gaussian").fit(
        draws=args.draws, tune=args.draws, chains=4, cores=args.cores, target_accept=0.9, random_seed=7,
        progressbar=False)


def components(idata) -> list[np.ndarray]:
    return [(np.asarray(idata.posterior[s]) ** 2).reshape(-1) for s in SIGMAS]


def interval(x: np.ndarray) -> tuple[float, float, float]:
    return float(np.mean(x)), float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))


def diagnostics(idata, names: list[str]) -> tuple[int, float]:
    rhat = az.summary(idata, var_names=names, kind="diagnostics")["r_hat"].max()
    return int(idata.sample_stats["diverging"].sum()), float(rhat)


def person_effects(idata, method: str, scale: str) -> pd.DataFrame:
    eff = idata.posterior["1|person_id"].mean(("chain", "draw"))
    return pd.DataFrame({"method": method, "scale": scale, "person_id": eff[eff.dims[0]].values,
                         "effect": eff.values})


def models(d: pd.DataFrame, method: str, scale: str, args) -> tuple[dict, pd.DataFrame]:
    col = f"{method}_{scale}"
    dd = d[["person_id", "question_id", "log_tokens_z", col]].dropna().rename(columns={col: "y"})
    dd["y"] = (dd.y - dd.y.mean()) / dd.y.std()
    dd[["person_id", "question_id"]] = dd[["person_id", "question_id"]].astype(str)
    m0 = fit(f"y ~ 1 + {RE}", dd, args)
    m1 = fit(f"y ~ 1 + log_tokens_z + {RE}", dd, args)
    p0, q0, r0 = components(m0)
    p1, q1, r1 = components(m1)
    share0, share1 = interval(p0 / (p0 + q0 + r0)), interval(p1 / (p1 + q1 + r1))
    erho = interval(p0 / (p0 + r0 / N_ANSWERS))
    phi = interval(p0 / (p0 + (q0 + r0) / N_ANSWERS))
    b = interval(np.asarray(m1.posterior["log_tokens_z"]).reshape(-1))
    div0, rhat0 = diagnostics(m0, SIGMAS)
    div1, rhat1 = diagnostics(m1, SIGMAS + ["log_tokens_z"])
    row = dict(method=method, scale=scale, n=len(dd), persons=dd.person_id.nunique(),
               abstention_pct=100 * (1 - len(dd) / len(d)),
               person_m0=p0.mean(), question_m0=q0.mean(), residual_m0=r0.mean(),
               person_m1=p1.mean(), question_m1=q1.mean(), residual_m1=r1.mean(),
               share_m0=share0[0], share_m0_lo=share0[1], share_m0_hi=share0[2],
               erho2_6=erho[0], erho2_6_lo=erho[1], erho2_6_hi=erho[2],
               phi_6=phi[0], phi_6_lo=phi[1], phi_6_hi=phi[2],
               n_phi70=TARGET / (1 - TARGET) * (q0.mean() + r0.mean()) / p0.mean(),
               person_drop_pct=100 * (1 - p1.mean() / p0.mean()),
               share_m1=share1[0], share_m1_lo=share1[1], share_m1_hi=share1[2],
               length_b=b[0], length_b_lo=b[1], length_b_hi=b[2],
               divergences=div0 + div1, rhat_max=max(rhat0, rhat1))
    return row, person_effects(m0, method, scale)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, default=DATA)
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--work", type=Path, default=WORK)
    ap.add_argument("--methods", nargs="+", default=METHODS, choices=METHODS)
    ap.add_argument("--scales", nargs="+", default=SCALES, choices=SCALES)
    ap.add_argument("--draws", type=int, default=2000)
    ap.add_argument("--cores", type=int, default=1)
    args = ap.parse_args()

    d = pd.read_csv(args.data)
    need = ["person_id", "question_id", "n_tokens"] + [f"{m}_{s}" for m in args.methods for s in args.scales]
    missing = [c for c in need if c not in d.columns]
    if missing:
        raise SystemExit(f"missing columns: {missing}")
    lt = np.log(d.n_tokens)
    d["log_tokens_z"] = (lt - lt.mean()) / lt.std()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.work.mkdir(parents=True, exist_ok=True)
    rows, effects = [], []
    for m in args.methods:
        for s in args.scales:
            row, eff = models(d, m, s, args)
            rows.append(row)
            effects.append(eff)
            print(f"{m:6} {s:18} n={row['n']:5}  share {row['share_m0']:.3f}  E-rho2 {row['erho2_6']:.3f}  "
                  f"Phi {row['phi_6']:.3f}  drop {row['person_drop_pct']:5.1f}%  length_b {row['length_b']:+.3f}  "
                  f"div {row['divergences']}  rhat {row['rhat_max']:.3f}", flush=True)
            pd.DataFrame(rows).round(4).to_csv(args.out, index=False)
            pd.concat(effects).to_csv(args.work / "person_effects.csv", index=False)
    print(f"wrote {args.out}, {args.work / 'person_effects.csv'}")


if __name__ == "__main__":
    main()
