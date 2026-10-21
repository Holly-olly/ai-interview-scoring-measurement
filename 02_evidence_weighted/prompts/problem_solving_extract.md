# Evidence Extraction: Problem solving

## Objective

Extract evidence relevant to the competency **Problem solving** from the candidate's interview answer. You do not rate anything.

### Competency definition

The ability to identify, analyze, determine causative factors, and find solutions for problems. Those ranking high in this competency are able to isolate the issue and use appropriate techniques to resolve the situation.

The competency shows in what the candidate did, or regularly does, in situations that call for it. Relevant behavioural manifestations may include:
- recognizes and addresses issues
- anticipates problems
- identifies appropriate solutions
- solves problems

The competency has two poles. Ineffective behaviour is evidence too: ignoring or not recognizing a problem, not looking for its cause, taking no action to resolve it, leaving it to others.

Not evidence of Problem solving: completing an ordinary task where no problem arose, technical knowledge or tools named without a problem they were used to solve, a successful outcome with no description of how the problem was handled.

## What a unit is

A unit is one independent piece of evidence of Problem solving or of its opposite pole. There are three kinds:

- `episode`: one specific past occasion in which the candidate did something that shows Problem solving or its opposite. Everything about that occasion is ONE unit: what happened, what the candidate did, the difficulty met, the result. The steps of one occasion are never separate units. Two different occasions are two units.
- `routine`: one thing the candidate regularly does that shows Problem solving or its opposite. Different regular practices are different units.
- `claim`: what the candidate says about themselves in general, with no occasion and no concrete regular practice.

How many units: one per occasion, one per regular practice, and for claims one unit per pole.

## Two poles

Evidence of the strong side and evidence of the weak side are never in the same unit when they are separate statements about the candidate: a strength and a weakness, or how the candidate was before and how they are now. If one sentence contains both, cut the sentence and give each part its own unit.
Pattern: "I am good at A, but I struggle with B" gives two units, one quoting "I am good at A", the other quoting "I struggle with B".
Inside one episode, a difficulty or hesitation that the candidate then dealt with stays in that episode.

## Not a unit

- an outcome, a result or other people's reaction on its own;
- beliefs or opinions about Problem solving in general ("it is important", "everyone needs it"), advice, or what "one should" do: a claim must say what the candidate does or is like;
- topics, interests, aspirations, job titles, achievements with no behaviour of the candidate;
- behaviour of other people only;
- a statement that the candidate has no example or never met such a situation: having nothing to tell is not evidence of the opposite pole;
- general reasoning about people ("you", "a person", "one") that says nothing about what the candidate does.
If the answer has no evidence, return an empty list.

## Quotes

Quote only the parts of the answer that carry the evidence: exact, continuous excerpts in their original order. A quote may be a part of a sentence. No paraphrase, no corrected grammar, no "...", no words left out inside a quote. A part of the answer belongs to one unit only.

Do not rate, score or judge the evidence, and do not add anything the candidate did not say.

## Output fields

For each unit, in this order:
- `evidence`: a concise, neutral description of the evidence in your own words, not a copy of the quote;
- `type`: `episode`, `routine` or `claim`;
- `markers`: the one behavioural manifestation from the list above that the quotes state most directly, in the wording of the list; add a second only if the quotes state it separately; for evidence of the opposite pole write `opposite pole`; an empty list if none is stated;
- `quotes`.
