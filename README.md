# Claude Code skills

| | What it does |
|---|---|
| `skills/academic-writing` | Makes paper prose precise instead of AI-sounding, and builds the story around the strongest result. |
| `skills/project-team` | Runs one project with several agents: one plans, one coordinates, the rest build in parallel. |
| `skills/bedtime` | Keeps Claude and your GPUs working overnight, with a report ready in the morning. |
| `skills/qu` | Three-heading status update: running, results, needs you. |
| `skills/grill-me` | Claude questions you about a plan until every decision is settled. |
| `skills/results-table-html` | Turns a CSV of results into one sortable HTML table. |
| `output-styles/caveman.md` | Short replies, answer first. |

## Install

```bash
mkdir -p ~/.claude/skills ~/.claude/output-styles
cp -r skills/* ~/.claude/skills/
cp output-styles/caveman.md ~/.claude/output-styles/
```

To use the style, add `"outputStyle": "caveman"` to `~/.claude/settings.json`.

## Credits

- `grill-me` is a modified version of grill-me from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT).
- `caveman.md` is a modified version of [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) (Apache-2.0).
