# Pattern catalogue

Every pair below is a real edit from supplementary-information passes.
Each pattern gives the tell (why an academic reader flags it), the rule, and the pairs.

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
Judgement calls: what was deliberately left alone

---

## 1. Everyday verbs for mathematical operations

**Tell.** A verb for handling a physical object (carry, copy, turn into, get, share, pass
through) where the text means a defined operation. It reads as narration, and the reader has to
guess which operation is meant.
**Rule.** Use the verb the field defines: maps, projects, computes, assigns, expresses in,
leaves unchanged.

- "the atom that $g$ carries onto site $j$" -> "the atom that $g$ maps onto site $j$"
- "Clean coordinates carried into the noisy cell" -> "Clean coordinates expressed in the noisy cell"
- "copied to the other atoms of the orbit" -> "mapped to the other atoms of the orbit"
- "turns the deformation into ... the noise it implies" -> "computes the predicted clean cell ... then the predicted lattice noise"

## 2. Objects given agency or motion

**Tell.** Atoms, orbits, constraints or crystals act ("keep", "draw", "tie", "receive",
"enters", "respects", "sees"). It hides what the algorithm does and who does it.
**Rule.** Make the quantity the subject. Use the operation's verb. Use the passive when the actor
is the algorithm.

- "the atoms keep their fractional coordinates" -> "the fractional coordinates of the atoms are held fixed"
- "Each revealed orbit draws one species for all its atoms from the orbit-averaged logits." -> "The element of each newly unmasked orbit is sampled from the orbit-averaged logits and assigned to all atoms of the orbit."
- "Parameters that the crystal system ties together receive the same noise component, and angles it fixes receive none" -> "It assigns the same noise component to all cell lengths that the crystal system constrains to be equal, and zero noise to all angles that the crystal system fixes."
- "Each crystal receives this prediction as $\pi$ with probability 0.5" -> "For each crystal, $\pi$ is set to this prediction with probability 0.5"
- "which is all the network sees" -> "which is the only input to the network"

## 3. A picture instead of the guarantee

**Tell.** An intuitive image ("move together", "stay on", "passes through") replaces a property
that can be stated exactly. The image cannot be checked.
**Rule.** State what the operator guarantees, in the paper's terms.

- "so equivalent atoms move together and stay on their Wyckoff sites" -> "so the displacements of symmetry-equivalent atoms are related by the space-group operations and every atom remains on its Wyckoff site"
- "A perturbation that already respects the crystal system passes through the projection unchanged." -> "The projection leaves unchanged any perturbation that already satisfies the constraints of the crystal system."

## 4. Paraphrase of a concept that has a name

**Tell.** A description of a standard object instead of its name, longer and only approximately
right.
**Rule.** Use the field's term, preferably one the paper already uses.

- "does not change under rotation, translation or reordering of the atoms" -> "is invariant under rotation, translation and permutation of the atoms"
- "the symmetry operations that leave the orbit's representative atom in place" -> "the site-symmetry group of the orbit's representative atom"
- "measured the shortest way round the periodic cell" -> "measured to the nearest periodic image"
- "two orbits on a fixed position would overlap" -> "two orbits of a Wyckoff position without free parameters would occupy the same sites"
- "these sites hold 9.1% of the atoms" -> "these sites are occupied by 9.1% of the atoms"

## 5. Lab slang for standard operations and objects

**Tell.** Workshop words ("fresh noise", "draw", "reveal", "switch off", "generations") where
the reader knows a standard term. Phrasal verbs for the state of a setting read as spoken lab
talk.
**Rule.** Use the standard term, the same one the rest of the document uses. Replace a phrasal
verb with the single standard verb.

- "inject fresh noise" -> "add newly sampled noise"
- "reveal each masked orbit" -> "unmask each masked orbit"
- "Standard normal draw for the lattice noise" -> "Standard normal vector for the lattice noise"
- "so we switched it off when computing the stability metrics" -> "so we disabled it when computing the stability metrics"
- "the insulating generations" -> "the insulating structures"

## 6. Spatial metaphors for quantities

**Tell.** Edge, neighbours, in between: a picture the reader must rebuild to recover the
quantity.
**Rule.** Name the quantity: limit, range, adjacent, intermediate.

