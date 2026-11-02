---
name: project-team
description: the user's multi-agent project framework — one brainstorm agent scopes a new project and writes per-part briefs; one coordinator (no real work) dispatches, stops and resumes; N part agents implement in parallel, talking only through a shared board (BOARD.md) and rare one-line messages. Use when the user says "you're the brainstorm agent", "you are the coordinator", "you are part N" / "agent task N" / "task N", "start a new project with agents", "next wave", or when a repo has a team folder (`team/`, or one TEAM.md names) and a session is told its role. Not for single-session tasks.
---

# Project team

Three roles. Read the shared rules below, then ONLY your role file:
- **Brainstorm**: "you're the brainstorm agent" → [brainstorm.md](brainstorm.md)
- **Coordinator**: "you are the coordinator" → [coordinator.md](coordinator.md). Separate session, never numbered.
- **Part N**: "you are part N" (also "task N", "agent N") → [worker.md](worker.md)

`<repo>` = folder `~/<repo>`; `<proj>` = short name in session names (often the same). `<NN>` = two-digit part number. `<team>` = `~/<repo>/team`, or the folder TEAM.md Facts names.
Skill files: `~/.claude/skills/project-team/` (`templates/`, `scripts/tokens.sh` per-session tokens, `scripts/patrol.sh` coordinator patrol, `scripts/resume_watch.sh` resume after a limit, `TEAM_DIR=<folder>` for a non-default team folder).
Built from two multi-agent game-build runs.

## Project layout (made by brainstorm)
```
CLAUDE.md              agent guide: repo map, commands, fast/slow tests, where things live, team pointer (templates/CLAUDE_root.md)
<pkg>/CLAUDE.md        purpose, entry files, how to add X, tests, owner (templates/CLAUDE_pkg.md); written with the package
.ignore                hides research dumps, generated data, dist, .data from search (templates/ignore)
.claude/settings.json  {"crossSessionInbound": "accept"}  ← sessions can receive messages
docs/INTERFACES.md     contracts between parts; in git; changed in the same commit as code
<team>/                coordination state; default `team/` (gitignored); live copy only in the main checkout
  TEAM.md      project facts, read order, coordinator powers
  RULES.md     standing agent rules, dated one-liners; read on every wake        ≤2.5 KB
  BOARD.md     one line per part (state, current, next) · Need User ≤5 · last 10 milestones  ≤3 KB
  QUEUE.md     next features in order · owner · waits-user flag                   ≤2 KB
  PITFALLS.md  symptom → fix one-liners                                            ≤3 KB
  SCOPE.md     goal · the user decided (dated) · proposed defaults · out of scope
  PARTS.md     part table (= ownership map) · dispatch table · flow chart · waves
  parts/P<NN>_<name>.md   one brief per part
  REQUESTS.md  the user's requests/bug reports, their words, owner, state
  ISSUES.md    cross-part bugs · DECISIONS.md deviations · log/ per-part notes, archives
  research/NN_<topic>.md · launch.sh (named sessions in tmux; optional)
```
Worktree copies of `<team>` are missing or stale: always absolute paths `<team>/...`.

## Shared rules (every role)
**Names are addresses.** `<proj> coordinator`, `<proj> part N`; SendMessage to that exact name. Agents can't rename themselves: if ListAgents' first line ("This session is …") isn't your name, ask the user once: "`/rename <proj> part N` please", keep reading meanwhile.

**Message only when someone must act.** One tag, first word:
| Tag | From → to | When |
|---|---|---|
| `DONE P3.2 <sha>` | part → coordinator | step named in some dispatch Needs, or whole part, merged. Milestones go ONLY here |
| `START P4.2` | coordinator → part | every Need of that step merged |
| `STOP` / `RESUME` | coordinator → parts | run control |
| `REQ R7` / `DONE R7 <sha>` | coordinator ↔ owner part | the user's request routed / finished. ID only: their exact words stay in the REQUESTS.md row, read them there |
| `DECISION <the user's words>` | coordinator → affected parts; part → coordinator if the user told the part | the user decided something |
| `ISSUES N` | part → owner part | N new lines for you in ISSUES.md, batched |
| `IFACE` | part → affected parts | contract in INTERFACES.md changed under them |
| `BLOCKED` | part → coordinator | can't proceed AND no stopgap (else a Need User line, no message) |
| `ASK` | anyone → anyone | needs an answer; the ONLY tag that gets a reply |
- Caveman, ≤2 lines, ≤300 chars, fact first. Point to file/commit, don't explain.
- **No reply unless `ASK`.** Never ack, thank, "will do", "starting now", progress, "all fine".
- Worth recording → disk (BOARD line, log, ISSUES, DECISIONS, PITFALLS), not a message.
- Rule changes (how agents work, budget, process) → RULES.md, dated; never a broadcast. Everyone re-reads RULES.md on every wake.
- Waiting: end your turn. No polling, no sleep loops; a message wakes you. Waiting on a job or state: `/watch` skill.
- Pass references, not text: to anyone, including subagents, give a file, row or commit to read, never a retelling.
- Agent drifting (chatty, acking, off-scope): one-line reminder, once.

**Shared files.** Many agents write `<team>`. Each agent edits ONLY its own BOARD line. BOARD/REQUESTS/QUEUE/RULES: Edit tool only (it refuses stale writes; re-read and retry); ISSUES/DECISIONS/PITFALLS: append with `>>`. Never `sed -i` or Write over them. At each wave end the coordinator tidies BOARD, RULES, PITFALLS, QUEUE to their caps; old content → `log/`.

**the user gets questions only through the coordinator**, batched and numbered. Parts never block on the user and never use AskUserQuestion: Need User line in BOARD (`- [ ] P3: question; stopgap used; impact`), use the brief's suggestion, log in DECISIONS.md, continue.

**Every role is a lead.** Main session plans, splits, reviews diffs, integrates, reports. Every task (code, tests, builds, research, deploy checks) → a subagent with a caveman brief (scope, absolute paths they may edit, done criteria), ≤100-word reports, long output to files. Concurrent subagents never edit the same file; shared registries/index files only by the lead. Every Agent call names `model`: `sonnet` for easy features, tests, builds, deploy checks; `opus` only for hard design/visual work.

**Subagent over 400k:** a hook (`scripts/sub_ctx_guard.py`) tells it to hand back done + exact remainder; spawn a fresh one for the rest.

**Context cap ~400-500k.** Update your memory tree (`/memtree`, `<team>/memory/P<NN>/`). Write log/handoff (step, done, next, blockers), then compact (the user prefers it to a restart). Agents can't run `/compact` themselves: one line to the user in your session ("`/compact` please, log saved") and `needs /compact` on your BOARD line; end turn.

**Shared machine.** Kill only PIDs you started (one part's `pkill -f vite` killed everyone's servers). Only your port range. `nvidia-smi` before GPU use. Never declare another agent dead from ListAgents alone (check `ps`, tmux, transcript mtime); never kill or take over its work or processes without the user. Never restart a service someone may be using (the user playing, a demo) without checking it is idle. Auto mode blocks a command → don't retry or work around; Need User line; move on. The user's global rules still apply.

**STOP**: finish current small action, stop your subagents and dev servers (prod/live services stay up), commit WIP on your branch (never main), log "stopped at X, next Y", BOARD line `stopped`, end turn. **RESUME / after compaction**: re-read RULES.md, your log, your BOARD line, `git status`; continue.
