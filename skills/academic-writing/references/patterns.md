# Pattern catalogue

Each pattern gives the tell (why an academic reader flags it), the rule, and illustrative
before and after pairs.

Contents
1. Everyday verbs for mathematical operations
2. Objects given agency or motion
3. A picture instead of the guarantee
4. Paraphrase of a concept that has a name
5. Lab slang for standard operations and objects
6. Spatial metaphors for quantities
7. Slogans and loose causal glosses
8. Vague outcome and provenance words
9. Conversational openers, idioms and fillers
10. Descriptions that name a nearby object
11. Missing referents
12. A category word where the members are known
13. A defined term reused for another quantity
14. Sentence shape
15. Scoreboard phrasing
16. Imprecise quantities in formulas
Judgement calls: what to leave alone

---

## 1. Everyday verbs for mathematical operations

**Tell.** A verb for handling a physical object (carry, copy, turn into, get, share, pass
through) where the text means a defined operation. It reads as narration, and the reader has to
guess which operation is meant.
**Rule.** Use the verb the field defines: maps, projects, computes, assigns, expresses in,
leaves unchanged.

- "the vector that $A$ carries onto $\mathbf{y}$" -> "the vector that $A$ maps onto $\mathbf{y}$"
- "coordinates carried into the new basis" -> "coordinates expressed in the new basis"
- "copied to the other entries of the block" -> "assigned to the other entries of the block"
- "turns the residual into a correction" -> "computes a correction from the residual"

## 2. Objects given agency or motion

**Tell.** Variables, constraints, networks or samples act ("keep", "draw", "tie", "receive",
"respects", "sees"). It hides what the algorithm does and who does it.
**Rule.** Make the quantity the subject. Use the operation's verb. Use the passive when the actor
is the algorithm.

- "the fixed entries keep their values" -> "the fixed entries are held constant"
- "Each cluster draws one label from the averaged scores." -> "The label of each cluster is sampled from the averaged scores and assigned to all its members."
- "Parameters that the constraint ties together receive the same update" -> "The same update is applied to all parameters that the constraint requires to be equal"
- "which is all the network sees" -> "which is the only input to the network"

## 3. A picture instead of the guarantee

**Tell.** An intuitive image ("settle down", "move together", "passes through") replaces a
property that can be stated exactly. The image cannot be checked.
**Rule.** State what the operator guarantees, in the paper's terms.

- "so the iterates settle down" -> "so the iteration is a contraction and converges to a unique fixed point"
- "A vector that already respects the constraint passes through the projection unchanged." -> "The projection leaves unchanged any vector that already satisfies the constraint."

## 4. Paraphrase of a concept that has a name

**Tell.** A description of a standard object instead of its name, longer and only approximately
right.
**Rule.** Use the field's term, preferably one the paper already uses.

- "does not change under rotation or reordering of the inputs" -> "is invariant under rotation and permutation of the inputs"
- "the distribution the chain settles into" -> "the stationary distribution of the chain"
- "the directions the matrix only stretches" -> "the eigenvectors of the matrix"

## 5. Lab slang for standard operations and objects

**Tell.** Workshop words ("fresh noise", "a draw", "blew up", "switch off") where the reader
knows a standard term. Phrasal verbs for the state of a setting read as spoken lab talk.
**Rule.** Use the standard term, the same one the rest of the document uses. Replace a phrasal
verb with the single standard verb.

- "inject fresh noise" -> "add newly sampled noise"
- "a new draw from the prior" -> "a new sample from the prior"
- "we threw out runs that blew up" -> "we excluded runs in which the loss diverged"
- "so we switched it off during evaluation" -> "so we disabled it during evaluation"

## 6. Spatial metaphors for quantities

**Tell.** Edge, neighbours, in between: a picture the reader must rebuild to recover the
quantity.
**Rule.** Name the quantity: limit, range, adjacent, intermediate.

- "the upper edge of the labels" -> "the upper limit of the label range"
- "together with its neighbours" -> "together with the adjacent frequency bands"
- "peaks in between" -> "peaks at intermediate values"

## 7. Slogans and loose causal glosses

**Tell.** A "because" or "or else" clause that explains with a slogan. It sounds persuasive and
states nothing checkable.
**Rule.** State the concrete property the paper itself gives as the reason.

- "We normalised deliberately, because scale should not matter." -> "We normalise each feature to unit variance so that the penalty weights all features equally."
- "Each row must sum to one, or the matrix breaks." -> "Each row must sum to one for the matrix to be a stochastic matrix."
- "to preserve symmetry" -> "so that the operator remains self-adjoint"

## 8. Vague outcome and provenance words

**Tell.** "covered", "erases", "drops", "comes from", "gives", "performance" point at a result
without naming it.
**Rule.** Name the quantity and the direction of change. Say what a number is. Use the metric's
name.

- "mainly due to detection drops" -> "mainly through a lower recall"
- "Measured accuracy comes from 2,000 test images" -> "Measured accuracy is the rate on the 2,000 test images"
- "The encoder gives a code" -> "The encoder produces a code"
- "although performance remains below the baseline" -> "although the F1 score remains below that of the baseline"

## 9. Conversational openers, idioms and fillers

**Tell.** A spoken aside that gives an attitude, not a fact ("Whatever ...", "Of course"), or
spoken English ("in one shot", "on top", "anymore", "deliberately").
**Rule.** State the fact and its condition literally. Delete fillers.

