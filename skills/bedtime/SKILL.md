---
name: bedtime
description: >
  Overnight autonomy protocol — the user is going to sleep and the agent must keep working
  unsupervised: keep the GPUs busy with the most valuable experiment it can justify,
  chain the next job when one finishes, and have a report ready when they wake. Use when
  the user says "bedtime", "/bedtime", "going to bed", "good night", "gn", "sleeping now",
  "keep going overnight", or "don't let the GPUs idle". Not for short absences ("back
  in an hour") — that is normal away mode.
---

# /bedtime — overnight autonomy

The user sleeps ~7–8 h. The failure to avoid: they wake and nothing happened. Second failure:
compute burned on something pointless. Third: an in-session watcher that died with the
session at 02:00 and left the GPUs idle. Design against all three, in that order.

## 1. Acknowledge (≤ 4 lines, no questions)
The user is leaving. Do not ask anything. State: what runs now, what you will do overnight
(the picked item + fallback), where the morning report will be. If a decision is
genuinely theirs, take the default that keeps compute busy and reversible, name the
assumption in the ack, and again in NEED YOU in the morning.

## 2. Inventory — resources and candidates (≤ 10 min, cheap checks)
- **Compute:** `nvidia-smi` here (shared with other users — take only free
  cards, nice long jobs, never touch theirs); remote nodes from the project's machine list,
  if one exists; cluster queues if any are in play. Note what is free vs busy vs
  finishing soon.
- **Claude budget:** check remaining usage. Fleets and workflows overnight can drain the weekly
  limit; keep to the user's stop threshold. Prefer on-disk drivers (cost 0 tokens while they
  run) over agent-driven loops.
- **Candidates**, in priority order — pick the highest one that fits the free compute:
  1. Work the user already queued: today's conversation, the battleplan's next phase, the
     latest handoff file's "next session should pick up", WRAPUP_PLAN / TODO files.
  2. The experiment that most reduces uncertainty for the current goal (usually the paper):
     the ablation a reviewer would demand, the missing baseline, the seed repeat.
  3. Evals/metrics on finished checkpoints (project metrics) — cheap, always useful.
  4. Analysis of finished results → plots/report in the project's reports folder.
  5. Code hygiene — only if no compute-shaped work exists.
  Prefer GPU-hour-hungry work: idle GPU-hours are what is wasted overnight, not your time.
  Skip anything that needs the user's decision to be useful, anything already known pointless,
  and anything touching a design the user has fixed. Controlled comparisons: one factor
  at a time, nothing that breaks comparability with the baseline.

## 3. Launch — with the usual hygiene, plus durability
- Resolve the config and state what goes in (rows, filters, split, every deviation from
  baseline) in the log, not just your head. Smoke-test the exact command first.
- **Detached driver on disk, not an agent loop:** `nohup setsid <driver>.sh` writing
  `state.txt` / `result.txt` / logs under `<run>/` (the `final_now_driver.sh`
  pattern). The driver chains stage → stage and job → next job itself, with per-stage
  deadlines that fail loudly. If this session dies, the GPUs stay busy.
- Verify effect, not action: process alive after startup, first log lines, first wandb
  points; wandb URL into the morning report.
- One item per free GPU max; leave a card free if a housemate's job is clearly finishing
  and will want it back — shared machine.

## 4. Watch — sparse, durable
- Arm a monitor (Monitor tool / ScheduleWakeup ~30–60 min) whose only job is: dead? →
  diagnose; relaunch if the cause is cheap and understood (OOM → smaller batch, path
  typo); otherwise fall to the next candidate. Finished? → the driver should already have
  started the next job; if it did not, start it. Idle GPU at any wake-up = act, not note.
- Expectation before observation at each wake-up: state the loss/epoch/step you expect,
  compare, one line in the overnight log.
- Context getting tight → write a handoff file `YYYY-MM-DD_overnight.md` NOW, including how to check every driver, then continue.
- Pushes: none overnight except one, if the whole plan collapsed and cannot be
  recovered — they read it on waking. Everything else waits for the report.

## 5. Morning deliverable
- A report file `YYYY-MM-DD_overnight.md`:
  what was launched and why (the ladder rung), what finished, numbers vs baseline,
  what died and what was salvaged, what is still running with absolute ETAs, links.
- First message when the user appears: **/qu format**, unprompted, pointing at that file.
  Anything you decided for them → top of NEED YOU with the default you took.

## Never overnight
No irreversible or outward-facing actions: no push to main, no force-push, no deleting
runs/checkpoints/data, no paid-service spend beyond what they approved, no reopening locked
decisions, no changes to paper claims. Nothing that needs them to be useful. Nothing on
another user's process, GPU, or config.
