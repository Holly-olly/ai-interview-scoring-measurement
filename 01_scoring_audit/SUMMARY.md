# Scoring audit: human ratings, the dataset's AI report and a zero-shot scorer

RecruitView answers come with human ratings and with a report that Gemini wrote after watching each video answer
(Gupta et al., 2025). Here the same answers are scored in three ways, and each method is checked for reliability, for
its dependence on answer length and for agreement with the others. The sample is 1,885 answers of 328 persons to 76
questions.

Seven scales are scored: the five personality traits and two judgments of the interview.

| Scale | Question to the human raters | Definition given to the zero-shot rating (shortened) |
|---|---|---|
| Openness | "Which video shows the person is more OPEN to new experiences?" | desire to encounter a wide variety of ideas, feelings and activities |
| Conscientiousness | "Which video shows that the person is more ORGANIZED and RESPONSIBLE?" | goal-directed and planful behaviour, following norms and rules, effort and reliability |
| Extraversion | "Which video shows the person is more ENERGETIC and OUTGOING?" | enjoying interaction with others, being positive, energetic and assertive |
| Agreeableness | "Which video shows the person is more FRIENDLY and COMPASSIONATE?" | being likeable, pleasant and harmonious in relations with others |
| Neuroticism | "Which video shows the person is more SENSITIVE, UNSTABLE or NERVOUS?" | tendency to experience negative emotions such as anger, depression and anxiety; asked as emotional stability and reversed (6 - x) |
| Answer quality | wording not shown in the dataset paper | how thoroughly, specifically and coherently the answer addresses the question |
| Interview decision | "Which video's participant would you prefer to hire?" | whether the candidate should advance, judged on the content of the answers only |

*Note.* Human raters watched two video answers and chose "Video 1", "Video 2" or "None" (annotation form, Gupta et
al., 2025). TEAS codes the verdict that the Gemini report states for each scale. The zero-shot definitions and key
behaviours of the five traits are those of Stockdale, Hickman and Liu (2026), used without rating anchors or
examples; answer quality and interview decision were defined for this study from the RecruitView variable
descriptions.

| Method | Reads | Score |
|---|---|---|
| Human ratings | the video answer | released with the dataset: pairwise comparisons of answers, converted by the dataset authors into z-scores within question |
| TEAS (numeric coding of the Gemini report) | the Gemini report of the answer | `gpt-4o-mini` codes the report into a number per scale (1 to 5; interview decision 0 to 2), or gives none when the report does not support one |
| Zero-shot rating (`gpt-4o-mini`) | the answer transcript | `gpt-4o-mini` rates one answer on one scale per call (1 to 5; interview decision 1 to 3; 0 = not estimable) from the definition and key behaviours of the scale; temperature 0.3 |

*Note.* The zero-shot answer-quality rating is the answer-quality covariate of
[summary 3](../03_problem_solving_gtheory/SUMMARY.md). The zero-shot problem-solving rating of summaries 2 and 3 is a
different scorer (`gpt-4.1`).

## Results

- **Persons account for 10% to 48% of the variance of a single score.** The person share is .19 to .29 for human
  ratings, .10 to .35 for TEAS and .21 to .48 for the zero-shot rating. For a person's mean over six answers, Phi(6)
  is .58 to .71, .40 to .77 and .61 to .85. The zero-shot rating has the largest person share on conscientiousness,
  neuroticism, answer quality and interview decision, TEAS on extraversion, human ratings on agreeableness; on
  openness human ratings and the zero-shot rating are equal. The gap between methods is largest on answer quality.
- **Person effects of human ratings and TEAS correlate negatively on all seven scales:** Pearson -.23 to -.63.
- **TEAS and the zero-shot rating, two tasks of the same model, agree on single answers from .28 to .71**
  (Spearman): most on answer quality and conscientiousness, least on extraversion and neuroticism.
- **Longer answers go with less favourable human ratings and more favourable language-model scores**, on all seven
  scales (for human ratings: lower scores and higher neuroticism). With answer length in the model, the person
  variance falls by 18% to 67% on the six scales other than neuroticism; the largest person share left is .35
  (zero-shot answer quality, .48 without length).
- **At the same length, shuffled or random words turn most zero-shot ratings into "not estimable"** (51% to 99%). A
  coherent answer to a different question of similar length is "not estimable" more often than the intact answer
  (32% to 51% against 0% to 20%); when rated, its answer quality is lower (1.99 against 2.48) and its trait ratings
  are 0.07 to 0.38 lower.

## Reliability