- "the upper edge of the labels" -> "the upper limit of the label range"
- "together with its neighbours" -> "together with the adjacent bands"
- "peaks in between" -> "peaks at intermediate values"

## 7. Slogans and loose causal glosses

**Tell.** A "because" or "or else" clause that explains with a slogan. It sounds persuasive and
states nothing checkable.
**Rule.** State the concrete property the paper itself gives as the reason.

- "We chose Cartesian coordinates deliberately, because the chemistry is set by distances in Ångström." -> "We diffuse Cartesian coordinates so that the noise scale is a real-space distance in Ångström."
- "All atoms of an orbit must carry the same species, or the crystal loses its space group." -> "All atoms of a Wyckoff orbit must be of the same element for the crystal to be invariant under the operations of its space group."
- "to preserve symmetry" -> "so that the crystal retains its space group"

## 8. Vague outcome and provenance words

**Tell.** "covered", "erases", "drops", "comes from", "gives", "performance" point at a result
without naming it.
**Rule.** Name the quantity and the direction of change. Say what a number is. Use the metric's
name.

- "mainly due to stability drops" -> "mainly through a lower metastable fraction"
- "so it needs more noise to be covered" -> "so a larger noise scale is needed for the wrapped noise distribution to become uniform along such a line"
- "Measured mSUN comes from 2,500 new structures" -> "Measured mSUN is the rate among 2,500 new structures"
- "The template VAE gives a cubic template" -> "The template VAE produces a cubic template"
- "although performance remains below Chemeleon 2" -> "although mSUN remains below that of Chemeleon 2"

## 9. Conversational openers, idioms and fillers

**Tell.** A spoken aside that gives an attitude, not a fact ("Whatever ...", "Of course"), or
spoken English ("in one shot", "on top", "anymore", "deliberately").
**Rule.** State the fact and its condition literally. Delete fillers.

- "Whatever the prior says, constrained angles are set to exactly 90° or 120°" -> "Angles fixed by the crystal system are set to exactly 90° or 120° independently of the prior"
- "in one shot" -> "directly from the clean cell"
- "already unmasked atoms will not switch states anymore" -> "since an unmasked orbit does not change state in the reverse process"

## 10. Descriptions that name a nearby object

**Tell.** The description is close to the symbol but not exactly it: a count described as a set,
an index as the thing it indexes, an adjective on the wrong noun.
**Rule.** Check each description against the definition and name the exact object.

- "Atoms in the cell" -> "Number of atoms in the cell"
- "Periodic image; its wrapped-normal weight" -> "Index of a periodic image; its wrapped-normal weight"
- "a small cross-entropy term" -> "an auxiliary cross-entropy term with a small weight"
- "the decoder marginalised over $\mathbf{z}$" -> "the decoder marginalised over the prior on $\mathbf{z}$"

## 11. Missing referents

**Tell.** "this", "one", "the set", "the head", a bare "the median": several candidates fit.
**Rule.** Replace the pronoun with its noun and reuse the paper's component names.

- "where one was run" -> "where such a set exists"
- "over the set" -> "over the fine-tuning set"
- "the median for each target" -> "the median predicted permittivity for each target"
- "from the head" -> "from the space-group MLP"
- "the softmax of the previous logits" -> "the softmax of the logits at the previous step"

## 12. A category word where the members are known

**Tell.** "parameters" when only cell lengths are ever meant.
**Rule.** Name the exact set.

- "Parameters that must be equal" -> "Cell lengths constrained to be equal"

## 13. A defined term reused for another quantity

**Tell.** A phrase the paper reserves for one quantity names a neighbouring one, or a word has a
second meaning elsewhere in the paper.
**Rule.** Find where the paper defines a phrase before reusing it. Give each word one meaning.

- "predicts a coordinate update $\hat{\mathbf{s}}_\theta$" -> "predicts the scaled coordinate target $\hat{\mathbf{s}}_\theta$" (the main text calls the step itself the coordinate update)
- "The lattice head's prediction is scored as a noise estimate." -> "The lattice loss is computed on the noise estimate implied by the prediction of the lattice readout." ("scored" means evaluation elsewhere)
- "$\gamma_{\mathrm{g}} = 1$ is the conditional model" -> "$\gamma_{\mathrm{g}} = 1$ recovers the conditional model"

