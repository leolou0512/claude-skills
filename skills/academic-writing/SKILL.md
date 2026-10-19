---
name: academic-writing
description: >
  Revise or write technical and scientific prose so it reads as precise academic writing, not
  AI-generated or colloquial text. Covers the recurring tells (everyday verbs for mathematical
  operations, objects given agency, pictures instead of guarantees, paraphrases of named
  concepts, slogans as reasons, spatial metaphors, fillers), what to leave alone, a marked-edit
  workflow that keeps numbers, citations and meaning, and paper-level narrative (launch
  principle, 发布会原则: lead with the strongest advantage, no self-weakening wording). Use
  whenever the user asks to write or restructure an abstract, introduction or conclusion, frame
  results against baselines, polish, restyle, tighten, proofread, "make it sound academic",
  "remove the AI tone", or run a style pass on a paper, SI, caption, rebuttal or report; when a
  co-author or reviewer calls the text colloquial or AI-like; and before handing over any new
  paper prose you wrote, even unasked.
---

# Academic writing

Two layers. The style rules make each sentence precise. The launch principle decides what the
paper argues and in what order. All examples are illustrative.

## What "academic" means here

Precision, not formality. An academic reader already holds a definition for every standard term,
so the exact word is both shorter and clearer than a vivid one. AI-sounding prose fails in a
consistent direction: it narrates mathematics as if objects moved and acted, paints pictures
where a property can be stated, and explains with slogans. The fix is almost always to **name
the thing**: the operation, the object, the quantity, the property the paper already states.

Over-editing is an equal failure. Formal-sounding synonyms, restyled correct sentences and
invented precision all make a text worse. A low edit count on an already technical section is a
correct result.

## The rules, with the reason for each

**Name things exactly.**
- Use the field's verb for an operation: maps, projects, computes, assigns, is expressed in,
  never carries, copies, turns into, gets, ties. The field's verb carries its definition.
- Use the named concept, not a description of it: "invariant under" not "does not change
  under", "eigenvectors" not "the directions the matrix only stretches". A paraphrase is longer
  and only approximately right.
- Name the quantity, not a picture of it: limit, range, adjacent, intermediate, not edge,
  neighbours, in between. The reader otherwise rebuilds the picture to recover the quantity.
- Name the exact object: "number of samples" not "samples", "learning rate" not
  "hyperparameters" when only the learning rate is meant.
- Give every "this", "one", "the set", "it" a referent when more than one thing fits.

**Do not give objects agency or motion.** Variables do not "keep" values, constraints do not
"tie", "see" or "respect", a network does not "look at" its input, a sample does not "receive" a
label. Make the quantity the subject, use the operation's verb, and use the passive when the
actor is the algorithm. Agency language hides what the method computes.

**State the guarantee, not the image.** "so the iteration is a contraction and converges to a
unique fixed point" instead of "so the iterates settle down". The image is unverifiable; the
property is checkable.

**Justify with the stated property, never a slogan.** "We normalise each feature to unit
variance so that the penalty weights all features equally", not "because scale should not
matter". A slogan sounds persuasive and states nothing a referee can check.

**Say which quantity changes and in which direction.** "through a lower recall", not "due to
detection drops". Say what a number is ("the accuracy on the 2,000 test images"), not where it
"comes from". Replace "performance" with the metric.