Person x question G-study for each method: a Bayesian mixed model with person and question as random effects (m0 in
`analysis/variance_models.py`), on the score standardized within method and scale. Person share = person / (person +
question + residual); the residual holds the person x question interaction and error. E-rho2(6) and Phi(6) refer to a
person's mean over 6 answers, the median number of answers per person. Persons answered different questions, so the
differences between questions enter the comparison of persons: Phi(6) counts them as error, E-rho2(6) does not.

| Scale | Method | Person share [95% CI] | E-rho2(6) | Phi(6) [95% CI] | Answers for Phi = .70 |
|---|---|---|---|---|---|
| Openness | Human | .24 [.19, .29] | .65 | .65 [.59, .71] | 7.4 |
|  | TEAS | .15 [.10, .21] | .56 | .51 [.40, .61] | 13.0 |
|  | Zero-shot | .25 [.20, .30] | .71 | .66 [.60, .72] | 7.1 |
| Conscientiousness | Human | .21 [.17, .26] | .61 | .61 [.54, .68] | 8.7 |
|  | TEAS | .27 [.22, .32] | .72 | .68 [.63, .74] | 6.4 |
|  | Zero-shot | .37 [.31, .42] | .81 | .78 [.73, .81] | 4.0 |
| Extraversion | Human | .27 [.22, .32] | .69 | .69 [.63, .74] | 6.2 |
|  | TEAS | .30 [.25, .35] | .73 | .72 [.66, .77] | 5.5 |
|  | Zero-shot | .22 [.17, .27] | .67 | .62 [.56, .69] | 8.4 |
| Agreeableness | Human | .24 [.19, .29] | .65 | .65 [.59, .71] | 7.4 |
|  | TEAS | .10 [.05, .17] | .43 | .40 [.22, .55] | 20.2 |
|  | Zero-shot | .21 [.16, .26] | .67 | .61 [.53, .68] | 8.9 |
| Neuroticism | Human | .19 [.14, .23] | .58 | .58 [.50, .65] | 10.1 |
|  | TEAS | .24 [.19, .29] | .66 | .65 [.58, .71] | 7.5 |
|  | Zero-shot | .32 [.26, .37] | .77 | .73 [.68, .78] | 5.0 |
| Answer quality | Human | .29 [.24, .34] | .71 | .71 [.66, .76] | 5.7 |
|  | TEAS | .35 [.30, .41] | .82 | .77 [.72, .80] | 4.2 |
|  | Zero-shot | .48 [.43, .54] | .86 | .85 [.82, .87] | 2.5 |
| Interview decision | Human | .24 [.20, .29] | .66 | .66 [.60, .71] | 7.2 |
|  | TEAS | .31 [.26, .36] | .77 | .73 [.68, .77] | 5.2 |
|  | Zero-shot | .39 [.33, .44] | .82 | .79 [.75, .82] | 3.7 |

*Note.* Human scores are z-scores within question, so their question variance is close to zero and Phi(6) equals
E-rho2(6); for TEAS and the zero-shot rating Phi(6) is .01 to .06 lower. Answers for Phi = .70: D-study from the
posterior means of the variance components. TEAS openness and agreeableness rest on 1,202 and 1,059 answers (next
section) and have the widest intervals.

## Answers without a score

| Scale | TEAS | Zero-shot |
|---|---|---|
| Openness | 36.2% | 11.1% |
| Conscientiousness | 8.2% | 8.2% |
| Extraversion | 9.9% | 5.3% |
| Agreeableness | 43.8% | 15.5% |
| Neuroticism | 1.4% | 17.9% |
| Answer quality | 0.1% | 0.8% |
| Interview decision | 0.0% | 1.9% |

*Note.* Answers without a number are left out of every analysis of that method and scale; reliability and length
figures refer to the scored answers. TEAS gives no number when the Gemini report says little about a trait, so the
answers left out are not a random subset.

## Agreement between methods

| Scale | Human and TEAS, persons: Pearson [95% CI] (n) | TEAS and zero-shot, answers: Spearman [95% CI] (n) |
|---|---|---|
| Openness | -.37 [-.46, -.28] (323) | .51 [.47, .56] (1,133) |
| Conscientiousness | -.49 [-.56, -.40] (325) | .64 [.60, .67] (1,607) |
| Extraversion | -.43 [-.51, -.33] (327) | .29 [.23, .34] (1,621) |
| Agreeableness | -.23 [-.33, -.12] (306) | .48 [.43, .53] (996) |
| Neuroticism | -.28 [-.38, -.18] (328) | .28 [.23, .33] (1,534) |
| Answer quality | -.61 [-.67, -.53] (327) | .71 [.68, .73] (1,868) |
| Interview decision | -.63 [-.69, -.56] (328) | .60 [.57, .63] (1,849) |

