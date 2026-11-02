---
name: memtree
description: Long-horizon project memory as a folder tree that keeps fine detail compaction would lose. Each folder describes itself and what lives below it, so a session reads titles first and expands only relevant branches. Use before any /compact, when resuming after compaction, when context nears 400-500k, when picking up an area of a long project, or when the user says memory tree, memtree, "save before compact", "what did we decide about X".
---

# Memory tree

Compaction replaces detail with generalised summaries. The tree keeps the detail. Compact summary is a lead; the tree is the source.

```
memory/
  NODE.md               what this tree holds
  voice/
    NODE.md             description of appropriate detail, what is below
    transcription/
      NODE.md
      2026-10-29_model_compare.html
      leo_comments.md
```
A node is a folder. Any file may live in it: markdown, HTML, reports, the user's comments, logs. To add a layer, move a folder inside another; links are relative so nothing breaks.

**NODE.md:** first line = one-line description. Then detail fitting that level: top nodes a few lines, deeper nodes more. Note contents with `- name: note`.

**Read the tree:** `python3 ~/.claude/skills/memtree/memtree.py <root> --depth 2`. Expand by calling it on a node, then open files.

## Reading
- Before work on an area, and after any compaction: view the tree, open every branch touching the task.
- Tree and summary disagree: the tree wins. Check code or git if it matters.

## Before compact, the session itself writes
Do this while the detail is still in context; a later session or hook can't recover it.
1. View the tree. Update existing nodes rather than adding parallels.
2. Copy **exact**: the user's words, decisions and why, rejected options and why, numbers, error strings, commands, `file:line`, commit ids. Summarise only reasoning.
3. Keep source: put the report or log in the node, or a commit or file link. A conclusion without its source misleads once stale.
4. Changed decision: mark old text `superseded by <path>`; never silently overwrite.
5. Skip what code, git or CLAUDE.md already record.

Then log and ask for `/compact`.

## Upkeep
A node's folder gets crowded → group into subfolders and rewrite descriptions upward. Rewrite from the files, never from an older summary. Status is untested: it hasn't yet been compared against compaction alone.
