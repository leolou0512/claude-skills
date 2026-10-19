---
name: qu
description: >
  Quick update — the ultra-terse status format for when the user comes back after the
  agent has been working alone for a while. Three fixed headers only: RUNNING /
  RESULTS / NEED YOU. Use when the user says "qu", "/qu", "quick update", "quick status",
  "what's up", "back, anything?", or returns from an absence and asks how it went.
  Also the default register for any unprompted update after a long autonomous
  stretch.
---

# /qu — quick update

The user has been away; they want the state in five seconds. The failure mode is a block of
prose. Caveman register (fragments OK, no filler, no hedging), three headers, done.

## Before writing (≤1 min, no audit)
Refresh from ground truth, not memory: `nvidia-smi`, `pgrep`/`ps`, the run's
`state.txt`/log tail, output files. If a real number takes >1 min to pull, write
"not pulled yet" — never estimate as fact. Heavy digging → subagent, you format.

## Format — exactly this, nothing before or after

```
RUNNING
- <job/run, plain name> — <state>, <progress> — ETA <HH:MMZ or "unknown">
- (nothing) / DEAD: <what>, <cause> — <salvaged / relaunched?>

RESULTS
- <headline number first, exact, with the baseline it beats/misses>
- <link or path to the file>   ← only if a file exists
- (none yet — <why, 5 words>)

NEED YOU
- <the one decision/blocker + who owns it> / (nothing)
```

## Hard rules
- **≤ 10 lines total.** One line per item. No paragraphs. No preamble, no sign-off,
  no "summary" sentence, no headers beyond the three.
- Every section present, even if the content is "(nothing)". Empty ≠ omitted.
- Dead/failed jobs go in RUNNING as `DEAD:` — first bullet of that section. Never
  buried, never softened.
- Numbers exact, in %, with the comparison inline ("12.6% mSUN vs 12.56 stock").
- ETAs absolute clock + Z. Never "soon"/"in a bit".
- Plain names: a run codename gets a 2–4 word gloss in parentheses on first use
  ("`zeroinit_final` (epoch-656 chain)"). No session shorthand, no phase labels.
- NEED YOU holds at most the top 1–2 items. If the user needs to choose, state the
  default you'll take if they say nothing.
- Argument narrows scope: "qu grid" → grid only, same format.
- If they ask a follow-up, answer that one thing in ≤3 lines — do not re-emit the block.

## Example

```
RUNNING
- coord_1p2_lat_1p5_iso (isotropic-noise diffusion) — epoch 412/1000, loss 5.31 — ETA 08-16 03:40Z
- DEAD: eval on node A — OOM at relax stage 04:12Z — relaunched batch 8, ETA 06:30Z

RESULTS
- epoch-656 chain: mSUN 13.1% (327/2500) vs 12.56% stock baseline — raw, pre-relax
- reports/2026-08-15_zeroinit_e656.md

NEED YOU
- Relax numbers land ~06:30Z; if <12.56% I stop the chain unless you say otherwise.
```
