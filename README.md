# AI interview scoring as measurement

Psychometric work on AI scoring of video-interview answers. The data are RecruitView interviews: 1,885 answers of 328
candidates to 76 questions, each answer with an AI-generated report and human ratings. The work asks how different
scoring methods work, why they give the scores they give, how reliable each one is, and what a score measures.

### My approach

I develop and evaluate assessment systems that operate on human-generated data, whether AI-powered or not. This
repository shows four parts of that work:

- **Scoring in several ways:** zero-shot language-model ratings of transcripts, numeric coding of an AI-generated
  report, and an evidence-weighted pipeline that links every score to the quotes behind it.
- **Checking how and why a scoring works:** answer length, negative controls (content removed at a fixed length),
  agreement between methods given the same definitions.
- **Building scoring pipelines:** extraction, rating and checking stages run in batches, with every published prompt
  checked against the hash in its call log.
- **Measuring what a score is worth:** generalizability theory with scoring method and question as facets, and person
  covariates that show what the person component shares with other measures.

## Summaries

| | Summary | Question |
|---|---|---|
| 1 | [Scoring audit: human ratings, the dataset's AI report and a zero-shot scorer](01_scoring_audit/SUMMARY.md) | How reliable is each method, do the methods agree, and what drives the scores? |
| 2 | [Evidence-weighted interview scoring](02_evidence_weighted/SUMMARY.md) | Can a score be transparent and less driven by answer length, and what does that cost? |
| 3 | [What a problem-solving score measures](03_problem_solving_gtheory/SUMMARY.md) | Is the score the person, the question asked, or a general skill at answering well? |

Key results so far, scoring audit (seven scales, three methods, 1,885 answers):

- On a single answer, persons account for 10% to 48% of the score variance; the zero-shot rating of the transcript
  has the largest share on four of seven scales.
- Person effects of human ratings and of the numeric coding of the AI report correlate negatively on all seven
  scales (-.23 to -.63).
- Longer answers go with less favourable human ratings and more favourable language-model scores.
- At a fixed length, shuffled or random words turn most zero-shot ratings into "not estimable".

Problem solving (summaries 2 and 3, 1,885 answers):

- A zero-shot rating and the evidence-weighted score, given the same definition and rating scale, **order candidates
  the same way** (both are judgments of the same model); only the evidence-weighted score shows which quotes each
  score rests on, and it depends less on answer length.
- The evidence-weighted score covers fewer answers (37%) and on its own is less reliable.
- At a fixed length, shuffled or random words make the zero-shot rating "not estimable" in 78% and 100% of 240 rated
  answers (60 in each of four length groups); another answer of the same candidate in which the original run found no
  problem-solving behaviour, placed under the question, is rated in 6 of 240. Ratings kept after shuffling come mostly from answers rated 3 or higher.
- About a quarter of the score variance is the candidate; **most of it is shared with the answer quality of the
  candidate's other answers**. Questions that call for problem solving give more to score and more agreement between
  the two methods.

## Terms

- **Person variance (person share):** the share of score variance due to stable differences between candidates.
- **Facet:** a source of variation in the design, such as question, scoring method or question activation.
- **E-rho2 (generalizability coefficient):** reliability of a candidate's score averaged over a number of questions,
  for ranking candidates who answered the same questions. **Phi:** the same with differences between questions
  counted as error; it applies to absolute decisions and to candidates who answered different questions.
- **D-study:** how reliability changes with the number of questions or scoring methods.
- **Question activation:** how much a question calls for the competency (trait activation theory).

## Repository

```
README.md
01_scoring_audit/              summary, analysis scripts (reliability, answer length, agreement, negative control)
02_evidence_weighted/          summary, prompts of every stage, one answer through the pipeline
03_problem_solving_gtheory/    summary, full report, analysis script, result tables and figures
```

## Data access

RecruitView (Gupta et al., 2025) is a gated dataset licensed CC BY-NC 4.0 (academic, non-commercial). This repository
does not redistribute it; access can be requested at
[huggingface.co/datasets/AI4A-lab/RecruitView](https://huggingface.co/datasets/AI4A-lab/RecruitView). Only aggregate
results are shared here, plus one answer used as a worked example. The dataset's human ratings are pairwise-derived
z-scores within question; they are analysed in summary 1. This is research on measurement properties of interview
scoring; it is not a hiring tool.

Gupta, A. K., Sheth, F., Shaikh, H., Kumar, D., Puniya, A., Panwar, D., Chaurasia, S., & Mathur, P. (2025).
*RecruitView: A multimodal dataset for predicting personality and interview performance for human resources
applications* (arXiv:2512.00450). arXiv. https://arxiv.org/abs/2512.00450

## Contacts

[olgamaslenkova@gmail.com](mailto:olgamaslenkova@gmail.com) ·