*Note.* Person effects: posterior means of the person random effect in m0. Pearson interval by Fisher z; Spearman of
the person effects -.26 to -.66. Answers: those both methods scored; interval from 1,000 bootstrap samples of
persons. TEAS and the zero-shot rating are both judgments of `gpt-4o-mini`.

## Answer length

The G-study model m0 against m1, the same model with the log of answer length (standardized) as a predictor.

| Scale | Human: person variance | Human: length slope | TEAS: person variance | TEAS: length slope | Zero-shot: person variance | Zero-shot: length slope |
|---|---|---|---|---|---|---|
| Openness | -55% | -.35 | -60% | +.37 | -59% | +.45 |
| Conscientiousness | -44% | -.29 | -49% | +.40 | -51% | +.53 |
| Extraversion | -33% | -.25 | -18% | +.22 | -67% | +.49 |
| Agreeableness | -47% | -.31 | -33% | +.19 | -58% | +.45 |
| Neuroticism | -23% | +.20 | -2% | -.08 | -41% | -.42 |
| Answer quality | -52% | -.34 | -58% | +.52 | -47% | +.53 |
| Interview decision | -52% | -.33 | -57% | +.48 | -55% | +.52 |

*Note.* Person variance: change from m0 to m1. Length slope: SD of the score per SD of log answer length; every 95%
interval excludes zero. The slope pools length differences within and between persons. Person share with answer
length in the model: .13 to .20 (human), .06 to .26 (TEAS), .09 to .35 (zero-shot).

## Negative control (zero-shot rating)

248 answers, sampled across answer length, each rated in four conditions: intact; word shuffle (the same words in
random order); random words (as many random corpus words as the answer has); off-topic (a coherent answer to a
different question with the nearest word count).

| Scale | Intact | Word shuffle | Random words | Off-topic |
|---|---|---|---|---|
| Openness | 9% | 73% | 93% | 36% |
| Conscientiousness | 9% | 51% | 87% | 39% |
| Extraversion | 7% | 78% | 96% | 33% |
| Agreeableness | 17% | 91% | 99% | 51% |
| Neuroticism (rated as emotional stability) | 20% | 88% | 98% | 50% |
| Answer quality | 0% | 51% | 97% | 32% |
| Interview decision | 1% | 62% | 95% | 33% |

*Note.* Share of ratings "not estimable". Mean of the ratings given, answer quality: intact 2.48, word shuffle 1.01,
random words 1.00, off-topic 1.99; under word shuffle and random words these means rest on the few answers still
rated.

## Data properties to keep in mind

- Human scores are model-derived: within-question z-scores from a nuclear-norm multinomial-logit model over pairwise
  comparisons. Their tails are heavy (excess kurtosis about 9 to 14 on most scales); neuroticism has a narrow spread
  (SD .49 against about 1.1 on the other scales).
- The three methods share scale names, not questions (scale table above).
- TEAS and zero-shot scores are integers on short scales; the interview decision has three levels. The
  variance-component models treat all scores as continuous.
- Both language-model methods use one model (`gpt-4o-mini`) and one prompt each. They differ in input (Gemini report
  or transcript) and in task (coding a report or rating an answer) at the same time.
- The data have no rater identifiers.
- Five delivery scales of the dataset (speaking skills, confidence, facial expression, overall personality, overall
  performance) are not used: the transcript-based rating has no counterpart for them.

## Sample

| Step | Answers | Persons | Removed |
|---|---|---|---|
| Released | 2,011 | 331 | |
| Retakes removed (latest recording kept) | 1,929 | 331 | 82 |
| Answers of 5 tokens or fewer removed | 1,885 | 328 | 44 |

Answers per person: median 6, range 1 to 13. Answer length: median 60 tokens, range 6 to 219.

## Models and code

- `analysis/variance_models.py`: m0 and m1 for every method and scale (bambi, Gaussian; 4 chains x 2,000 draws; r-hat
  1.00 for all models; 3 divergent transitions, all in TEAS agreeableness).
- `analysis/agreement.py`: agreement between methods.
- `analysis/negative_control.py`: the negative-control table.
- Each script runs on a CSV with the columns listed in it. The answer-level data are not shared (RecruitView is a
  gated dataset; see the repository README).

## References

Gupta, A. K., Sheth, F., Shaikh, H., Kumar, D., Puniya, A., Panwar, D., Chaurasia, S., & Mathur, P. (2025).
*RecruitView: A multimodal dataset for predicting personality and interview performance for human resources
applications* (arXiv:2512.00450). arXiv. https://arxiv.org/abs/2512.00450

Stockdale, K., Hickman, L., & Liu, S. (2026). Scoring employment interviews with large language models: Evaluation
design components, validity investigations, and best practice recommendations. *Journal of Applied Psychology*.
Advance online publication. https://doi.org/10.1037/apl0001396
