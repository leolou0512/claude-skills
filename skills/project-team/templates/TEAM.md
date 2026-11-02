# TEAM: __PROJ__
Rules: skill `project-team` + `RULES.md` (standing rules, read on every wake). This file = project facts.

## Read order for any new agent
1. this file → 2. `RULES.md` → 3. `SCOPE.md` → 4. `PARTS.md` (your row + dispatch table) → 5. `PITFALLS.md` → 6. your brief / role file → 7. its "Read first" list.

## Facts
| Item | Value |
|---|---|
| Repo (main checkout = integration only) | `~/__REPO__`, branch `main`, push: no |
| Team folder | `~/__REPO__/__TEAM_DIR__/` (default `team/`, gitignored; absolute paths from worktrees) |
| Worktrees | `~/__REPO__-wt/p<NN>`, branch `part-<NN>` |
| Sessions | `__PROJ__ coordinator`, `__PROJ__ part 1` … `__PROJ__ part N` |
| Ports | part N: 40000 + 100·N … +99 (part 3 = 40300–40399); prod: __PROD_PORT__ |
| Build / fast gate / slow tests | root `CLAUDE.md` §Commands |
| Prod / the user's URL | `git -C ~/__REPO__ worktree add --detach ~/__REPO__-prod main`; update `git -C ~/__REPO__-prod checkout --detach main` after green tests; owner part __OPS__; URL __URL__ |
| Machine | __MACHINE__; heavy jobs: __HEAVY__ |
| tmux (if launch.sh used) | `tmux -L __PROJ__ attach -t __PROJ__` |

## Coordinator powers
May decide: order, timing, anything SCOPE/PARTS already answer.
Must ask the user: any number/limit/budget/scope change, public exposure, restarting a live service, adding a part.
