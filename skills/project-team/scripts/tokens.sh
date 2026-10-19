#!/usr/bin/env bash
# Token use per session of a project. out = session's own output tokens (subagent output is not reliably logged);
# input+cache includes its subagents. Times UTC.
# Usage: bash tokens.sh ~/<repo>
set -euo pipefail
dir="$HOME/.claude/projects/$(realpath "${1:?repo path}" | sed 's|[^A-Za-z0-9]|-|g')"
[ -d "$dir" ] || { echo "no transcripts in $dir" >&2; exit 1; }
sum='map(select(.type=="assistant" and .message.usage)) | unique_by(.message.id) | map(.message.usage)
     | {out: (map(.output_tokens // 0) | add // 0),
        cache: (map((.cache_read_input_tokens // 0) + (.cache_creation_input_tokens // 0) + (.input_tokens // 0)) | add // 0)}'
printf '%-26s %9s %13s  %s\n' session out input+cache last_utc
for f in "$dir"/*.jsonl; do
  id=$(basename "$f" .jsonl)
  name=$(jq -rs 'map(select(.type=="custom-title") | .customTitle) | last // "(unnamed)"' "$f")
  last=$(jq -rs 'map(.timestamp // empty) | last // "" | .[5:16]' "$f")
  own=$(jq -cs "$sum" "$f")
  subs=$(ls "$dir/$id"/subagents/*.jsonl 2>/dev/null || true)
  if [ -n "$subs" ]; then sub=$(cat $subs | jq -cs "$sum"); else sub='{"out":0,"cache":0}'; fi
  jq -rn --arg n "$name" --arg l "$last" --argjson o "$own" --argjson s "$sub" \
    '[$n, $o.out, ($o.cache + $s.cache), $l] | @tsv'
done | sort -t$'\t' -k2,2nr | awk -F'\t' '{printf "%-26s %9d %13d  %s\n",$1,$2,$3,$4}'
