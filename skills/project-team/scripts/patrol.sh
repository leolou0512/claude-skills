#!/usr/bin/env bash
# Coordinator patrol: prints only NEW conditions needing action; prints nothing when all fine.
# Usage: [TEAM_DIR=docs/parts] [DRY=1] bash ~/.claude/skills/project-team/scripts/patrol.sh ~/<repo> "<proj>" [quiet_minutes=45]
#   TEAM_DIR: team folder relative to repo (default team). DRY=1: print all current conditions, write no state.
set -uo pipefail
repo=$(realpath "$1"); proj=$2; quiet=${3:-45}
team=$repo/${TEAM_DIR:-team}; board=$team/BOARD.md
prev=$HOME/.cache/project-team/patrol_$(printf %s "$proj" | tr -c 'A-Za-z0-9' _)   # outside repo: team dir may be in git
tdir="$HOME/.claude/projects/$(echo "$repo" | sed 's|[^A-Za-z0-9]|-|g')"
[ -f "$board" ] || { echo "patrol: no $board"; exit 0; }
now=$(date +%s); cur=()

# Part lines: | N (or "<proj> part N …") | state | current | next |; other rows ignored
while IFS=$'\t' read -r n state note; do
  case "$note" in *"needs /compact"*) cur+=("P$n needs /compact (batch to the user)") ;; esac
  case "$state" in
    blocked) cur+=("P$n blocked: $note") ;;
    active)
      f=$(grep -l "\"customTitle\":\"$proj part $n\"" "$tdir"/*.jsonl 2>/dev/null | xargs -r ls -t 2>/dev/null | head -1)
      if [ -z "$f" ]; then cur+=("P$n active but no transcript named '$proj part $n'")
      else age=$(( (now - $(stat -c %Y "$f")) / 60 )); [ "$age" -ge "$quiet" ] && cur+=("P$n active but quiet ${age}m (check ps/tmux before acting)"); fi ;;
  esac
done < <(awk -F'|' 'NF>=6 { c=$2; gsub(/^ +| +$/,"",c); n=""
  if (c ~ /^[0-9]+$/) n=c; else if (match(c, /part [0-9]+/)) n=substr(c, RSTART+5, RLENGTH-5)
  if (n=="") next; for(i=3;i<=5;i++) gsub(/^ +| +$/,"",$i); print n"\t"$3"\t"$4" | "$5 }' "$board")

# Open Need User items (ticked and template "P?:" lines ignored); cap 5
nl=$(awk '/^## Need User/{f=1;next} /^## /{f=0} f && /^- / && !/^- \[x\]/ && !/P\?:/' "$board" | wc -l)
[ "$nl" -gt 0 ] && cur+=("Need User: $nl open$([ "$nl" -gt 5 ] && echo ' (cap 5)')")

# Shared files present and under their caps (bytes)
for fc in BOARD:3072 RULES:2560 PITFALLS:3072 QUEUE:2048; do
  f=$team/${fc%%:*}.md
  if [ ! -f "$f" ]; then cur+=("no ${fc%%:*}.md in $team")
  elif [ "$(stat -c %s "$f")" -gt "${fc#*:}" ]; then cur+=("${fc%%:*}.md over cap: tidy, old → log/"); fi
done

# Budget verdict (optional usage check; skipped when absent)
b=$(timeout 30 bash "$HOME/.claude/skills/budget/check_usage.sh" 2>/dev/null | grep '^VERDICT' || true)
case "$b" in *CLEAR*|"") ;; *) cur+=("Budget: ${b#VERDICT: }") ;; esac

if [ -n "${DRY:-}" ]; then [ "${#cur[@]}" -gt 0 ] && printf '%s\n' "${cur[@]}"; exit 0; fi
# Print only conditions not reported last time
mkdir -p "${prev%/*}"; touch "$prev"
for c in "${cur[@]}"; do grep -qxF -- "$c" "$prev" || echo "$c"; done
printf '%s\n' "${cur[@]}" > "$prev"
