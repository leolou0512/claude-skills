---
name: results-table-html
description: Build a self-contained, single-file HTML table for comparing experiment results from a CSV. Sortable columns, collapsible column groups, frozen header and identifier columns, ↑/↓ direction arrows, best-value highlighting, per-column number formats, dark mode, no external dependencies. Use when the user asks for a results table, a sweep summary, "make a table from the CSV", or an interactive comparison they can sort and scroll.
---

# results-table-html

## Quick start

```bash
python ~/.claude/skills/results-table-html/scripts/build_table.py --csv results.csv --out table.html
```

No config needed. Leading text columns are frozen at the left, the rest form one group, and
the direction of a metric is guessed from its name (loss, error, time → ↓; accuracy, f1, score
→ ↑). Unsure names get no arrow. Open the HTML in any browser.

## When the automatic layout is not enough

Add `--config table.json`. Start from `scripts/example_config.json`. Every key is optional:

- `groups`: `[[id, label, [columns]], ...]`. The first group is frozen at the left. Columns in
  no group are added as "Other", never dropped.
- `higher_better` / `lower_better`: arrows and green best-value cells. Setting either turns off
  the name guessing.
- `no_highlight`: columns that should never be green (inputs, settings).
- `rate_as_percent`: 0–1 values shown as `xx.xx%`.
- `formats`: per-column format: `f3` (3 decimals), `pct2` (×100, 2 decimals, %), `pct1raw`
  (already %, 1 decimal), `int`, `sci3`.
- `ident_widths`: pixel width per frozen column (estimated from content when absent).
- `title`.

## Rules

- Format per column, never per row: one column, one number of decimals.
- No arrow is better than a wrong arrow. Leave a column out of both direction lists when unsure.
- Read the script's printed summary (frozen columns, guessed directions) and its warnings.
- Keep the output one self-contained file.
