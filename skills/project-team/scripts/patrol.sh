#!/usr/bin/env bash
# Coordinator patrol: prints only NEW conditions needing action; prints nothing when all fine.
# Usage: bash ~/.claude/skills/project-team/scripts/patrol.sh ~/<repo> "<proj>" [quiet_minutes=45]
set -uo pipefail
repo=$(realpath "$1"); proj=$2; quiet=${3:-45}
team=$repo/team; st=$team/STATUS.md; prev=$team/.patrol_state
tdir="$HOME/.claude/projects/$(echo "$repo" | sed 's|[^A-Za-z0-9]|-|g')"
[ -f "$st" ] || { echo "patrol: no $st"; exit 0; }
now=$(date +%s); cur=()

# Part rows: | N | state | step | merge | note | updated |
while IFS=$'\t' read -r n state note; do
  case "$state" in
    blocked) cur+=("P$n blocked: $note") ;;
    active)
      f=$(grep -l "\"customTitle\":\"$proj part $n\"" "$tdir"/*.jsonl 2>/dev/null | xargs -r ls -t 2>/dev/null | head -1)
      if [ -z "$f" ]; then cur+=("P$n active but no transcript named '$proj part $n'")
      else age=$(( (now - $(stat -c %Y "$f")) / 60 )); [ "$age" -ge "$quiet" ] && cur+=("P$n active but quiet ${age}m (check ps/tmux before acting)"); fi ;;
  esac
done < <(awk -F'|' '/^\| *[0-9]+ *\|/ {for(i=2;i<=6;i++) gsub(/^ +| +$/,"",$i); print $2"\t"$3"\t"$6}' "$st")

# Open Need user items (template line "P?:" ignored)
nl=$(awk '/^## Need user/{f=1;next} /^## /{f=0} f && /^- \[ \]/ && !/P\?:/' "$st" | wc -l)
[ "$nl" -gt 0 ] && cur+=("Need user: $nl open")

# Budget verdict (optional: needs a budget-check script; skipped if absent)
b=$(timeout 30 bash "$HOME/.claude/skills/budget/check_usage.sh" 2>/dev/null | grep '^VERDICT' || true)
case "$b" in *CLEAR*|"") ;; *) cur+=("Budget: ${b#VERDICT: }") ;; esac

# Print only conditions not reported last time
touch "$prev"
for c in "${cur[@]}"; do grep -qxF "$c" "$prev" || echo "$c"; done
printf '%s\n' "${cur[@]}" > "$prev"
