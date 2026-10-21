"""G-theory of problem-solving interview scores from one answer-level dataset.

Two scoring methods of the same answers (zero-shot rating of the whole answer, evidence-weighted answer score),
problem-solving activation of the question as a fixed facet, and the share of person variance that the answer quality
and the answer length of the person's other answers account for. Input: a CSV with one row per answer and the numeric
columns in REQUIRED (../README.md); any dataset with these columns runs. Models: lme4 REML in
gtheory_models.R; percentile CIs from a parametric bootstrap.

  python run_analysis.py [--data CSV] [--out DIR] [--boot 500]
  -> DIR/results/table*.csv, DIR/results/tables.md, DIR/results/results.txt, DIR/figures/fig*.png
     (defaults: ../data/ps_answers.csv, DIR = this folder; model input in analysis/work/, with --out in DIR/work/)

Requires Python 3 (pandas, numpy, matplotlib) and R with lme4 (Rscript on the PATH).
"""
import argparse
import subprocess
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
TOP = HERE.parent
DATA = TOP / "data" / "ps_answers.csv"
WORK = HERE / "work"          # answer x method model input (row-level, gated data)
RES = TOP / "results"
FIG = TOP / "figures"
REQUIRED = ["response_id", "person_id", "question_id", "activation", "n_tokens", "ps_zero_shot", "ps_evidence_weighted",
            "answer_quality"]
SOURCES = ["person", "person:activation", "person:method", "question", "question:method", "person:question", "residual"]
SOURCE_LABEL = {"person": "Person (p)", "person:activation": "Person x activation (pa)",
                "person:method": "Person x method (pm)", "question": "Question (q)",
                "question:method": "Question x method (qm)", "person:question": "Person x question (pq)",
                "residual": "Residual (pqm,e)", "total": "Total"}
COVS = {"cov_none": "none", "cov_length": "answer length", "cov_quality": "answer quality",
        "cov_quality_length": "answer quality + answer length"}
# Neural Haze palette (lib/palette.ts)
SURFACE, INK, MUTED, GRID = "#1C1928", "#F0EFF8", "#C5C3D6", "#6E6A88"
COLOR = {"zero_shot": "#9B30FF", "evidence_weighted": "#C8F135", "answer_quality": "#00F5D4", "both": "#FF2D78"}
SOURCE_COLOR = {"person": "#C8F135", "person:activation": "#6B9A0A", "person:method": "#00F5D4", "question": "#9B30FF",
                "question:method": "#4E0FAD", "person:question": "#FF2D78", "residual": "#6E6A88"}


