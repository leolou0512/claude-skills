# __PROJ__: agent guide
<!-- project-team pointer: keep these 2 lines -->
Multi-agent project. If the user names your role (brainstorm / coordinator / part N): load skill `project-team`, then read `~/__REPO__/__TEAM_DIR__/TEAM.md`. Otherwise ignore `__TEAM_DIR__/` and work normally.

## Repo map
| Path | What | Owner |
|---|---|---|
| `__PATH__` | __WHAT__ | P__N__ |

## Commands
- Install / build: `__BUILD__`
- Fast tests (seconds, on source; pre-merge gate): `__TEST_FAST__`
- Slow tests (e2e, long runs): `__TEST_SLOW__`
- Regenerate registries: `__GEN__`

## Where things live
- One file per item (`__ITEM_DIR__/<id>.ts`); registries generated, never hand-edited.
- Contracts: `docs/INTERFACES.md`. Package details: each package's `CLAUDE.md`.
