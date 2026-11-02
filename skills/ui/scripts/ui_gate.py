#!/usr/bin/env python3
# PreToolUse Bash hook: refuse to merge UI paths without a reviewer verdict. No-op unless <git-common-dir>/ui-gate-paths exists.
import json, os, re, subprocess as sp, sys

d = json.load(sys.stdin)
cmd = d.get("tool_input", {}).get("command", "")
m = re.search(r"\bgit\b(?:\s+-C\s+(\S+))?[^;&|]*?\bmerge\b((?:\s+-{1,2}[\w=-]+)*)\s+([^\s;&|-]\S*)", cmd)
if not m:
    sys.exit(0)
where = os.path.expanduser(m.group(1) or d.get("cwd") or ".")
branch = m.group(3)

def git(*a, stdin=None):
    r = sp.run(["git", "-C", where, *a], input=stdin, text=True, capture_output=True)
    return r.stdout.strip() if r.returncode == 0 else ""

common = git("rev-parse", "--path-format=absolute", "--git-common-dir")
paths = os.path.join(common, "ui-gate-paths") if common else ""
if not paths or not os.path.exists(paths):
    sys.exit(0)
changed = git("diff", "--name-only", f"HEAD...{branch}")
pattern = open(paths).read().strip()
if not changed or not pattern or not re.search(pattern, changed):
    sys.exit(0)
patch = git("diff", f"HEAD...{branch}")
pid = git("patch-id", "--stable", stdin=patch + "\n").split()[:1]
verdict = os.path.join(common, "ui-gate", (pid or ["none"])[0] + ".md")
first = open(verdict).readline() if os.path.exists(verdict) else ""
if first.startswith(("PASS", "USER-SKIP")):
    sys.exit(0)
os.makedirs(os.path.dirname(verdict), exist_ok=True)
print(f"UI paths changed on {branch}: see /ui. Fresh reviewer writes {verdict}; first line must be PASS.", file=sys.stderr)
sys.exit(2)
