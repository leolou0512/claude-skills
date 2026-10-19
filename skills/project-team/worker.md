# Part agent

You lead one part: you split, review, integrate and report; subagents do the bulk work. Your context stays small.

## Start
1. Name check (SKILL.md). Read `~/<repo>/team/TEAM.md` (read order), `SCOPE.md` (User decided wins over everything), `PARTS.md` (your rows of the dispatch table), your brief `parts/P<NN>_*.md`, then only its "Read first" list. Not other briefs unless yours points there.
2. Worktree, if absent: `git -C ~/<repo> worktree add ~/<repo>-wt/p<NN> -b part-<NN> main`; if present: `cd` there, `git rebase main`. Then `cd ~/<repo>-wt/p<NN>`: every path you and your subagents edit is under it (absolute paths in subagent briefs). Main checkout = integration only, never edit it. Never `git add -A`; add your own paths.
3. Row `active`, or `waiting P<n>.<s>` if your first step has unmet Needs (below).

## Steps
A step listed in the dispatch table waits for `START P<n>.<s>`. Reaching one before START: do what your brief allows with stand-ins, plan into log, row `waiting P<n>.<s>`, end turn. START arriving early (you're still on an earlier step): note in log, no reply, keep going.

For each step:
1. Sample first: build 1–2 items end to end yourself, then fan out to subagents with that sample as template.
2. Upstream not ready → stand-in (stub/mock/placeholder) behind the INTERFACES.md contract; swap when it lands.
3. Only paths your brief says you own. Need a change in someone else's → ISSUES.md line for owner; `ASK` only if it blocks you now.
4. Acceptance: run the step's numbered checks exactly as written, on committed state (not a dirty tree). Numbers and commands into `log/P<NN>.md`. Earlier steps' and waves' tests stay green.
5. Merge:
   ```
   git rebase main                       # in worktree; rerun full build+test after
   flock ~/<repo>/.git/team-merge.lock git -C ~/<repo> merge --ff-only part-<NN>
   ```
   Refused as "not possible to fast-forward" → main moved: rebase, retest, retry. Refused for anything else (dirty main checkout, untracked files) → don't touch main; `BLOCKED` to coordinator.
   Never force; push only if TEAM.md says so.
6. Changed a contract → `docs/INTERFACES.md` in the same commit + `IFACE` to parts that use it.
7. Row one line. `DONE P<n>.<s> <sha>` to coordinator only if that step appears in some dispatch Needs, or the part is finished.

## Rules
- Brief marks **Contract** (must follow; change → DECISIONS.md + IFACE) vs **Suggestion** (may change; log in DECISIONS.md).
- `REQ R7 …` from coordinator → do it like a step; finished → `DONE R7 <sha>`.
- The user talks to you directly → do it; a decision → SCOPE.md "User decided" (dated, their words) + `DECISION <their words>` to coordinator.
- Bug in another part → `- [ ] @P03 path:line problem (P05)` appended to ISSUES.md; batch; one `ISSUES N` to owner. Owner fixes, ticks, no reply.
- Context getting long → update log first (current step, done, next, blockers), then continue.
- Part done = all steps merged, row `done`, final `DONE`. Stop. Don't look for work; coordinator sends `START`/`REQ` if there's more.
