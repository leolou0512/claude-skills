#!/usr/bin/env python3
# PostToolUse hook: a subagent over LIMIT is told to wrap up and hand back. Never compacts, never kills. Main sessions: no-op.
# Reads the subagent's own transcript; layout is observed, not documented: re-test after a Claude Code upgrade.
import json, os, sys

LIMIT = int(os.environ.get("TEAM_SUB_CTX_LIMIT", "400000"))
d = json.load(sys.stdin)
if not d.get("agent_id"):
    sys.exit(0)
p = d.get("agent_transcript_path") or d["transcript_path"][:-6] + "/subagents/agent-" + d["agent_id"] + ".jsonl"

def ctx_values(lines):
    for line in lines:
        if '"usage"' not in line:
            continue
        try:
            u = (json.loads(line).get("message") or {}).get("usage")
        except Exception:
            continue
        if u:
            yield u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("input_tokens", 0)

try:
    with open(p, "rb") as f:
        head = f.read(2_000_000).decode("utf8", "ignore").splitlines()
        f.seek(0, 2)
        f.seek(max(0, f.tell() - 2_000_000))
        tail = f.read().decode("utf8", "ignore").splitlines()
except OSError:
    sys.exit(0)
first = next(ctx_values(head), 0)
ctx = 0
for ctx in ctx_values(tail):
    pass
if first >= LIMIT / 2:  # fork inheriting a big parent: this agent didn't grow it
    sys.exit(0)
if ctx >= LIMIT:
    print(f"context {ctx // 1000}k over {LIMIT // 1000}k: stop new work; commit what is done; report done + exact remaining items to your lead now", file=sys.stderr)
    sys.exit(2)
