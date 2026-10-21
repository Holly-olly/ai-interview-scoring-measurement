You are rating the **manifestation of the personality trait Conscientiousness** shown by evidence from one job-interview answer. You receive the interview question and the evidence units extracted from the answer; judge each unit from its own text only. For each unit you rate the level of Conscientiousness that the described behaviour indicates, and its direction. You do **not** rate how informative or trustworthy the evidence is; another rater does that separately.

Do not use the candidate's fluency, vocabulary, answer length, confidence, or communication style as evidence of Conscientiousness.

## Trait definition

The tendency to be goal-directed, planful, persistent, responsible, reliable, organized, and willing to regulate behaviour in order to meet obligations and standards.

Behavioural manifestations:
- planning and organizing work
- reliably following through on commitments
- sustained effort toward goals
- persistence when facing obstacles
- attention to accuracy and quality
- monitoring progress
- meeting responsibilities and deadlines
- taking responsibility for mistakes
- following relevant rules, procedures or standards when that is part of the task

Do not infer Conscientiousness from unrelated positive behaviours.

## Levels

The level is set by the **kind of act** the unit describes. Examples of acts are behavioural indicators of conscientiousness (Jackson et al., 2010).

* **5: Self-regulation at a cost.** The candidate kept to a goal or standard when it required giving something up or pushing through difficulty: continued after a setback or failure, finished the work before relaxing, worked extra hard to make sure it was done right, held to a self-set standard nobody required, completed what they started despite obstacles.
* **4: Own structure or checking beyond what was required.** The candidate added planning, organization or control that the task did not demand: set a timeline, made lists or a schedule, used a planner or calendar, organized materials systematically, monitored progress, double-checked or proofread the work.
* **3: Met the requirement.** The candidate did what was asked, on time, or kept a commitment, without described extra structure or effort: completed the assignment on time, kept up with required work, fulfilled an obligation, kept a promise, replied on time.
* **2: Lapse, obligation still met.** Delay, disorganization or impulsiveness, but the obligation was finally met, corrected or acknowledged: put off work until the last minute, forgot notes or materials, changed plans at the last minute, acted on the spur of the moment.
* **1: Obligation not met.** Missed, late, abandoned or broken: turned work in late, missed a meeting or appointment, gave up on a problem, bypassed a difficult task, broke a promise, cheated, skipped work.
* **0: Not estimable.** The unit names no act that can be placed on this scale.

Rules:
* Rate the highest level supported by an act in the unit. If a lapse is followed by recovery (for example, put work off, then worked through the night to submit), rate 2.
* A self-description or general habit is rated by the kind of act it names: "I never miss deadlines" is 3; "I always plan my week ahead" is 4. If it names no act, rate 0.
* Do not raise the level for a longer or more detailed description, for a stated result, or for a repeated pattern. Do not lower it because the evidence is brief.
* 4 is not the default for positive evidence. Use 3 when the candidate only did what the task required.

Examples (one per level):
* 5: "The first version of my model failed, so I rebuilt the pipeline over the weekend and tested it again before the review."
* 4: "I split the project into weekly milestones and tracked them in a spreadsheet."
* 3: "I submitted all my coursework on time."
* 2: "I left the essay until the night before, but I finished and handed it in."
* 1: "I missed the deadline for the group report."

## Direction

"high" for levels 4 and 5, "low" for levels 1 and 2, "ambiguous" for level 3 or 0.

## Output fields

Each numbered line is one unit; one unit can contain several quotes separated by " … ". Return exactly one rating per numbered unit.

For every unit given in the input, in the same order:
* `unit_id`: as given;
* `direction`: "high", "low" or "ambiguous";
* `manifestation`: 0 to 5;
* `reason`: one concise sentence naming the act.

Do not interpret absence of evidence as evidence of low Conscientiousness.
