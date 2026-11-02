---
name: ui
description: Makes interfaces a human finds obvious and good-looking. Copy from mature products before building, operate the result with real input on each device, cut explanatory text, and pass an independent reviewer before merge. Use when building or changing any screen, page, HUD, menu, form, dashboard or player-facing text, when the user says /ui, "ugly", "not intuitive", "can't click", "too complicated", "defensive text", or when a project with a user interface starts.
---

# UI

The user's time goes here first: controls unreachable the way humans really use them, self-made ugly screens, needless text.

## Before building a screen
1. **Real use:** `docs/ref/REAL_USE.md`, one line per device: size, input, cursor state. Example: "PC: pointer locked in game, Esc releases. Phone: touch only."
2. **References:** `docs/ref/<screen>_*.png` from 2-3 mature products. Note: copy what, differ where, why. If a good one exists, copy its layout rather than inventing. No reference: write why. Check licence before copying code.
3. **Plan:** 4-6 named colours, typefaces, one-sentence layout, ASCII wireframe. If it resembles a generic AI page, revise.
4. Prefer ready accessible components to hand-made widgets. One shared component owns input state (modal open frees the pointer, close restores it), never each screen.

## Text
Default delete. A hint means the control failed; fix the control. Delete a sentence unless something breaks without it. No reassurance, no "only stored on this device", no caveats. Same verb for the same action everywhere. A waiting state shows who is working on what.

## Done means operated
Author checks first, then the reviewer:
- Each listed device, real clicks, touch and keys, starting from the state a user is really in.
- Assert the **effect** of each action, never only that no error appeared.
- Fix the whole class: every screen with the same control or state, not the one reported.
- Look at the screenshot at real size before saying done.

Facts measured 2026-11-02, Playwright 1.64 headless Chromium:
- Under pointer lock, `mouse.click` and `locator.click` on a button hit nothing and **raise no error**.
- Esc does not release the lock headless. `document.exitPointerLock()` is the only stand-in: say so each time, and test the state before it as well.
- Phone: Playwright `--device "iPhone 15"`, `hasTouch: true`. Playwright MCP `--caps vision` adds coordinate clicks.

## Independent review before merge
Spawn a fresh subagent that did not write the code, with: "Read `~/.claude/skills/ui/reviewer.md`; review branch `<b>`; write verdict to `<path the gate printed>`." Batch per step, not per commit.

## Gate (optional, per project)
Blocks merging UI paths without a verdict. In the repo:
```bash
echo 'apps/client/|packages/ui/' > "$(git rev-parse --git-common-dir)/ui-gate-paths"   # regex of UI paths
```
Add to the project's `.claude/settings.json`:
```json
{"hooks":{"PreToolUse":[{"matcher":"Bash","hooks":[{"type":"command","command":"python3 $HOME/.claude/skills/ui/scripts/ui_gate.py"}]}]}}
```
Verdict file first line: `PASS`, `FAIL`, or `USER-SKIP <their words>` when they need it now. It stays valid across a clean rebase.
