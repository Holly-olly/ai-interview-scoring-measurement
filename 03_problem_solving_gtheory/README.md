# Problem-solving G-study

Generalizability study of problem-solving scores of RecruitView video-interview answers: two language-model scoring
methods applied to the same answers, the problem-solving activation of the question as a facet, and the share of
person variance accounted for by the answer quality and answer length of the person's other answers.

| Path | Content |
|---|---|
| `REPORT.md` | Report: data, construct and rating scale, scoring methods, models, results |
| `data/` | Answer-level dataset, one row per answer (local, not distributed, see below) |
| `analysis/run_analysis.py` | All calculations from the dataset: tables, plain-text results, figures |
| `analysis/gtheory_models.R` | lme4 models, D-study and parametric bootstrap, called by `run_analysis.py` |
| `SUMMARY.md` | One-page summary |
| `results/` | `tables.md` (formatted tables), `results.txt` (plain text); the script also writes numeric `table*.csv` locally |
| `figures/` | `fig1` to `fig6` |

## Running

```
python analysis/run_analysis.py --boot 500
```

Requires Python 3 (pandas, numpy, matplotlib) and R with lme4 (`Rscript` on the PATH). `--boot 0` skips the
parametric confidence intervals; `--boot-persons` (default 200) sets the person-cluster resamples for the share of
person variance left by the covariates. Intermediate model input goes to `analysis/work/` (row-level, not distributed).

Any CSV with one row per answer and these numeric columns runs through the same analysis (0 or empty = not scored):

| Column | Content |
|---|---|
| `response_id`, `person_id`, `question_id` | ids of the answer, the person and the question |
| `activation` | problem-solving activation of the question, 2 or more levels |
| `n_tokens` | answer length in word tokens |
| `ps_zero_shot` | zero-shot problem-solving rating of the whole answer, 1 to 5 (0 = not estimable) |
| `ps_evidence_weighted` | evidence-weighted answer score (empty = no usable evidence unit) |
| `answer_quality` | answer quality rating of the whole answer, 1 to 5 (0 = not estimable) |

```
python analysis/run_analysis.py --data other_scores.csv --out other_results --boot 500
```

## Data

RecruitView (Gupta et al., 2025; https://huggingface.co/datasets/AI4A-lab/RecruitView) is a gated dataset under
CC BY-NC 4.0. This folder publishes aggregate results only. The answer-level dataset in `data/` holds row-level
scores and stays local; it is rebuilt by `build_ps_gtheory_dataset.py` of the evidence-weighted scoring pipeline, which is published
separately. The work is non-commercial research on measurement properties of interview scoring; it is not a hiring
tool.
