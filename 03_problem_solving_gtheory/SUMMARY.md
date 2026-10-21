# What a problem-solving score measures: the person, the question, or answering well

Two language-model scores of problem solving were given to the same RecruitView answers: a zero-shot rating of the
whole answer and the evidence-weighted answer score ([`02_evidence_weighted`](../02_evidence_weighted/SUMMARY.md)).
This summary asks what the scores measure. Three readings are possible: a stable problem-solving level of the person;
something that depends on the question asked; or a general skill at answering interview questions well.

Trait activation theory (Tett & Guterman, 2000) expects a trait to show in behaviour when the situation calls for it.
Interview questions differ in how much they call for problem solving, so each question carries an activation level:
1 (problem solving not called for), 2 (room for it), 3 (a complete answer requires it).

## Results

- **About a quarter of the score variance is the person** (26%), and the two methods agree on it: person x method
  0.2% of the variance.
- **No sign that a person's standing differs by the question's activation** (person x activation 0.014
  [0.000, 0.126]). With 10 questions at activation 2 and 3 and no person answering two of them, a moderate effect
  cannot be excluded.
- **Activation widens the spread of answer scores while the disagreement between the methods stays the same**, so
  agreement on a single answer rises: .51 at activation 1, .63 at 2, .72 at 3.
- **Most of the person variance is shared with the answer quality of the person's other answers**, rated separately:
  58% of it (95% CI 36% to 92%). Answer length accounts for 26% (11% to 49%) and adds nothing once answer quality is in
  the model. This fits a general skill at answering well, a real link between problem solving and clear communication,
  or a shared impression of language-model raters; these data do not separate the three.
- **On questions that do not call for problem solving, the zero-shot rating leans more on general answer quality**
  than the evidence-weighted score (difference 0.13 per SD, SE 0.04); at activation 2 and 3 the two are equal.

## Sample by activation

| Activation | Questions | Answers | Scored by both methods | Persons |
|---|---|---|---|---|
| 1 | 66 | 1,682 | 453 (27%) | 225 |
| 2 | 6 | 120 | 85 (71%) | 85 |
| 3 | 4 | 83 | 72 (87%) | 72 |
| All | 76 | 1,885 | 610 (32%) | 265 |

## Variance components

Person x question x method, with activation as a fixed facet (questions nested in activation); scores standardized
within method; 95% intervals from a parametric bootstrap.

| Source | Variance [95% CI] | % |
|---|---|---|
| Person | 0.270 [0.151, 0.364] | 26.2 |
| Person x activation | 0.014 [0.000, 0.126] | 1.4 |
| Person x method | 0.002 [0.000, 0.035] | 0.2 |
| Question | 0.062 [0.015, 0.120] | 6.1 |
| Question x method | 0.021 [0.002, 0.042] | 2.0 |
| Person x question | 0.260 [0.176, 0.340] | 25.3 |
| Residual | 0.400 [0.342, 0.447] | 38.9 |

A person score from one method reaches E-rho2 = .70 at 6 answers that both methods can score (.71 [.57, .77]); the
mean of the two methods reaches it at 4. At activation 1 about one answer in four can be scored by both methods.

## Agreement of the two methods by activation

| Activation | Answers | Answer variance [95% CI] | Agreement [95% CI] |
|---|---|---|---|
| 1 | 453 | 0.429 [0.348, 0.519] | .51 [.44, .59] |
| 2 | 85 | 0.708 [0.463, 0.998] | .63 [.51, .74] |
| 3 | 72 | 0.948 [0.608, 1.388] | .72 [.59, .82] |

*Note.* Agreement = share of the answer variance common to the two methods.

## General answer quality and answer length

Covariates are computed on each person's other answers (answers outside this sample), so they share no answer with
the problem-solving scores. Answer quality is a separate zero-shot rating (`gpt-4o-mini`) of how thoroughly,
specifically and coherently the answer addresses the question.

| Covariates of the other answers | Person variance [95% CI] | Share of person variance left [95% CI] |
|---|---|---|
| none | 0.270 [0.162, 0.367] | 1.00 |
| answer length | 0.201 [0.125, 0.277] | .74 [.51, .89] |
| answer quality | 0.112 [0.025, 0.184] | .42 [.08, .64] |
| answer quality + answer length | 0.114 [0.028, 0.182] | .42 [.11, .61] |

*Note.* Person variance: parametric bootstrap; share left: 200 person-cluster resamples.

## Data properties to keep in mind

- Activation 2 and 3 cover 10 questions; no person has more than one answer at these levels.
- The sample holds the answers both methods could score; at activation 1 that is 27% of the answers. Reliability
  figures refer to such answers.
- Scores are coarse: the evidence-weighted score is 3 on 70% of the answers, the zero-shot rating is 1 to 3 on 98%.
  The models treat them as continuous; parametric bootstrap intervals rest on the model's assumptions.
- The activation level of each question comes from one labelling of the question text, without an agreement check.
- All scores, including answer quality, are language-model ratings of the same transcripts.

Full report with methods, D-study and all tables: [`REPORT.md`](REPORT.md).

## References

Tett, R. P., & Guterman, H. A. (2000). Situation trait relevance, trait expression, and cross-situational consistency:
Testing a principle of trait activation. *Journal of Research in Personality, 34*(4), 397-423.
https://doi.org/10.1006/jrpe.2000.2292
