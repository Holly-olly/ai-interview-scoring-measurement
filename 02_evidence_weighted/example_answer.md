# One answer through the pipeline

One RecruitView answer (Gupta et al., 2025), scored for problem solving and for conscientiousness. The prompts of every
step are in `prompts/`.

**Question.** Can you give an example of a time when you had to take the initiative to solve a problem without being
asked?

**Answer.** When we were working on a group project, we had faced some issues integrating our code modules into a
cohesive project. So no one was directly responsible to fix it. So I took the initiative step to set up a version
control system to reduce code conflicts. I constantly checked up with my teammates for any other issues.

## Problem solving

**Extraction** finds two units of evidence:

| Unit | Type | Behavioural categories | What the rating stages see |
|---|---|---|---|
| 1 | episode | recognizes and addresses issues; identifies appropriate solutions | "we had faced some issues integrating our code modules into a cohesive project … no one was directly responsible to fix it … I took the initiative step to set up a version control system to reduce code conflicts" |
| 2 | routine | anticipates problems | "I constantly checked up with my teammates for any other issues" |

**Manifestation and signal strength** are rated separately, each without the other:

| Unit | Manifestation (BARS, 1 to 5) | Signal strength (0 to 5) | Reason given for the strength |
|---|---|---|---|
| 1 | 5 | 5 | Specific past situation with clear candidate action showing problem recognition and solution implementation, directly illustrating problem solving with a stated result. |
| 2 | 3 | 2 | The unit describes a general action related to monitoring for issues but lacks a specific problem-solving situation or clear personal initiative. |

**Answer score:** (5 x 5 + 3 x 2) / (5 + 2) = **4.43**.

**Zero-shot rating of the whole answer** (same definition and BARS, one number): **3**.

## Conscientiousness

The same answer read for conscientiousness gives the same two pieces of behaviour, labelled with conscientiousness
manifestations:

| Unit | Type | Manifestation | Level | Reason given for the level | Strength |
|---|---|---|---|---|---|
| 1 | episode | planning and organizing work | 4 | The candidate implemented a version control system, adding organizational structure beyond what was required. | 4 |
| 2 | routine | monitoring progress | 4 | Regularly checking with teammates for issues shows monitoring and organization beyond what was required. | 2 |

**Answer score:** (4 x 4 + 4 x 2) / (4 + 2) = **4.0**. **Zero-shot rating:** **4**.

The episode is strong evidence for both constructs (strength 5 and 4). The routine is weak evidence for both
(strength 2): it names a habit without a situation. Its level differs by construct: 3 for problem solving, 4 for
conscientiousness.

Gupta, A. K., Sheth, F., Shaikh, H., Kumar, D., Puniya, A., Panwar, D., Chaurasia, S., & Mathur, P. (2025).
*RecruitView: A multimodal dataset for predicting personality and interview performance for human resources
applications* (arXiv:2512.00450). arXiv. https://arxiv.org/abs/2512.00450
