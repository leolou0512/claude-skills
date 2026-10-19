---
name: project-team
description: Multi-agent project framework — one brainstorm agent scopes a new project and writes per-part briefs; one coordinator (no real work) dispatches, stops and resumes; N part agents implement in parallel, talking only through a shared status board and rare one-line messages. Use when the user says "you're the brainstorm agent", "you are the coordinator", "you are part N" / "agent task N" / "task N", "start a new project with agents", "next wave", or when a repo has a `team/` folder and a session is told its role. Not for single-session tasks.
---

# Project team

Three roles. Read the shared rules below, then ONLY your role file:
- **Brainstorm**: "you're the brainstorm agent" → [brainstorm.md](brainstorm.md)
- **Coordinator**: "you are the coordinator" → [coordinator.md](coordinator.md). Separate session, never numbered.
- **Part N**: "you are part N" (also "task N", "agent N") → [worker.md](worker.md)

`<repo>` = folder `~/<repo>`; `<proj>` = short name in session names (often the same). `<NN>` = two-digit part number.
Skill files: `~/.claude/skills/project-team/` (`templates/`, `scripts/tokens.sh` per-session tokens, `scripts/patrol.sh` coordinator patrol).
Built from the user's own multi-agent project runs (2026-10).

## Project layout (made by brainstorm)
```
CLAUDE.md              3-line pointer only (templates/CLAUDE_pointer.md)
.claude/settings.json  {"crossSessionInbound": "accept"}  ← sessions can receive messages
docs/INTERFACES.md     contracts between parts; in git; changed in the same commit as code
team/                  coordination state; `/team/` gitignored; lives ONLY in ~/<repo>/team
  TEAM.md      project facts, read order, coordinator powers, project-specific rules
  SCOPE.md     goal · User decided (dated) · proposed defaults · out of scope
  PARTS.md     part table · dispatch table · flow chart · waves
  parts/P<NN>_<name>.md   one brief per part
  STATUS.md    one row per part · Need user · last 10 milestones
  REQUESTS.md  the user's requests/bug reports, their words, owner, state
  ISSUES.md    cross-part bugs · DECISIONS.md deviations · log/P<NN>.md per-part notes
  research/NN_<topic>.md · launch.sh (named sessions in tmux; optional)
```
Worktrees have no `team/`: always absolute paths `~/<repo>/team/...`.

## Shared rules (every role)
**Names are addresses.** `<proj> coordinator`, `<proj> part N`; SendMessage to that exact name. Agents can't rename themselves: if ListAgents' first line ("This session is …") isn't your name, ask the user once: "`/rename <proj> part N` please", keep reading meanwhile.

**Message only when someone must act.** One tag, first word:
| Tag | From → to | When |
|---|---|---|
| `DONE P3.2 <sha>` | part → coordinator | step named in some dispatch Needs, or whole part, merged. Milestones go ONLY here |
| `START P4.2` | coordinator → part | every Need of that step merged |
| `STOP` / `RESUME` | coordinator → parts | run control |
| `REQ R7 <the user's words>` / `DONE R7 <sha>` | coordinator ↔ owner part | the user's request routed / finished |
| `DECISION <the user's words>` | coordinator → affected parts; part → coordinator if the user told the part | the user decided something |
| `ISSUES N` | part → owner part | N new lines for you in ISSUES.md, batched |
| `IFACE` | part → affected parts | contract in INTERFACES.md changed under them |
| `BLOCKED` | part → coordinator | can't proceed AND no stopgap (else a Need user line, no message) |
| `ASK` | anyone → anyone | needs an answer; the ONLY tag that gets a reply |
- Caveman, ≤2 lines, ≤300 chars, fact first. Point to file/commit, don't explain.
- **No reply unless `ASK`.** Never ack, thank, "will do", "starting now", progress, "all fine".
- Worth recording → disk (STATUS row, log, ISSUES, DECISIONS), not a message.
- Waiting: end your turn. No polling, no sleep loops; a message wakes you.
- Agent drifting (chatty, acking, off-scope): one-line reminder, once.

**Shared files.** Many agents write `team/`: change STATUS/REQUESTS with the Edit tool only (it refuses stale writes; re-read and retry), append to ISSUES/DECISIONS with `>>`. Never `sed -i` or Write over them.

**The user gets questions only through the coordinator**, batched and numbered. Parts never block on the user and never use AskUserQuestion: Need user line in STATUS (`- [ ] P3: question; stopgap used; impact`), use the brief's suggestion, log in DECISIONS.md, continue.

**Every role is a lead.** Broad reading, coding, long tests → subagents with caveman briefs (scope, absolute paths they may edit, done criteria), ≤100-word reports, long output to files. Concurrent subagents never edit the same file; shared registries/index files only by the lead.

**Shared machine.** Kill only PIDs you started (one part's `pkill -f vite` killed everyone's servers). Only your port range. `nvidia-smi` before GPU use. Never declare another agent dead from ListAgents alone (check `ps`, tmux, transcript mtime); never kill or take over its work or processes without the user. Never restart a service someone may be using (the user playing, a demo) without checking it is idle. Auto mode blocks a command → don't retry or work around; Need user line; move on. The user's global rules still apply.

**STOP**: finish current small action, stop your subagents and dev servers (prod/live services stay up), commit WIP on your branch (never main), log "stopped at X, next Y", row `stopped`, end turn. **RESUME / after compaction**: re-read TEAM.md (rules may have changed), your log, your row, `git status`; continue.
