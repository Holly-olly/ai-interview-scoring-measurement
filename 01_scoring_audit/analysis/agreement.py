"""Agreement between scoring methods: person effects of human ratings and TEAS; single answers of TEAS and zero-shot.

Human and TEAS: Pearson and Spearman of the person effects (posterior means of m0 in variance_models.py) over persons
with both; 95% interval of Pearson by Fisher z. TEAS and zero-shot: Spearman over the answers both methods scored;
95% interval from a person-cluster bootstrap.

  python agreement.py [--data CSV] [--effects CSV] [--out CSV] [--boot 1000]
  -> ../results/agreement.csv
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr

HERE = Path(__file__).resolve().parent
TOP = HERE.parent
DATA = TOP / "data" / "answers.csv"
EFFECTS = HERE / "work" / "person_effects.csv"
OUT = TOP / "results" / "agreement.csv"
SCALES = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism", "answer_score",
          "interview_score"]


def fisher_interval(r: float, n: int) -> tuple[float, float]:
    z, se = np.arctanh(r), 1 / np.sqrt(n - 3)
    return float(np.tanh(z - 1.96 * se)), float(np.tanh(z + 1.96 * se))


def cluster_bootstrap(x: pd.DataFrame, boot: int, rng: np.random.Generator) -> tuple[float, float]:
    rows = x.groupby("person_id").indices
    persons = np.array(list(rows))
    stats = []
    for _ in range(boot):
        idx = np.concatenate([rows[p] for p in rng.choice(persons, len(persons))])
        stats.append(spearmanr(x.a.values[idx], x.b.values[idx])[0])
    return float(np.percentile(stats, 2.5)), float(np.percentile(stats, 97.5))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, default=DATA)
    ap.add_argument("--effects", type=Path, default=EFFECTS)
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--boot", type=int, default=1000)
    args = ap.parse_args()

    d = pd.read_csv(args.data)
    e = pd.read_csv(args.effects).pivot_table(index="person_id", columns=["method", "scale"], values="effect")
    rng = np.random.default_rng(7)
    rows = []
    for s in SCALES:
        p = e[[("human", s), ("teas", s)]].dropna()
        r = pearsonr(p.iloc[:, 0], p.iloc[:, 1])[0]
        lo, hi = fisher_interval(r, len(p))
        a = d[["person_id", f"teas_{s}", f"zs_{s}"]].dropna().set_axis(["person_id", "a", "b"], axis=1)
        a = a.reset_index(drop=True)
        blo, bhi = cluster_bootstrap(a, args.boot, rng)
        rows.append(dict(scale=s, persons=len(p), human_teas_pearson=r, human_teas_pearson_lo=lo,
                         human_teas_pearson_hi=hi, human_teas_spearman=spearmanr(p.iloc[:, 0], p.iloc[:, 1])[0],
                         answers=len(a), teas_zs_spearman=spearmanr(a.a, a.b)[0], teas_zs_spearman_lo=blo,
                         teas_zs_spearman_hi=bhi))
        print(f"{s:18} human-TEAS r={r:+.3f} [{lo:+.3f}, {hi:+.3f}] n={len(p)}   "
              f"TEAS-zs rho={rows[-1]['teas_zs_spearman']:.3f} [{blo:.3f}, {bhi:.3f}] n={len(a)}", flush=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).round(4).to_csv(args.out, index=False)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
