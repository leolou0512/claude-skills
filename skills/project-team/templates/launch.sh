#!/usr/bin/env bash
# Opens named Claude sessions for this project in tmux (own socket, clean env).
# Run on the project machine, any terminal (user) or from the coordinator session:
#   bash ~/__REPO__/team/launch.sh            # coordinator + all parts
#   bash ~/__REPO__/team/launch.sh 3 5        # only parts 3 and 5
#   bash ~/__REPO__/team/launch.sh coord      # only coordinator
# Watch: tmux -L __PROJ__ attach -t __PROJ__   (sessions also appear in the Claude app via remote control)
# Repo folder must already be trusted by Claude Code (it is if the brainstorm agent ran there), else each window stops at the trust prompt.
set -euo pipefail
PROJ="__PROJ__"
ROOT="$HOME/__REPO__"
PARTS=(__PART_NUMBERS__)            # e.g. (1 2 3 4 5 6)
MODE="${MODE:-auto}"                # permission mode
EXTRA="${EXTRA:-}"                  # e.g. EXTRA="--model opus --effort medium"
T=(tmux -L "$PROJ")

# Strip Claude session markers: a claude started with them writes no transcript (silent).
CLEAN=(env $(env | grep -oE '^(CLAUDE[A-Z_]*|CLAUDECODE)=' | sed 's/=$//; s/^/-u /' || true))

if ! "${T[@]}" has-session -t "$PROJ" 2>/dev/null; then
  "${CLEAN[@]}" "${T[@]}" new-session -d -s "$PROJ" -n shell -c "$ROOT"
fi
if "${T[@]}" show-environment -g 2>/dev/null | grep -q '^CLAUDE'; then
  echo "tmux -L $PROJ server carries CLAUDE* vars; kill it (tmux -L $PROJ kill-server) and rerun" >&2; exit 1
fi

open() {  # $1 window, $2 session name, $3 first prompt
  local w=$1 name=$2 prompt=$3
  if "${T[@]}" list-windows -t "$PROJ" -F '#W' | grep -qx "$w"; then echo "skip $w (already open)"; return; fi
  "${T[@]}" new-window -t "$PROJ" -n "$w" -c "$ROOT"
  "${T[@]}" send-keys -t "$PROJ:$w" \
    "$(printf 'claude --permission-mode %q %s -n %q --remote-control %q %q' "$MODE" "$EXTRA" "$name" "$name" "$prompt")" Enter
  echo "opened $w → \"$name\""
}

part_prompt() { echo "You are $PROJ part $1. Load skill project-team, read $ROOT/team/TEAM.md and your brief $ROOT/team/parts/P$(printf %02d "$1")_*.md, then follow worker.md."; }
coord_prompt="You are the $PROJ coordinator. Load skill project-team, read $ROOT/team/TEAM.md, then follow coordinator.md."

want=("$@"); [ ${#want[@]} -eq 0 ] && want=("${PARTS[@]}" coord)
for x in "${want[@]}"; do
  if [ "$x" = coord ]; then continue; fi
  open "p$x" "$PROJ part $x" "$(part_prompt "$x")"; sleep 2
done
# Coordinator last, so its first ListAgents already sees the parts.
for x in "${want[@]}"; do
  if [ "$x" = coord ]; then sleep 10; open coord "$PROJ coordinator" "$coord_prompt"; fi
done
