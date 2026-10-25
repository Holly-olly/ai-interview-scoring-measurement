"""Negative control of the zero-shot rating: share of "not estimable" ratings and mean rating per condition.

Each answer is rated in four conditions: intact; word_shuffle (the same words in random order); random_words (as many
random corpus words as the answer has); offtopic (a coherent answer to a different question with the nearest word
count). Input: a CSV with one row per answer, scale and condition and the columns response_id, scale, condition,
score (0 = not estimable).

  python negative_control.py [--scores CSV] [--out CSV]
  -> ../results/negative_control.csv
"""
import argparse
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
TOP = HERE.parent
SCORES = TOP / "data" / "negcontrol_scores.csv"
OUT = TOP / "results" / "negative_control.csv"
SCALES = ["openness", "conscientiousness", "extraversion", "agreeableness", "emotional_stability", "answer_score",
          "interview_score"]
CONDS = ["intact", "word_shuffle", "random_words", "offtopic"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scores", type=Path, default=SCORES)
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()

    d = pd.read_csv(args.scores)
    d["not_estimable"] = d.score.eq(0)
    pct = d.pivot_table(index="scale", columns="condition", values="not_estimable", aggfunc="mean")
    pct = pct.reindex(SCALES)[CONDS] * 100
    mean = d[~d.not_estimable].pivot_table(index="scale", columns="condition", values="score", aggfunc="mean")
    mean = mean.reindex(SCALES)[CONDS]

    print(f"{d.response_id.nunique()} answers, {len(d)} ratings")
    print("\nnot estimable, %\n" + pct.round(0).astype(int).to_string())
    print("\nmean of the ratings given\n" + mean.round(2).to_string())
    args.out.parent.mkdir(parents=True, exist_ok=True)
    pd.concat({"not_estimable_pct": pct, "mean_rated": mean}, axis=1).round(3).to_csv(args.out)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
