#!/usr/bin/env python3
"""Print a memory tree: every folder with its description, like `tree` with notes.
Usage: memtree.py ROOT [--depth N]   (default 2; ROOT may be any node; deeper = call again on that node)
NODE.md in a folder: first non-blank line (minus #) is its description; `- name: note` lines describe its contents."""
import os, re, sys

args = sys.argv[1:]
depth = 2
if "--depth" in args:
    i = args.index("--depth")
    depth = int(args[i + 1])
    del args[i : i + 2]
if len(args) != 1:
    sys.exit(__doc__)
root = os.path.abspath(os.path.expanduser(args[0]))
if not os.path.isdir(root):
    print(f"memtree: no tree at {root}")
    sys.exit(0)

def read_node(path):
    try:
        lines = open(os.path.join(path, "NODE.md"), errors="replace").read().splitlines()
    except OSError:
        return "(no description)", {}
    title = next((l.lstrip("# ").strip() for l in lines if l.strip()), "(no description)")
    notes = {}
    for l in lines:
        m = re.match(r"\s*-\s+`?([^`:]+?)/?`?:\s+(.*)", l)
        if m:
            notes[m.group(1)] = m.group(2)
    return title, notes

def count(path):
    return sum(len(fs) for _, _, fs in os.walk(path))

def show(path, level, prefix):
    title, notes = read_node(path)
    names = sorted(n for n in os.listdir(path) if n != "NODE.md" and not n.startswith("."))
    names.sort(key=lambda n: not os.path.isdir(os.path.join(path, n)))
    for i, n in enumerate(names):
        p = os.path.join(path, n)
        last = i == len(names) - 1
        branch = prefix + ("└─ " if last else "├─ ")
        if os.path.isdir(p):
            print(f"{branch}{n}/  {read_node(p)[0]}" + (f"  [{count(p)} files]" if level >= depth else ""))
            if level < depth:
                show(p, level + 1, prefix + ("   " if last else "│  "))
        else:
            kb = os.path.getsize(p) / 1024
            print(f"{branch}{n}  {kb:.0f}KB" + (f"  {notes[n]}" if n in notes else ""))

print(f"{root}/  {read_node(root)[0]}")
show(root, 1, "")