## 14. Sentence shape

**Tell.** Two facts in one sentence; an "X but not Y" line that restates its neighbour as an
image; the activity as subject; loose comparatives; hard-to-parse reduced relatives.
**Rule.** Split at the second fact. Delete a restatement. Put the actor first. Write "N times as
long as" (strictly, "N times longer than" means N + 1). Use "as X decreases" for a trend.

- "no retraining, and template sampling is about $10^3$ times cheaper" -> "no retraining. Template sampling is about $10^3$ times cheaper"
- "Alex-MP-20, built from the Materials Project and Alexandria, has 607,683 ..." -> "Alex-MP-20 is built from the Materials Project and Alexandria. It has 607,683 ..."
- Deleted: "The projection removes degrees of freedom but not the Gaussian character of the noise."
- "Generating 2,500 structures takes our method 17.4 h, about three times longer than MatterGen" -> "Our method takes 17.4 h to generate 2,500 structures, about three times as long as MatterGen"
- "With each step down in $\gamma$," -> "As $\gamma$ decreases,"
- "the type logits the denoiser predicted for the atom" -> "the type logits predicted for the atom"
- "the templates ... take about two minutes" -> "sampling the templates ... takes about two minutes"

## 15. Scoreboard phrasing

**Tell.** Ranking verbs and "exceeding X but remaining below Y" turn a measurement into a
contest.
**Rule.** Give the numbers side by side and let them speak.

- "our relaxed method achieves an mSUN rate of 16.40%, exceeding MatterGen's 15.0% but remaining below Crystalite's 22.6%" -> "Our method achieves an mSUN rate of 16.40% after relaxation, compared with 15.0% for MatterGen and 22.6% for Crystalite"
- "and ranks among the highest for validity and uniqueness" -> "and its validity and uniqueness are among the highest"

## 16. Imprecise quantities in formulas

**Tell.** A descriptive phrase for a quantity the paper has a symbol for, which a reader can
misread as a different quantity.
**Rule.** Use the symbol when it is already defined.

- "with the single-step coefficient clipped at 0.999" -> "with $1 - \alpha_t$ clipped at 0.999"

---

## Judgement calls: what was deliberately left alone

Over-editing is a failure. These were considered and kept, with the reason.

- **Standard terms that look informal.** "generates" (group theory), "emits" letters, "mixing
  coefficients", a mean that would "drift", "takes the DDPM mean step", "Gaussian latent",
  "implied clean cell", "wrap", "smear", "corruption path", "unmodified clone" (a git checkout at
  a named commit). Replacing expected jargon makes text less clear.
- **Accurate plain English.** "levels off at 3.6 Å", "a masked orbit stays masked", "runs from
  0.005", "come from an unmodified clone", "Three linear heads give the outputs", "follow the
  prior within the bands", "global batch of 128". The test is whether a verb gives an object
  intent or paints an image. These do neither.
- **The paper's own words.** "falls" (the main text writes "validity falls to 60%"), "reachable
  periodic copies". Keep a word the paper already uses, even if a synonym looks more formal.
- **A symbol's definition in a notation table.** Changing "species" to "atom types" was reverted
  because the main text defines the symbol as "atomic species". The table must match.
- **Approved wording.** Sentences the author approved word for word stay unless a word in them is
  clearly colloquial. Approval outranks a borderline taste call.
- **Hedges and estimates.** "a counting error of about 0.9 points", "the likely cause of the low
  validity". A rewording can shift the hedge.
- **Missing facts.** "physically plausible density and cell" is vague, but the thresholds are not
  in the paper, so it was flagged, not fixed. The DiffCSP++ correction step was not renamed
  "Langevin" because the paper never says so. "idempotent" was not introduced for "leaves
  unchanged", because it adds a claim. An attention mechanism that could not be checked in the
  code was not reworded.
- **Tables and specification sections.** Telegraphic table entries ("Lattice schedule, variance
  preserving") are fine. A settings section can legitimately need two edits in a hundred lines.
