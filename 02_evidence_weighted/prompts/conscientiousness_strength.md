You are rating the **signal strength** of evidence of the personality trait **Conscientiousness** from one job-interview answer. You receive the interview question and the evidence units extracted from the answer. You rate only how informative each unit is. You do **not** rate the level of Conscientiousness and you do **not** judge whether the behaviour is high or low.

Judge each unit from its own text only. Do not use the candidate's fluency, vocabulary, length, confidence, or communication style.

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

## What signal strength combines

Signal strength answers: "How informative is this unit for determining whether Conscientiousness was actually manifested?" It combines two things:

**A. Quality of the report.** Is a specific past action described? Is the candidate's own action clear? Is the situation clear? Is the result stated? Is it a pattern over time or a single act?

**B. Typicality of the act for Conscientiousness.** How typical is this kind of act of people high (or low) in Conscientiousness? The following acts are from the Behavioral Indicators of Conscientiousness (Jackson et al., 2010), grouped by how strongly they relate to the trait.

Highly typical acts:
* setting a timeline for getting a project done; finishing a set amount of work before relaxing; completing the projects one starts; working extra hard on a project to make sure it is done right; keeping up with required work;
* in the low direction: putting off work until the last minute; turning in assignments late; missing appointments; forgetting materials for class or work.

Moderately typical acts:
* double-checking one's work; proofreading; completing assignments on time; persisting at tasks after setbacks or failures; using a calendar or planner; making lists and crossing items off; replying to emails on time; organizing work files systematically;
* in the low direction: bypassing a difficult task; doing things on the spur of the moment; waffling when asked to commit to a group project.

Weakly typical acts:
* working overtime; working until physically exhausted; volunteering for work outside one's role.

Acts that mainly show technical skill, the requirements of a task or role, another trait or competency, or interest are weakly informative about Conscientiousness unless the unit also shows one of the behavioural manifestations above.

## Scale

* **5: Very strong.** A specific past episode with the candidate's own action, a highly typical act, and a stated result.
* **4: Strong.** A specific past action that is highly or moderately typical, with the candidate's role clear, but the result or part of the context is missing.
* **3: Moderate.** A concrete action or a regular activity that is only moderately typical, or a typical act described vaguely.
* **2: Weak.** An action that mainly shows something other than Conscientiousness, such as skill, task content or interest; or a vague past action without content.
* **1: Very weak.** A self-description, a general habit without content, an intention, a motivation, or a lesson.
* **0: Not evidence.** The unit describes no act or disposition of Conscientiousness: for example a hobby, an opinion, an achievement with no behaviour behind it, or behaviour that belongs to another trait or competency.

Examples:
* 5: "Our report was due on Friday. On Tuesday I split the remaining work into daily targets, finished my part on Thursday, checked every table, and we submitted on time."
* 4: "Before handing in my thesis chapter, I checked every reference against the original source."
* 3: "For two years I reviewed my lecture notes most evenings."
* 2: "I built a web app with a login page and a database."
* 1: "I never miss a deadline and I like order."
* Strength 5 with low conscientiousness: "I kept postponing my part until the night before, submitted it unchecked, and our team lost marks."

Signal strength is not the trait level: a unit can have strength 5 and show low Conscientiousness, or strength 1 and claim high Conscientiousness. The length of a unit and the amount of technical detail do not raise its strength.

## Output fields

Each numbered line is one unit; one unit can contain several quotes separated by " … ". Return exactly one rating per numbered unit.

For every unit given in the input, in the same order:
* `unit_id`: as given;
* `signal_strength`: 0 to 5;
* `reason`: one concise sentence naming the report quality and the typicality that decided the rating.
