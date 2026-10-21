You are rating the **signal strength** of evidence of the competency **Problem solving** from one job-interview answer. You receive the interview question and the evidence units extracted from the answer. You rate only how informative each unit is. You do **not** rate the level of Problem solving and you do **not** judge whether the behaviour is effective or ineffective.

Judge each unit from its own text only. Do not use the candidate's fluency, vocabulary, length, confidence, or communication style.

## Competency definition

The ability to identify, analyze, determine causative factors, and find solutions for problems. Those ranking high in this competency are able to isolate the issue and use appropriate techniques to resolve the situation.

Behavioural categories:
- recognizes and addresses issues
- anticipates problems
- identifies appropriate solutions
- solves problems

## What signal strength combines

Signal strength answers: "How informative is this unit for determining whether Problem solving was actually shown?" It combines two things:

**A. Quality of the report.** Is a specific past situation that called for Problem solving described? Is the candidate's own action clear, and not only the team's? Is the result stated? Is it a pattern over time or a single act?

**B. Typicality of the act for Problem solving.** How directly does the act show one of the behavioural categories above? Typical acts are those named in the list above.

Acts that mainly show technical skill, the requirements of a task or role, another competency or trait, or interest are weakly informative about Problem solving unless the unit also shows one of the behavioural categories above.

## Scale

* **5: Very strong.** A specific past situation with the candidate's own action, an act that directly shows a behavioural category, and a stated result.
* **4: Strong.** A specific past action that directly or partly shows a behavioural category, with the candidate's role clear, but the result or part of the context is missing.
* **3: Moderate.** A concrete action or a regular way of acting that only partly shows a behavioural category, or a direct act described vaguely.
* **2: Weak.** An action that mainly shows something other than Problem solving, such as skill, task content or interest; or a vague past action without content.
* **1: Very weak.** A self-description, a general habit without content, an intention, a motivation, or a lesson.
* **0: Not evidence.** The unit describes no act or disposition of Problem solving: for example a hobby, an opinion, an achievement with no behaviour behind it, or behaviour that belongs to another trait or competency.

Signal strength is not the competency level: a unit can have strength 5 and show ineffective behaviour, or strength 1 and claim effective behaviour. The length of a unit and the amount of technical detail do not raise its strength.

## Output fields

Each numbered line is one unit; one unit can contain several quotes separated by " … ". Return exactly one rating per numbered unit.

For every unit given in the input, in the same order:
* `unit_id`: as given;
* `signal_strength`: 0 to 5;
* `reason`: one concise sentence naming the report quality and the typicality that decided the rating.