**Shape sentences for a top-to-bottom reader.** One fact per sentence; split at the second fact.
Claim first, mechanism second. Delete a sentence that restates its neighbour as an image. Make
the actor the subject ("The solver takes 4.2 h to converge", not "Converging takes the solver
4.2 h"). Write "three times as long as", not "three times longer than". Replace phrasal verbs
(switch off, turn on, set up) with the single standard verb (disable, enable, configure). Drop
fillers and idioms (in one shot, on top, anymore, deliberately, of course).

**Stay consistent with the paper itself.** Before choosing a word, grep the paper for where the
concept is defined and reuse that exact phrase. Give each word one meaning (if "scored" means
evaluation elsewhere, do not use it for a loss). A notation table repeats the main text's
definition of each symbol, whatever a general rule prefers. Agree a vocabulary change across the
whole paper before making it in one section.

**Banned constructions** (the usual LLM tells): em dashes and "--"; colons inside prose
sentences; rhetorical semicolons; "While X, Y" openers; "not only ... but also"; "Furthermore"
chains; sentences opening with "Because" or a bare maths symbol; scoreboard words (beats,
outperforms, exceeds X but remains below Y, ranks among, strongest, SOTA); overclaims; delve,
leverage, crucial, pivotal, seamless, notably, underscore, paradigm, novel framework.

## Narrative: the launch principle (发布会原则)

A paper is a product launch, not a progress report. The style rules above decide how each
sentence is worded. These rules decide what the paper argues and in what order.

**Scope.** Apply them in full when writing new prose or restructuring an abstract,
introduction, results discussion or conclusion. In a marked style pass, apply only rule 3 as
marked edits and list violations of the others in the report. Reordering the story, reframing a
comparison or removing an experiment changes meaning, and that is the author's decision.

**1. Build the story around the strongest advantage.** Pick the one result or property that no
baseline matches and organise the abstract, introduction and results around it. Other results
support it. A reader keeps one claim per paper.

**2. Argue, do not narrate the process.** Not "we first tried X, then Y, which failed". Present
the final method and justify each component by what it provides. A failed variant becomes an
ablation stated as a requirement ("Removing the normalisation step lowers accuracy from A% to
B%"), not a story ("Without normalisation, our early attempts failed"). Chronology says what was
done. The argument says why it works.

**3. No self-weakening wording.** Delete "unfortunately", "only" and "merely" as judgements,
"still clearly behind", "limited effect", "fails to". Do not summarise the weaknesses for the
referee. An epistemic hedge is different and stays: "about 0.9 points" and "the likely cause"
qualify how certain a fact is, while "unfortunately" judges the work. Remove the judgement,
never the number.

**4. Do not stage a contest on a metric the method cannot win.** Make the comparison on the
axis the method is designed for (for example a guarantee, cost or data efficiency), and
introduce that axis as the paper's stated objective. Guardrail: the standard benchmark metrics,
computed with their canonical protocol, stay in the tables for every baseline. Changing the
comparison basis means adding a justified axis and applying it to all methods, never removing or
recomputing the standard one.

**5. A result that does not lead is explained, not conceded.** Give the numbers side by side
(pattern 15), then the difference in objective or the trade-off that accounts for the gap, using
a fact the paper states. If the paper states no such reason, flag it. Never invent one.

**6. State every advantage explicitly.** Do not leave the referee to find it in a table. Write
the quantity and the margin ("an accuracy 1.4 points above that of the strongest baseline") or
the property no compared method has. Scoreboard words stay banned. The quantity carries the
claim.

**7. Every experiment has an argumentative job.** For each experiment, write the claim it
supports in one sentence. No claim means propose removing it or moving it to the appendix, and
the author decides. A result that contradicts the main claim has a job: it stays, framed by
rule 5. Removing it would be selective reporting.

**8. Abstract and introduction open like a launch.** Problem, gap in existing methods, the idea,
then the strongest result with its number. No method history and no contribution list before
the gap is clear.

**9. The conclusion reinforces the key points.** Restate the main claim and its strongest
number. Introduce no new weakness in the final paragraph. A limitations section that the venue
requires states the scope the method is designed for and the next step, not an apology.

## What to leave alone

- Accurate plain English. "levels off at 0.3", "a masked entry stays masked", "comes from an
  unmodified copy of the code" are exact. Replacing them is restyling, not correcting.
- Standard jargon that only looks informal: "generates" in the group-theory sense, "emits",
  "mixing coefficients", "wraps around", "clone" in the git sense.
- A word the main text already uses, even if a synonym looks more formal ("falls").
- Wording the author approved, hedged claims and estimates ("a counting error of about 0.9
  points", "the likely cause"). A rewording can shift a hedge. Self-weakening judgements are not
  hedges (launch rule 3).
- Numbers, units, equations, symbols, table values, citations, reference and label targets.
- Anything whose precise version needs a fact the paper does not state. Colloquial wording can be
  fixed from the text alone; vague wording often needs a fact. If the paper lacks it, leave the
  sentence and flag it. Never invent the fact to make a sentence precise.
- Tables may stay telegraphic.

## Workflow

1. **Read the brief before the text.** Read the project's style guide, if one exists. Read any
   co-author comment and write down the general pattern it objects to, so the read is a targeted
   scan rather than a restyle. Decide the expected edit volume (low for a settings or table-heavy
   section).
2. **Work on a snapshot.** Co-authors may be editing the live file. Copy it, record the commit,
   and edit the copy. For a long document, split it into chunks by section and give each chunk to
   a separate agent, each with its own copy and a shared brief.
3. **Scan sentence by sentence.** List every verb, idiom, gloss and paraphrase a referee could
   question. For each, grep the paper for the defined term. Read the code or the equations before
   rewording a mechanism; the wording must follow what is computed.
4. **Edit with a script** that asserts each old string occurs exactly once. Mark every edit:
   `\del{old}\add{new}` on the same line, the smallest changed phrase, or the whole sentence when
   most of it changes. Inside `\del{}` wrap inline maths and every `\cite`/`\ref` in `\mbox{}`
   (ulem breaks otherwise). Never put display maths, `\label`, `\begin`/`\end`, `\item` or
   `\caption` inside a mark; marks go inside a caption's text. Do not add or remove lines.
5. **Verify.** Rejecting every mark must reproduce the original text, and no number, reference,
   citation or label may change (a symbol such as $1 - p$ replacing a phrase adds a "1"; explain
   any such hit). Diff against the snapshot to confirm only the intended lines moved. Reread
   every accepted sentence.
6. **Merge onto the live file.** Pull, then three-way merge (`git merge-file current snapshot
   edited`) so concurrent co-author edits survive. Conflicts next to edited lines are usually a
   co-author's added comment; keep both the edited line and their comment.
7. **Check the revision macros.** If `\add`/`\del` are commented out in the preamble, the marked
   workflow is off: apply the edits as clean text rather than re-enabling the macros. Compile and
   check for undefined references and "??".
8. **Report.** A changelog of `line N: "old" -> "new" (reason, six words or fewer)`, a list of
   phrases considered and left with the reason, and flags for anything that needs the author
   (missing facts, protocol mismatches, missing citations, launch-principle violations that a
   style pass does not fix).

## One-line rules

1. Name the operation, not an everyday action (maps, not carries).
2. Name the exact object (number of samples, not samples).
3. Name the quantity, not a spatial picture (upper limit, not upper edge).
4. Use the field's term for a property instead of describing it.
5. No object acts: make the quantity the subject.
6. State the guarantee, not the image.
7. Justify a choice with the property the paper states, never a slogan.
8. Say which quantity changes and in which direction.
9. One fact per sentence; split at the second fact.
10. Take the exact phrase from where the paper defines the concept.
11. Give "this", "one" and "the set" a referent.
12. Write "N times as long as", never "N times longer than".
13. Leave accurate plain English, approved wording, hedges and numbers alone.
14. If precision needs a fact the paper does not state, flag it; never invent it.
15. Rejecting every mark must give back the original text.
16. Organise the paper around its strongest advantage. Argue, do not narrate the process.
17. Delete self-weakening judgements. Keep epistemic hedges and every number.
18. Compare on the axis the method is designed for. Standard metrics stay, canonical protocol.
19. A result that does not lead: numbers side by side, then the stated reason. Never a concession.
20. Every experiment states the claim it supports. The author decides on removal.
21. Abstract: problem, gap, idea, strongest number. Conclusion: no new weakness.

## Reference

`references/patterns.md` has the full catalogue: sixteen patterns, each with its tell, the rule
and before and after pairs, followed by the judgement calls to leave unchanged and why. Read it
when running a style pass, or when a sentence feels wrong and you want the matching pattern.