def load() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Answers, and the answer x method rows of the G-study sample with the person covariates."""
    a = pd.read_csv(DATA)
    check(a)
    a["log_tokens"] = np.log(a.n_tokens)
    a["common"] = (a.ps_zero_shot > 0) & a.ps_evidence_weighted.notna()
    other = a[~a.common]                                         # answers outside the G-study sample
    z = lambda m: (m - m.mean()) / m.std()
    quality = other[other.answer_quality > 0].groupby("person_id").answer_quality.mean()
    length = other.groupby("person_id").log_tokens.mean()
    c = a[a.common]
    long = pd.concat([c.assign(method="zero_shot", score=c.ps_zero_shot),
                      c.assign(method="evidence_weighted", score=c.ps_evidence_weighted)])
    long["score_z"] = long.groupby("method").score.transform(lambda x: (x - x.mean()) / x.std())
    long["quality_other"] = long.person_id.map(z(quality))
    long["length_other"] = long.person_id.map(z(length))
    return a, long


def check(a: pd.DataFrame) -> None:
    """Structure the analysis needs; scores are any numbers (0 or empty = not scored)."""
    missing = [c for c in REQUIRED if c not in a]
    if missing:
        raise SystemExit(f"{DATA}: missing columns {missing}")
    text = [c for c in REQUIRED if not pd.api.types.is_numeric_dtype(a[c])]
    if text:
        raise SystemExit(f"{DATA}: non-numeric columns {text}")
    if a.response_id.duplicated().any():
        raise SystemExit(f"{DATA}: response_id is not unique (one row per answer)")
    if a[["person_id", "question_id", "activation", "n_tokens", "ps_zero_shot", "answer_quality"]].isna().any().any():
        raise SystemExit(f"{DATA}: empty values outside ps_evidence_weighted")
    if (a.n_tokens <= 0).any():
        raise SystemExit(f"{DATA}: n_tokens must be above 0")
    if a.activation.nunique() < 2:
        raise SystemExit(f"{DATA}: activation needs at least 2 levels")


def run_models(long: pd.DataFrame, boot: int, boot_persons: int) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    WORK.mkdir(parents=True, exist_ok=True)
    cols = ["response_id", "person_id", "question_id", "activation", "method", "score_z", "quality_other", "length_other"]
    long[cols].to_csv(WORK / "scores.csv", index=False)
    subprocess.run(["Rscript", str(HERE / "gtheory_models.R"), str(WORK), str(boot), str(boot_persons)], check=True)
    return tuple(pd.read_csv(WORK / f) for f in ("components.csv", "fixed.csv", "stats.csv"))


# ---- tables (numeric, written as CSV) ------------------------------------------------------------------------------

def table_sample(a: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for level, g in [*a.groupby("activation"), ("all", a)]:
        c = g[g.common]
        vc = c.person_id.value_counts()
        rows.append({"activation": level, "questions": g.question_id.nunique(), "answers": len(g),
                     "zero_shot_rated": int((g.ps_zero_shot > 0).sum()),
                     "evidence_weighted_scored": int(g.ps_evidence_weighted.notna().sum()), "both": len(c),
                     "questions_both": c.question_id.nunique(), "persons_both": c.person_id.nunique(),
                     "persons_2plus_answers_both": int((vc >= 2).sum())})
    t = pd.DataFrame(rows)
    for col in ("zero_shot_rated", "evidence_weighted_scored", "both"):
        t[col + "_pct"] = (100 * t[col] / t.answers).round(1)
    return t


def table_levels(a: pd.DataFrame) -> pd.DataFrame:
    c = a[a.common]
    return pd.DataFrame({"level": range(6),
                         "zero_shot_all": [int((a.ps_zero_shot == k).sum()) for k in range(6)],
                         "zero_shot_sample": [int((c.ps_zero_shot == k).sum()) for k in range(6)],
                         "answer_quality_all": [int((a.answer_quality == k).sum()) for k in range(6)],
                         "answer_quality_sample": [int((c.answer_quality == k).sum()) for k in range(6)]})


def table_summary(a: pd.DataFrame) -> pd.DataFrame:
    c = a[a.common]
    rows = []
    for name, s in [("zero-shot, answers rated 1 to 5", a.ps_zero_shot[a.ps_zero_shot > 0]),
                    ("zero-shot, G-study sample", c.ps_zero_shot),
                    ("evidence-weighted, answers with a score", a.ps_evidence_weighted.dropna()),
                    ("evidence-weighted, G-study sample", c.ps_evidence_weighted),
                    ("answer quality, answers rated 1 to 5", a.answer_quality[a.answer_quality > 0]),
                    ("answer quality, G-study sample", c.answer_quality[c.answer_quality > 0]),
                    ("answer length (tokens), all answers", a.n_tokens),
                    ("answer length (tokens), G-study sample", c.n_tokens)]:
        rows.append({"measure": name, "n": len(s), "mean": s.mean(), "sd": s.std(), "min": s.min(),
                     "q1": s.quantile(0.25), "median": s.median(), "q3": s.quantile(0.75), "max": s.max()})
    return pd.DataFrame(rows).round(2)


def table_correlations(a: pd.DataFrame) -> pd.DataFrame:
    c = a[a.common]
    rows = []
    for level, g in [*c.groupby("activation"), ("all", c)]:
        sp = lambda d, x, y: d[x].corr(d[y], method="spearman")
        q = g[g.answer_quality > 0]
        rows.append({"activation": level, "answers": len(g),
                     "zero_shot__evidence_weighted": sp(g, "ps_zero_shot", "ps_evidence_weighted"),
                     "zero_shot__answer_quality": sp(q, "ps_zero_shot", "answer_quality"),
                     "evidence_weighted__answer_quality": sp(q, "ps_evidence_weighted", "answer_quality"),
                     "zero_shot__length": sp(g, "ps_zero_shot", "n_tokens"),
                     "evidence_weighted__length": sp(g, "ps_evidence_weighted", "n_tokens")})
    return pd.DataFrame(rows).round(2)


def table_components(stats: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for model in ("base", "joint"):
        s = stats[(stats.model == model) & stats.stat.str.startswith("sigma2_")]
        total = s.estimate.sum()
        for r in s.itertuples():
            rows.append({"model": model, "source": r.stat[len("sigma2_"):], "variance": r.estimate,
                         "ci_lo": r.ci_lo, "ci_hi": r.ci_hi, "pct": 100 * r.estimate / total})
        rows.append({"model": model, "source": "total", "variance": total, "pct": 100.0})
    t = pd.DataFrame(rows)
    t["order"] = t.source.map({k: i for i, k in enumerate(SOURCES + ["total"])})
    return t.sort_values(["model", "order"]).drop(columns="order").round(4)


def table_dstudy(stats: pd.DataFrame) -> pd.DataFrame:
    s = stats[stats.model.isin(["base", "joint"]) & stats.stat.str.match(r"(erho2|phi)_m\d_q\d+$")]
    p = s.stat.str.extract(r"(?P<coefficient>erho2|phi)_m(?P<methods>\d)_q(?P<questions>\d+)")
    s = pd.concat([s, p], axis=1).astype({"methods": int, "questions": int})
    cols = ["model", "coefficient", "methods", "questions", "estimate", "ci_lo", "ci_hi"]
    return s[cols].sort_values(cols[:4]).round(3)


def table_agreement(a: pd.DataFrame, stats: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for level in sorted(a.activation.unique()):
        s = stats[stats.model == f"level_{level}"].set_index("stat")
        g = a[a.common & (a.activation == level)]
        row = {"activation": level, "answers": len(g), "questions": g.question_id.nunique()}
        for k in ("sigma2_answer", "sigma2_question", "sigma2_question:method", "sigma2_residual", "agreement"):
            row.update({k: s.loc[k, "estimate"], k + "_lo": s.loc[k, "ci_lo"], k + "_hi": s.loc[k, "ci_hi"]})
        rows.append(row)
    return pd.DataFrame(rows).round(3)


def table_covariates(stats: pd.DataFrame, fixed: pd.DataFrame, comp: pd.DataFrame) -> pd.DataFrame:
    person = stats[stats.stat == "sigma2_person"].set_index("model")
    share = stats[stats.stat == "share_left"].set_index("model")
    rows = []
    for model, label in COVS.items():
        f = fixed[fixed.model == model].set_index("term")
        row = {"covariates": label, "person_variance": person.loc[model, "estimate"],
               "ci_lo": person.loc[model, "ci_lo"], "ci_hi": person.loc[model, "ci_hi"],
               "share_left": person.loc[model, "estimate"] / person.loc["cov_none", "estimate"],
               "share_lo": share.ci_lo.get(model, np.nan), "share_hi": share.ci_hi.get(model, np.nan),
               "singular": bool(comp[comp.model == model].singular.iloc[0])}
        for cov in ("quality_other", "length_other"):
            if cov in f.index:
                row[cov + "_evidence_weighted"], row[cov + "_evidence_weighted_se"] = f.loc[cov, ["estimate", "se"]]
                row[cov + "_zs_minus_ew"], row[cov + "_zs_minus_ew_se"] = f.loc[f"methodzero_shot:{cov}",
                                                                                ["estimate", "se"]]
        rows.append(row)
    return pd.DataFrame(rows).round(3)


def table_quality_levels(a: pd.DataFrame, fixed: pd.DataFrame, comp: pd.DataFrame) -> pd.DataFrame:
    answer = comp[comp.component == "answer"].set_index("model").variance
    rows = []
    for level in sorted(a.activation.unique()):
        f = fixed[fixed.model == f"level_{level}_quality"].set_index("term")
        b, se = f.loc["quality_other", ["estimate", "se"]]
        diff, dse = f.loc["methodzero_shot:quality_other", ["estimate", "se"]]
        rows.append({"activation": level, "evidence_weighted": b, "evidence_weighted_se": se, "zero_shot": b + diff,
                     "zs_minus_ew": diff, "zs_minus_ew_se": dse, "answer_variance": answer[f"level_{level}"],
                     "answer_variance_with_quality": answer[f"level_{level}_quality"]})
    return pd.DataFrame(rows).round(3)


# ---- formatted tables (report style) -------------------------------------------------------------------------------

def apa(x: float, nd: int = 2) -> str:
    """Statistic bounded by 1, without the leading zero."""
    if pd.isna(x):
        return ""
    s = f"{x:.{nd}f}"
    return s.replace("0.", ".", 1) if abs(x) < 1 else s


def num(x: float, nd: int = 3) -> str:
    return "" if pd.isna(x) else f"{x:.{nd}f}"


def ci(lo: float, hi: float, fmt=num) -> str:
    return "" if pd.isna(lo) else f"[{fmt(lo)}, {fmt(hi)}]"


def formatted(t: dict) -> dict:
    out = {}
    s = t["sample"]
    out["Table 1. Sample by problem-solving activation of the question"] = pd.DataFrame({
        "Activation": s.activation, "Questions": s.questions, "Answers": s.answers,
        "Zero-shot rated 1-5": [f"{n} ({p}%)" for n, p in zip(s.zero_shot_rated, s.zero_shot_rated_pct)],
        "Evidence-weighted score": [f"{n} ({p}%)" for n, p in zip(s.evidence_weighted_scored,
                                                                 s.evidence_weighted_scored_pct)],
        "Both (G-study)": [f"{n} ({p}%)" for n, p in zip(s.both, s.both_pct)],
        "Persons": s.persons_both, "Persons with 2+ answers": s.persons_2plus_answers_both})
    out["Table 2. Score levels (answers)"] = t["levels"]
    out["Table 3. Score distributions"] = t["summary"]
    r = t["correlations"]
    out["Table 4. Spearman correlations between scores, G-study sample"] = pd.DataFrame({
        "Activation": r.activation, "Answers": r.answers,
        "Zero-shot, evidence-weighted": r.zero_shot__evidence_weighted.map(apa),
        "Zero-shot, answer quality": r.zero_shot__answer_quality.map(apa),
        "Evidence-weighted, answer quality": r.evidence_weighted__answer_quality.map(apa),
        "Zero-shot, length": r.zero_shot__length.map(apa),
        "Evidence-weighted, length": r.evidence_weighted__length.map(apa)})
    c = t["components"]
    g = pd.DataFrame({"Source": [SOURCE_LABEL[k] for k in SOURCES + ["total"]]})
    for model, name in (("base", "p x q x m"), ("joint", "p x (q:a) x m")):
        m = c[c.model == model].set_index("source").reindex(SOURCES + ["total"])
        g[f"{name}: variance"] = m.variance.map(num).to_numpy()
        g[f"{name}: 95% CI"] = [ci(lo, hi) for lo, hi in zip(m.ci_lo, m.ci_hi)]
        g[f"{name}: %"] = m.pct.map(lambda x: "" if pd.isna(x) else f"{x:.1f}").to_numpy()
    out["Table 5. Variance components (scores standardized within method)"] = g
    d = t["dstudy"]
    b = d[d.model == "base"]
    rows = []
    for nq in sorted(b.questions.unique()):
        row = {"Questions": nq}
        for nm in (1, 2):
            for coef, label in (("erho2", "E-rho2"), ("phi", "Phi")):
                x = b[(b.methods == nm) & (b.questions == nq) & (b.coefficient == coef)].iloc[0]
                row[f"{label}, {nm} method{'s' if nm > 1 else ''}"] = f"{apa(x.estimate)} {ci(x.ci_lo, x.ci_hi, apa)}"
        j = d[(d.model == "joint") & (d.questions == nq) & (d.methods == 1)]
        row["E-rho2 with activation, 1 method"] = (f"{apa(j.estimate.iloc[0])} {ci(j.ci_lo.iloc[0], j.ci_hi.iloc[0], apa)}"
                                                   if len(j) else "")
        rows.append(row)
    out["Table 6. D-study"] = pd.DataFrame(rows)
    ag = t["agreement"]
    out["Table 7. Agreement of the two methods by activation level"] = pd.DataFrame({
        "Activation": ag.activation, "Questions": ag.questions, "Answers": ag.answers,
        "Answer variance": [f"{num(v)} {ci(lo, hi)}" for v, lo, hi in
                            zip(ag.sigma2_answer, ag.sigma2_answer_lo, ag.sigma2_answer_hi)],
        "Question": ag.sigma2_question.map(num), "Question x method": ag["sigma2_question:method"].map(num),
        "Residual": ag.sigma2_residual.map(num),
        "Agreement": [f"{apa(v)} {ci(lo, hi, apa)}" for v, lo, hi in zip(ag.agreement, ag.agreement_lo,
                                                                          ag.agreement_hi)]})
    cv = t["covariates"]
    coef = lambda row, cov: ("" if pd.isna(row.get(cov + "_evidence_weighted")) else
                             f"{num(row[cov + '_evidence_weighted'], 2)} ({num(row[cov + '_evidence_weighted_se'], 2)}); "
                             f"{num(row[cov + '_zs_minus_ew'], 2)} ({num(row[cov + '_zs_minus_ew_se'], 2)})")
    out["Table 8. Person variance with person covariates of the other answers"] = pd.DataFrame({
        "Covariates": cv.covariates, "Person variance": [f"{num(v)} {ci(lo, hi)}" for v, lo, hi in
                                                         zip(cv.person_variance, cv.ci_lo, cv.ci_hi)],
        "Share left [95% CI]": [f"{apa(s)} {ci(lo, hi, apa)}".strip() for s, lo, hi in
                                zip(cv.share_left, cv.share_lo, cv.share_hi)],
        "Answer quality: EW (SE); ZS - EW (SE)": [coef(r, "quality_other") for _, r in cv.iterrows()],
        "Answer length: EW (SE); ZS - EW (SE)": [coef(r, "length_other") for _, r in cv.iterrows()]})
    q = t["quality_levels"]
    out["Table 9. Answer quality of the other answers by activation level"] = pd.DataFrame({
        "Activation": q.activation,
        "Evidence-weighted (SE)": [f"{num(b, 2)} ({num(s, 2)})" for b, s in zip(q.evidence_weighted,
                                                                               q.evidence_weighted_se)],
        "Zero-shot": q.zero_shot.map(lambda x: num(x, 2)),
        "ZS - EW (SE)": [f"{num(b, 2)} ({num(s, 2)})" for b, s in zip(q.zs_minus_ew, q.zs_minus_ew_se)],
        "Answer variance, without -> with": [f"{num(x)} -> {num(y)}" for x, y in
                                             zip(q.answer_variance, q.answer_variance_with_quality)]})
    return out


def markdown(df: pd.DataFrame) -> str:
    cols = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    lines += ["| " + " | ".join("" if pd.isna(v) else str(v) for v in r) + " |" for r in df.itertuples(index=False)]
    return "\n".join(lines)


# ---- figures -------------------------------------------------------------------------------------------------------

def theme() -> None:
    plt.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE, "text.color": INK,
        "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "axes.edgecolor": GRID,
        "font.size": 10, "axes.titlesize": 11, "axes.titleweight": "bold", "axes.spines.top": False,
        "axes.spines.right": False, "legend.frameon": False})


def save(fig, name: str) -> None:
    fig.tight_layout()
    fig.savefig(FIG / name, dpi=200)
    plt.close(fig)


def fig_distributions(a: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 3.6))
    for ax, col, key, title in [(axes[0], "ps_zero_shot", "zero_shot", "Zero-shot rating, all answers"),
                                (axes[2], "answer_quality", "answer_quality", "Answer quality (Stage-5), all answers")]:
        n = [int((a[col] == k).sum()) for k in range(6)]
        bars = ax.bar(range(6), n, color=[GRID] + [COLOR[key]] * 5)
        ax.bar_label(bars, color=INK, fontsize=8, padding=2)
        ax.set_xticks(range(6), ["0\nnot est."] + [str(k) for k in range(1, 6)])
        ax.set_title(title, loc="left")
        ax.set_ylabel("Answers")
    ew = a.ps_evidence_weighted.dropna()
    axes[1].hist(ew, bins=np.arange(1, 5.25, 0.25), color=COLOR["evidence_weighted"], edgecolor=SURFACE)
    axes[1].set_title(f"Evidence-weighted score, {len(ew)} answers", loc="left")
    axes[1].set_xlabel("Strength-weighted mean level of the units")
    save(fig, "fig1_score_distributions.png")


def fig_coverage(sample: pd.DataFrame) -> None:
    t = sample[sample.activation != "all"]
    x, w = np.arange(len(t)), 0.26
    fig, ax = plt.subplots(figsize=(8, 4))
    for i, (col, key, label) in enumerate([("zero_shot_rated_pct", "zero_shot", "Zero-shot rated 1 to 5"),
                                           ("evidence_weighted_scored_pct", "evidence_weighted",
                                            "Evidence-weighted score"),
                                           ("both_pct", "both", "Both (G-study sample)")]):
        bars = ax.bar(x + (i - 1) * w, t[col], w, color=COLOR[key], label=label)
        ax.bar_label(bars, fmt="%.0f%%", color=INK, fontsize=8, padding=2)
    ax.set_xticks(x, [f"Activation {v}\n{q} questions, {n} answers"
                      for v, q, n in zip(t.activation, t.questions, t.answers)])
    ax.set_ylim(0, 105)
    ax.set_ylabel("% of answers")
    ax.set_title("Answers scored by each method, by problem-solving activation of the question", loc="left")
    ax.legend(loc="upper left", fontsize=8)
    save(fig, "fig2_coverage_by_activation.png")


def fig_components(comp: pd.DataFrame) -> None:
    models = [("base", "p x q x m"), ("joint", "+ activation facet"),
              ("cov_quality", "+ answer quality (other answers)"), ("cov_quality_length", "+ answer quality and length")]
    fig, ax = plt.subplots(figsize=(10.5, 3.9))
    for i, (model, _) in enumerate(models):
        v = comp[comp.model == model].set_index("component").variance
        left = 0.0
        for src in SOURCES:
            if src in v:
                ax.barh(i, v[src], left=left, color=SOURCE_COLOR[src], edgecolor=SURFACE, height=0.6,
                        label=SOURCE_LABEL[src] if i == 1 or (i == 0 and src != "person:activation") else None)
                if v[src] >= 0.05:
                    ax.text(left + v[src] / 2, i, f"{v[src]:.2f}", ha="center", va="center", fontsize=8,
                            color=SURFACE if src not in ("question:method", "residual", "question") else INK)
                left += v[src]
    ax.set_yticks(range(len(models)), [m[1] for m in models])
    ax.invert_yaxis()
    ax.set_xlabel("Variance (scores standardized within method)")
    ax.set_title("Variance components of the problem-solving scores", loc="left")
    handles, labels = ax.get_legend_handles_labels()
    keep = dict(zip(labels, handles))
    ax.legend([keep[SOURCE_LABEL[s]] for s in SOURCES if SOURCE_LABEL[s] in keep],
              [SOURCE_LABEL[s] for s in SOURCES if SOURCE_LABEL[s] in keep],
              ncol=4, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.18))
    save(fig, "fig3_variance_components.png")


def fig_agreement(agreement: pd.DataFrame, correlations: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(6.5, 4))
    x = agreement.activation.astype(int).to_numpy()
    yerr = [agreement.agreement - agreement.agreement_lo, agreement.agreement_hi - agreement.agreement]
    ax.errorbar(x, agreement.agreement, yerr=None if agreement.agreement_lo.isna().all() else yerr, fmt="o-",
                color=COLOR["both"], capsize=4, label="Agreement (share of answer variance common to the methods)")
    rho = correlations[correlations.activation != "all"]
    ax.plot(x, rho.zero_shot__evidence_weighted, "s--", color=MUTED, label="Spearman, zero-shot and evidence-weighted")
    ax.set_xticks(x, [f"{v}\n{n} answers" for v, n in zip(x, agreement.answers)])
    ax.set_xlabel("Problem-solving activation of the question")
    ax.set_ylim(0, 1)
    ax.set_title("Agreement of the two methods by activation level", loc="left")
    ax.legend(fontsize=8, loc="lower right")
    save(fig, "fig4_agreement_by_activation.png")


def fig_dstudy(dstudy: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(6.5, 4))
    b = dstudy[(dstudy.model == "base") & (dstudy.coefficient == "erho2")]
    for nm, color in ((1, COLOR["zero_shot"]), (2, COLOR["evidence_weighted"])):
        s = b[b.methods == nm]
        ax.plot(s.questions, s.estimate, "o-", color=color, label=f"{nm} method{'s' if nm > 1 else ''}")
        if s.ci_lo.notna().all():
            ax.fill_between(s.questions, s.ci_lo, s.ci_hi, color=color, alpha=0.15, linewidth=0)
    ax.axhline(0.70, color=MUTED, linestyle=":", linewidth=1)
    ax.text(12, 0.71, ".70", color=MUTED, ha="right", va="bottom", fontsize=8)
    ax.set_xlabel("Questions per person")
    ax.set_ylabel("E-rho2")
    ax.set_ylim(0, 1)
    ax.set_title("D-study: generalizability of the person score", loc="left")
    ax.legend(fontsize=8, loc="lower right")
    save(fig, "fig5_dstudy.png")


def fig_covariates(cov: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(9, 3.6))
    y = np.arange(len(cov))
    xerr = None if cov.ci_lo.isna().all() else [cov.person_variance - cov.ci_lo, cov.ci_hi - cov.person_variance]
    ax.barh(y, cov.person_variance, xerr=xerr, color=COLOR["evidence_weighted"], ecolor=MUTED, capsize=3, height=0.6)
    right = cov.ci_hi.fillna(cov.person_variance)
    for yi, (x, s) in enumerate(zip(right, cov.share_left)):
        ax.text(x + 0.008, yi, f"{s:.0%} of the person variance left", va="center", color=INK, fontsize=8)
    ax.set_xlim(0, right.max() * 1.55)
    ax.set_yticks(y, cov.covariates)
    ax.invert_yaxis()
    ax.set_xlabel("Person variance")
    ax.set_title("Person variance with covariates of other answers", loc="left")
    save(fig, "fig6_person_variance_covariates.png")


def main() -> None:
    global DATA, WORK, RES, FIG
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(DATA), help="answer-level CSV with the columns in REQUIRED")
    ap.add_argument("--out", default="", help="output folder for results/ and figures/ (default: this folder)")
    ap.add_argument("--boot", type=int, default=500, help="parametric bootstrap draws (0 = no CIs)")
    ap.add_argument("--boot-persons", type=int, default=200,
                    help="person-cluster resamples for the share of person variance left (0 = no CI)")
    args = ap.parse_args()
    DATA = Path(args.data)
    if args.out:
        out = Path(args.out)
        WORK, RES, FIG = out / "work", out / "results", out / "figures"
    a, long = load()
    comp, fixed, stats = run_models(long, args.boot, args.boot_persons)
    t = {"sample": table_sample(a), "levels": table_levels(a), "summary": table_summary(a),
         "correlations": table_correlations(a), "components": table_components(stats),
         "dstudy": table_dstudy(stats), "agreement": table_agreement(a, stats),
         "covariates": table_covariates(stats, fixed, comp), "quality_levels": table_quality_levels(a, fixed, comp)}
    RES.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    for i, (name, df) in enumerate(t.items(), 1):
        df.to_csv(RES / f"table{i}_{name}.csv", index=False)
    persons = long.drop_duplicates("person_id")
    info = [f"Answers: {len(a)}; persons: {a.person_id.nunique()}; questions: {a.question_id.nunique()}.",
            f"G-study sample (zero-shot rated 1 to 5 and an evidence-weighted score): {long.response_id.nunique()} "
            f"answers, {long.person_id.nunique()} persons, {long.question_id.nunique()} questions.",
            f"Persons with both covariates: {int(persons[['quality_other', 'length_other']].notna().all(axis=1).sum())}; "
            f"Spearman between the two covariates: "
            f"{persons.quality_other.corr(persons.length_other, method='spearman'):.2f}.",
            f"Bootstrap draws: {args.boot} parametric, {args.boot_persons} person-cluster. Singular fits: "
            + ", ".join(sorted(comp[comp.singular].model.unique())) + "."]
    tables = formatted(t)
    (RES / "tables.md").write_text("\n\n".join([" ".join(info)] + [f"**{k}**\n\n{markdown(v)}" for k, v in
                                                                     tables.items()]) + "\n")
    with pd.option_context("display.width", 250, "display.max_columns", 30, "display.max_colwidth", 60):
        text = "\n".join(info) + "\n\n" + "\n\n".join(f"{k}\n{v.to_string(index=False)}" for k, v in tables.items())
    (RES / "results.txt").write_text(text + "\n")
    theme()
    fig_distributions(a)
    fig_coverage(t["sample"])
    fig_components(comp)
    fig_agreement(t["agreement"], t["correlations"])
    fig_dstudy(t["dstudy"])
    fig_covariates(t["covariates"])
    print(text)


if __name__ == "__main__":
    main()
