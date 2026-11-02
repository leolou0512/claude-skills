#!/usr/bin/env bash
# Detached watchdog: after an account's 5-hour limit resets, send a resume line to each part window of a launch.sh team.
# Start once: setsid nohup bash ~/.claude/skills/project-team/scripts/resume_watch.sh <proj> [config_dir] >> <team>/log/resume_watch.log 2>&1 &
# <proj> is launch.sh's tmux socket and session name; parts are its windows named p*. config_dir default ~/.claude.
proj=$1; CFG=${2:-$HOME/.claude}; D=${STATUS_DIR:-${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/claude-statusline/v3}
EVERY=${EVERY:-300}; GRACE=${GRACE:-300}; hit=0; reset=0
while true; do
  # max 5-hour % and latest reset over this account's recent status files (some carry no 5-hour field)
  read -r pct r < <(for f in $(grep -l "\"config_dir\":\"$CFG\"" "$D"/usage-*.json 2>/dev/null | xargs -r ls -t | head -12); do
      p=$(grep -o '"five_hour_pct":"[0-9]*"' "$f" | grep -o '[0-9][0-9]*'); x=$(grep -o '"five_hour_resets_at":"[0-9]*"' "$f" | grep -o '[0-9][0-9]*')
      [ -n "$p" ] && [ -n "$x" ] && echo "$p $x"; done | sort -k2,2n -k1,1n | tail -1)
  # a reset already handled stays in stale status files until sessions make a request: never act on it twice
  if [ "${pct:-0}" -ge 98 ] && [ $hit -eq 0 ] && [ "${r:-}" != "${done_reset:-}" ]; then hit=1; reset=$r; echo "$(date) limit hit ${pct}%, reset $(date -d "@$r")"; fi
  if [ $hit -eq 1 ] && [ "$(date +%s)" -gt $((reset+GRACE)) ]; then
    for w in $(tmux -L "$proj" list-windows -t "$proj" -F '#W' | grep '^p'); do
      tmux -L "$proj" send-keys -t "$proj:$w" "RESUME (5-hour limit reset; re-read RULES.md and your log)" Enter; done
    echo "$(date) resumed parts"; hit=0; done_reset=$reset
  fi
  sleep "$EVERY"
done
