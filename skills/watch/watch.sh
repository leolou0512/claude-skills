#!/usr/bin/env bash
# Silent watcher: costs no model tokens while it runs. Run with Bash run_in_background; its exit wakes the session.
# Usage: watch.sh [--every SEC] [--warm SEC] -- CHECK_COMMAND [ARGS...]
#   CHECK prints something when ready or broken, prints nothing otherwise. Exit 1 with no output counts as quiet (grep).
#   --every: seconds between checks (default 60).
#   --warm:  exit after this long and print WARM (default 3000 = 50 min, inside the 1 h main-session cache); 0 = never.
# Exits: fired (CHECK output, new since last report) | WARM | "watch: check failed ..." when CHECK itself breaks (exit >=2).
set -uo pipefail
every=60; warm=3000
while [ $# -gt 0 ]; do
  case "$1" in
    --every) every=$2; shift 2 ;;
    --warm) warm=$2; shift 2 ;;
    --) shift; break ;;
    *) break ;;
  esac
done
[ $# -gt 0 ] || { echo "watch: no check command" >&2; exit 2; }
state_dir="$HOME/.cache/watch"; mkdir -p "$state_dir"
state="$state_dir/$(printf '%s\0' "$PWD" "$@" | sha1sum | cut -c1-16)"
start=$(date +%s)
while true; do
  out=$("$@" 2>&1); rc=$?
  if [ "$rc" -ge 2 ]; then
    printf 'watch: check failed rc=%s: %s\n%s\n' "$rc" "$*" "$out" | head -c 2000; exit 1
  fi
  if [ -z "$out" ]; then : > "$state"
  elif [ "$out" != "$(cat "$state" 2>/dev/null)" ]; then
    printf '%s\n' "$out" > "$state"; printf '%s\n' "$out"; exit 0
  fi
  if [ "$warm" -gt 0 ] && [ $(( $(date +%s) - start )) -ge "$warm" ]; then echo WARM; exit 0; fi
  sleep "$every"
done
