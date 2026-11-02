---
name: watch
description: Silent two-tier watcher for any session. A plain script checks cheaply and wakes the session as soon as something is ready or broken; a 50-minute wake keeps the conversation cache warm. Use whenever a session waits on a job, run, deploy, build, team or external state, or when anyone says patrol, monitor, watcher, "tell me when done", "keep checking", or would otherwise reach for cron, sleep loops or repeated polling.
---

# Watch

Never poll from the model. Every model wake re-reads the whole context.

```bash
# Bash with run_in_background: true
bash ~/.claude/skills/watch/watch.sh -- <check command>
```

- **Tier 1, silent:** the check runs every 60 s (`--every`) as plain shell. It exits, waking the session, as soon as the check prints something new. Quiet costs no tokens.
- **Tier 2, keep warm:** at 50 min it exits with `WARM`. That read resets the 1-hour cache, so the next real wake doesn't pay a rebuild. `--warm 0` turns it off: use when nothing may wake this session for over a day.

## On wake
- `WARM`: relaunch the same command. No text to the user.
- Check output: act and report, then relaunch if still waiting.
- `watch: check failed`: the check broke. Fix it and tell the user; a dead watcher is not calm.

## Writing the check
Print only when action is needed; print nothing otherwise. Same output twice is reported once.

| wait for | check |
|---|---|
| process end | `bash -c 'kill -0 <pid> 2>/dev/null \|\| echo "<pid> ended"'` |
| result file | `bash -c '[ -e <path> ] && echo "<path> ready"; true'` |
| log failure | `grep -m1 -E "Traceback\|FAILED" <log>` |
| several things | a small script that echoes one line per item |

Use a slower `--every` for checks heavier than a few seconds.

## Limits
- The watcher dies with its session. To outlive the session, run the job detached with on-disk state; the watcher only reports on it.
- Subagents have a 5-minute cache: they hand back with the job path and let the lead watch, rather than wait.
- Cost numbers are API-price estimates; subscription weights are unpublished.
