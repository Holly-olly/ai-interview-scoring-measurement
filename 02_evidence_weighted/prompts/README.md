# Prompts

Each file is the instruction text of one stage, exactly as sent with every call of the run. The text hashes to the
prompt hash recorded in the run's call log. The input follows as a second message:

- extraction and zero-shot rating: `Question: <question>` and `Answer: <full answer transcript>`;
- manifestation, evidence check and signal strength: `Question: <question>`, then the numbered evidence units, each as
  the parts of the answer its quotes cover, separated by " … ". These stages do not see the full answer.

The output of every stage is JSON with a fixed schema. Temperature 0.3 throughout.

| File | Stage | Model | Prompt hash | Run |
|---|---|---|---|---|
| `problem_solving_extract.md` | extraction of evidence units | `gpt-4.1` | `60deec77b58d` | `ps_w2` |
| `problem_solving_manifestation.md` | manifestation level of each unit, 1 to 5 (0 = not estimable) | `gpt-4.1` | `ef20cb00062f` | `ps_w2` |
| `problem_solving_check.md` | evidence check of units at level 1 | `gpt-4.1` | `34e357699b60` | `ps_w2` |
| `problem_solving_strength.md` | signal strength of each unit, 0 to 5 | `gpt-4.1-mini` | `e3db1b453628` | `ps_w2` |
| `problem_solving_zeroshot.md` | zero-shot rating of the whole answer, 1 to 5 (0 = not estimable) | `gpt-4.1` | `6d72aa42ef3f` | `ps_zs` |
| `conscientiousness_extract.md` | extraction of evidence units | `gpt-4.1` | `6329d89f42ad` | `consc_w2` |
| `conscientiousness_manifestation.md` | manifestation level of each unit | `gpt-4.1` | `4eb19b331ac3` | `consc_w2` |
| `conscientiousness_strength.md` | signal strength of each unit | `gpt-4.1-mini` | `aa409404e84a` | `consc_w2` |
| `conscientiousness_zeroshot.md` | zero-shot rating of the whole answer | `gpt-4.1` | `2a132ed17f1b` | `consc_zs` |

Problem solving uses the definition, behavioural categories and behaviourally anchored rating scale of Stockdale,
Hickman and Liu (2026), as given to the model in the runs; the zero-shot prompt follows their Def-BARS-1 approach with a
0 (not estimable) option. Conscientiousness uses the project's own definition and behavioural manifestations, with
trait levels after the Behavioral Indicators of Conscientiousness (Jackson et al., 2010). The conscientiousness runs
are shown as prompts only; their results are not published.

Jackson, J. J., Wood, D., Bogg, T., Walton, K. E., Harms, P. D., & Roberts, B. W. (2010). What do conscientious people
do? Development and validation of the Behavioral Indicators of Conscientiousness (BIC). *Journal of Research in
Personality, 44*(4), 501-511. https://doi.org/10.1016/j.jrp.2010.06.005

Stockdale, K., Hickman, L., & Liu, S. (2026). Scoring employment interviews with large language models: Evaluation
design components, validity investigations, and best practice recommendations. *Journal of Applied Psychology*.
Advance online publication. https://doi.org/10.1037/apl0001396