- "Whatever the initialisation says, the bias terms are set to zero" -> "The bias terms are set to zero independently of the initialisation"
- "in one shot" -> "in a single step"
- "already visited states will not switch anymore" -> "since a visited state does not change in later iterations"

## 10. Descriptions that name a nearby object

**Tell.** The description is close to the symbol but not exactly it: a count described as a set,
an index as the thing it indexes, an adjective on the wrong noun.
**Rule.** Check each description against the definition and name the exact object.

- "Samples in the batch" -> "Number of samples in the batch"
- "Class; its prior" -> "Index of a class; its prior probability"
- "a small regularisation term" -> "a regularisation term with a small weight"
- "the likelihood integrated over $\theta$" -> "the likelihood integrated over the prior on $\theta$"

## 11. Missing referents

**Tell.** "this", "one", "the set", "the head", a bare "the median": several candidates fit.
**Rule.** Replace the pronoun with its noun and reuse the paper's component names.

- "over the set" -> "over the validation set"
- "the median for each target" -> "the median predicted value for each target"
- "from the head" -> "from the classification head"
- "the softmax of the previous logits" -> "the softmax of the logits at the previous step"

## 12. A category word where the members are known

**Tell.** "hyperparameters" when only two of them are ever meant.
**Rule.** Name the exact set.

- "the hyperparameters were tuned" -> "the learning rate and batch size were tuned"

## 13. A defined term reused for another quantity

**Tell.** A phrase the paper reserves for one quantity names a neighbouring one, or a word has a
second meaning elsewhere in the paper.
**Rule.** Find where the paper defines a phrase before reusing it. Give each word one meaning.

- "predicts an update $\hat{\mathbf{d}}$" -> "predicts the search direction $\hat{\mathbf{d}}$" (the paper calls the step itself the update)
- "The prediction is scored against the target." -> "The loss is computed between the prediction and the target." ("scored" means evaluation elsewhere)
- "$\lambda = 0$ is the unregularised model" -> "$\lambda = 0$ recovers the unregularised model"

## 14. Sentence shape

**Tell.** Two facts in one sentence; an "X but not Y" line that restates its neighbour as an
image; the activity as subject; loose comparatives; hard-to-parse reduced relatives.
**Rule.** Split at the second fact. Delete a restatement. Put the actor first. Write "N times as
long as" (strictly, "N times longer than" means N + 1). Use "as X decreases" for a trend.

- "no retraining, and inference is about $10^3$ times cheaper" -> "no retraining. Inference is about $10^3$ times cheaper"
- "The dataset, built from two public archives, has 60,000 images" -> "The dataset is built from two public archives. It has 60,000 images"
- Deleted: "The projection removes dimensions but not the Gaussian character of the noise."
- "Training takes the model 17.4 h, about three times longer than the baseline" -> "The model takes 17.4 h to train, about three times as long as the baseline"
- "With each step down in $\gamma$," -> "As $\gamma$ decreases,"
- "the logits the network predicted for the token" -> "the logits predicted for the token"

## 15. Scoreboard phrasing

**Tell.** Ranking verbs and "exceeding X but remaining below Y" turn a measurement into a
contest.
**Rule.** Give the numbers side by side and let them speak.

- "our method achieves 86.4% accuracy, exceeding Baseline A's 85.0% but remaining below Baseline B's 91.2%" -> "our method achieves 86.4% accuracy, compared with 85.0% for Baseline A and 91.2% for Baseline B"
- "and ranks among the highest for precision and recall" -> "and its precision and recall are among the highest"

## 16. Imprecise quantities in formulas

**Tell.** A descriptive phrase for a quantity the paper has a symbol for, which a reader can
misread as a different quantity.
**Rule.** Use the symbol when it is already defined.

- "with the decay factor clipped at 0.999" -> "with $\beta$ clipped at 0.999"

---

## Judgement calls: what to leave alone

Over-editing is a failure. Leave these unchanged.

- **Standard terms that look informal.** "generates" (group theory), "emits" (automata),
  "mixing coefficients", a mean that "drifts", "wraps around" (periodic boundaries), "clone" (a
  git checkout at a named commit). Replacing expected jargon makes text less clear.
- **Accurate plain English.** "levels off at 0.3", "a masked entry stays masked", "runs from
  0.005", "comes from an unmodified copy of the code", "global batch of 128". The test is whether
  a verb gives an object intent or paints an image. These do neither.
- **The paper's own words.** "falls" (when the main text writes "accuracy falls to 60%"). Keep a
  word the paper already uses, even if a synonym looks more formal.
- **A symbol's definition in a notation table.** If the main text defines a symbol as "class
  label", the table says "class label", not a more formal synonym. The table must match.
- **Approved wording.** Sentences the author approved word for word stay unless a word in them is
  clearly colloquial. Approval outranks a borderline taste call.
- **Hedges and estimates.** "a counting error of about 0.9 points", "the likely cause of the low
  score". A rewording can shift the hedge.
- **Missing facts.** "physically plausible" is vague, but if the thresholds are not in the paper,
  flag it rather than fix it. Do not give a step a technical name the paper never uses. Do not
  introduce "idempotent" for "leaves unchanged", because it adds a claim. Do not reword a
  mechanism you could not check in the code.
- **Tables and specification sections.** Telegraphic table entries ("Learning-rate schedule,
  cosine") are fine. A settings section can legitimately need two edits in a hundred lines.
