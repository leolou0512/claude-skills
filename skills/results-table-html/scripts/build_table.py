#!/usr/bin/env python
"""Build an interactive HTML results table from a CSV and an optional JSON config.

Usage:
    python build_table.py --csv results.csv --out out.html                     # automatic layout
    python build_table.py --csv results.csv --config table.json --out out.html

Config schema (every key optional):
{
  "title":   "My results table",
  "groups":  [["ident", "Run", ["run","model"]], ["quality", "Quality", ["accuracy","loss"]]],
  "ident_widths":     [80, 160],
  "higher_better":    ["accuracy"],
  "lower_better":     ["loss"],
  "rate_as_percent":  ["accuracy"],
  "no_highlight":     ["batch_size"],
  "formats":          {"loss": "f3", "accuracy": "pct2"}
}

The first group is the identifier group: its columns stay frozen at the left.
No "groups": leading text columns become identifiers, the rest one group.
CSV columns in no group are added to an "Other" group, never dropped.
No "higher_better" and no "lower_better": direction is guessed from column names
(loss, error, time ... lower; accuracy, f1, score ... higher), otherwise left out.
No "ident_widths": widths are estimated from the content.

Format codes: "f1".."f6" = N decimal places; "pctN" = value*100 + "%" with N dp;
"pctNraw" = already a percent, N dp, append "%"; "int" = integer; "sci3" = scientific.
Anything not listed gets "%.4g".
"""
import argparse, csv, json, math, re, sys
from html import escape
from pathlib import Path

LOWER = {"loss", "error", "err", "mae", "mse", "rmse", "nll", "ppl", "perplexity", "fid",
         "latency", "runtime", "time", "cost", "dist", "distance", "divergence"}
HIGHER = {"acc", "accuracy", "precision", "recall", "f1", "auc", "score", "bleu", "rouge",
          "success", "top1", "top5"}


# ---------- formatting -----------------------------------------------------

def fmt_value(code, f):
    if code == "int":   return f"{int(f)}"
    if code == "sci3":  return f"{f:.3e}"
    if code.startswith("pct") and code.endswith("raw"):
        n = int(code[3:-3]); return f"{f:.{n}f}%"
    if code.startswith("pct"):
        n = int(code[3:]);   return f"{f*100:.{n}f}%"
    if code.startswith("f"):
        n = int(code[1:]);   return f"{f:.{n}f}"
    return f"{f:.4g}"


def to_float(raw):
    try:
        f = float(raw)
    except (ValueError, TypeError):
        return None
    return f if math.isfinite(f) else None


def display_value(col, raw, formats, rate_as_percent):
    if raw in (None, ""): return "", None
    f = to_float(raw)
    if f is None: return str(raw), None
    sort_key = f * 100.0 if col in rate_as_percent else f
    code = formats.get(col)
    if code:
        return fmt_value(code, f), sort_key
    if col in rate_as_percent:
        return f"{f*100:.2f}%", sort_key
    return f"{f:.4g}", sort_key


def arrow(col, hi, lo):
    if col in hi: return " ↑"
    if col in lo: return " ↓"
    return ""


# ---------- automatic layout -----------------------------------------------

def guess_direction(col):
    words = set(re.split(r"[^a-z0-9]+", col.lower()))
    lo, hi = bool(words & LOWER), bool(words & HIGHER)
    if lo == hi: return None
    return "lower" if lo else "higher"


def auto_groups(cols, rows):
    def is_text(c):
        return all(to_float(r.get(c)) is None for r in rows if r.get(c) not in (None, ""))
    ident = []
    for c in cols[:3]:
        if not is_text(c): break
        ident.append(c)
    ident = ident or cols[:1]
    rest = [c for c in cols if c not in ident]
    return [["ident", "Run", ident]] + ([["results", "Results", rest]] if rest else [])


def auto_width(col, rows):
    n = max([len(col)] + [len(r.get(col) or "") for r in rows])
    return max(60, min(320, 7 * n + 18))


# ---------- main -----------------------------------------------------------

def build(csv_path, cfg, out_path):
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        all_cols = reader.fieldnames or []
    if not all_cols:
        sys.exit(f"{csv_path}: no header row")

    groups = [list(g) for g in (cfg.get("groups") or auto_groups(all_cols, rows))]
    grouped = [c for g in groups for c in g[2]]
    unknown = [c for c in grouped if c not in all_cols]
    if unknown:
        print(f"warning: config columns not in the CSV, skipped: {unknown}", file=sys.stderr)
    missing = [c for c in all_cols if c not in grouped]
    if missing:
        print(f"warning: CSV columns in no group, added as 'Other': {missing}", file=sys.stderr)
        groups.append(["other", "Other", missing])

    listed_ident = groups[0][2]
    widths = cfg.get("ident_widths")
    if widths is not None and len(widths) != len(listed_ident):
        sys.exit(f"ident_widths has {len(widths)} entries, identifier group has "
                 f"{len(listed_ident)} columns")
    widths = widths or [auto_width(c, rows) for c in listed_ident]
    width = {c: w for c, w in zip(listed_ident, widths) if c in all_cols}
    ident_cols = [c for c in listed_ident if c in all_cols]

    hi, lo = cfg.get("higher_better"), cfg.get("lower_better")
    if hi is None and lo is None:
        guess = {c: guess_direction(c) for c in all_cols if c not in ident_cols}
        hi = [c for c, d in guess.items() if d == "higher"]
        lo = [c for c, d in guess.items() if d == "lower"]
    higher_better, lower_better = set(hi or []), set(lo or [])
    no_highlight  = set(cfg.get("no_highlight", []))
    rate_as_pct   = set(cfg.get("rate_as_percent", []))
    formats       = cfg.get("formats", {})
    title         = cfg.get("title") or Path(csv_path).stem

    # Column names never reach CSS or JS: every column and group gets a safe id.
    ordered_cols, col_to_group, seen = [], {}, set()
    for gi, (_gid, _label, cols) in enumerate(groups):
        for c in cols:
            if c in all_cols and c not in seen:
                ordered_cols.append(c); col_to_group[c] = f"g{gi}"; seen.add(c)
    cid = {c: f"c{i}" for i, c in enumerate(ordered_cols)}
    numeric = {c: c not in ident_cols and any(to_float(r.get(c)) is not None for r in rows)
               for c in ordered_cols}

    best_val = {}
    for c in ordered_cols:
        if c in no_highlight: continue
        if c not in higher_better and c not in lower_better: continue
        nums = [v for v in (display_value(c, r.get(c), formats, rate_as_pct)[1]
                            for r in rows) if v is not None]
        if nums:
            best_val[c] = min(nums) if c in lower_better else max(nums)

    left, off = {}, 0
    for c in ident_cols:
        left[c] = off; off += width[c]
    sticky_left_css = "\n".join(
        f"th.{cid[c]},td.{cid[c]}{{position:sticky;left:{left[c]}px;z-index:6;background:var(--cell);"
        f"width:{width[c]}px;min-width:{width[c]}px;max-width:{width[c]}px;overflow:hidden;"
        f"text-overflow:ellipsis{';box-shadow:2px 0 4px rgba(0,0,0,.15)' if c == ident_cols[-1] else ''}}}"
        for c in ident_cols)
    sticky_header_left = ",".join(f"thead tr.col-header th.{cid[c]}" for c in ident_cols)

    H = [
        "<!doctype html><html><head><meta charset='utf-8'>",
        "<meta name='viewport' content='width=device-width,initial-scale=1'>",
        f"<title>{escape(title)}</title>",
        "<style>",
        ":root{--bg:#fafafa;--fg:#222;--cell:#fff;--line:#ddd;--head:#eee;--headline:#aaa;--band:#445;--bandident:#222;--hover:#fffbe6;--best:#d4edda;--bestfg:#155724;--btn:#eef3fa;--btnhover:#dde7f5;--muted:#888;--accent:#06c}",
        "@media (prefers-color-scheme:dark){:root{--bg:#16181c;--fg:#ddd;--cell:#1f2228;--line:#353a44;--head:#2a2e36;--headline:#4a505c;--band:#3a4050;--bandident:#0e1013;--hover:#2e2c20;--best:#1d3b27;--bestfg:#8fd19e;--btn:#2a3140;--btnhover:#36405a;--muted:#999;--accent:#6af}}",
        "html,body{height:100%}",
        "body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;font-size:13px;margin:0;background:var(--bg);color:var(--fg);display:flex;flex-direction:column}",
        ".controls{background:var(--cell);padding:10px 14px;border-bottom:1px solid var(--headline);display:flex;align-items:center;gap:12px;flex-wrap:wrap}",
        ".controls h1{font-size:14px;margin:0 8px 0 0;font-weight:600}",
        ".controls .hint{color:var(--muted);font-size:12px}",
        ".group-toggle{padding:5px 10px;border:1px solid var(--headline);background:var(--btn);color:var(--fg);border-radius:4px;cursor:pointer;font-size:12px}",
        ".group-toggle.collapsed{opacity:.6;text-decoration:line-through}",
        ".group-toggle:hover{background:var(--btnhover)}",
        ".scroll{flex:1;min-height:0;overflow:auto}",
        "table{border-collapse:separate;border-spacing:0;margin:0;width:max-content}",
        "thead tr.group-header th{background:var(--band);color:#fff;font-weight:600;border:1px solid var(--headline);padding:6px 8px;cursor:pointer;user-select:none;position:sticky;top:0;z-index:11}",
        "thead tr.group-header th.ident{background:var(--bandident);cursor:default;left:0;z-index:16}",
        "thead tr.col-header th{background:var(--head);border:1px solid var(--headline);padding:5px 8px;cursor:pointer;user-select:none;position:sticky;top:var(--gh,32px);z-index:10;font-weight:500;text-align:left;white-space:nowrap}",
        "thead tr.col-header th:hover{background:var(--btnhover)}",
        "thead tr.col-header th.sorted-asc::after{content:' \\25B2';color:var(--accent)}",
        "thead tr.col-header th.sorted-desc::after{content:' \\25BC';color:var(--accent)}",
        ".arr{color:var(--muted);font-weight:400;font-size:11px}",
        "tbody td{border:1px solid var(--line);padding:4px 7px;white-space:nowrap;background:var(--cell)}",
        "tbody td.num{text-align:right;font-variant-numeric:tabular-nums}",
        "tbody td.best{background:var(--best);font-weight:600;color:var(--bestfg)}",
        "tbody tr:hover td:not(.best){background:var(--hover)}",
        sticky_left_css,
        f"{sticky_header_left}{{z-index:15}}" if ident_cols else "",
        ".hidden{display:none}",
        "</style></head><body>",
        "<div class='controls'>",
        f"<h1>{escape(title)}</h1><span class='hint'>click a column to sort, a group to hide it</span>",
    ]
    for gi, (_gid, gname, cols) in enumerate(groups):
        if gi == 0 or not any(c in ordered_cols for c in cols): continue
        H.append(f"<button class='group-toggle' data-group='g{gi}'>{escape(gname)}</button>")
    H.append("</div><div class='scroll'><table id='tbl'>")

    H.append("<thead><tr class='group-header'>")
    for gi, (_gid, gname, cols) in enumerate(groups):
        present = [c for c in ordered_cols if col_to_group[c] == f"g{gi}"]
        if not present: continue
        klass = "ident" if gi == 0 else ""
        H.append(f"<th class='{klass}' colspan='{len(present)}' data-group='g{gi}'>{escape(gname)}</th>")
    H.append("</tr><tr class='col-header'>")
    for c in ordered_cols:
        arr = arrow(c, higher_better, lower_better)
        arr_html = f"<span class='arr'>{arr}</span>" if arr else ""
        H.append(
            f"<th class='{cid[c]}' data-group='{col_to_group[c]}' data-numeric='{int(numeric[c])}' "
            f"title='{escape(c)}'>{escape(c)}{arr_html}</th>")
    H.append("</tr></thead><tbody>")

    for r in rows:
        H.append("<tr>")
        for c in ordered_cols:
            disp, fv = display_value(c, r.get(c), formats, rate_as_pct)
            classes = [cid[c]]
            if fv is not None: classes.append("num")
            if fv is not None and c in best_val and fv == best_val[c]:
                classes.append("best")
            if numeric[c]:
                sk = "" if fv is None else f"{fv:.10g}"
            else:
                sk = disp
            tip = f" title='{escape(disp)}'" if c in ident_cols else ""
            H.append(f"<td class='{' '.join(classes)}' data-group='{col_to_group[c]}' "
                     f"data-sort='{escape(sk)}'{tip}>{escape(disp)}</td>")
        H.append("</tr>")
    H.append("</tbody></table></div>")

    H.append("""
<script>
const tbl = document.getElementById('tbl');
// The column-header row sticks just below the group banner, whatever its height.
const setGh = () => document.documentElement.style.setProperty(
  '--gh', tbl.tHead.rows[0].getBoundingClientRect().height + 'px');
setGh(); addEventListener('resize', setGh);
const headers = tbl.querySelectorAll('thead tr.col-header th');
let sortState = {col: null, dir: 1};
headers.forEach((th, idx) => {
  th.addEventListener('click', () => {
    const dir = (sortState.col === idx) ? -sortState.dir : 1;
    sortState = {col: idx, dir};
    headers.forEach(h => h.classList.remove('sorted-asc', 'sorted-desc'));
    th.classList.add(dir === 1 ? 'sorted-asc' : 'sorted-desc');
    const isNum = th.dataset.numeric === '1';
    const body = tbl.tBodies[0];
    const rows = Array.from(body.rows);
    rows.sort((a, b) => {
      const av = a.cells[idx].dataset.sort, bv = b.cells[idx].dataset.sort;
      if (av === '' || bv === '') return (av === '') - (bv === '');  // blanks last in both directions
      if (isNum) return (parseFloat(av) - parseFloat(bv)) * dir;
      return av.localeCompare(bv, undefined, {numeric: true}) * dir;
    });
    rows.forEach(r => body.appendChild(r));
  });
});
document.querySelectorAll('.group-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const g = btn.dataset.group;
    const collapsed = btn.classList.toggle('collapsed');
    tbl.querySelectorAll(`[data-group='${g}']`).forEach(el => el.classList.toggle('hidden', collapsed));
  });
});
tbl.querySelectorAll('thead tr.group-header th').forEach(th => {
  const g = th.dataset.group;
  if (!g || th.classList.contains('ident')) return;
  th.addEventListener('click', () => {
    document.querySelector(`.group-toggle[data-group='${g}']`).click();
  });
});
</script>
</body></html>
""")
    Path(out_path).write_text("\n".join(H), encoding="utf-8")
    print(f"Wrote {out_path}  ({Path(out_path).stat().st_size//1024} KB): {len(rows)} rows, "
          f"{len(ordered_cols)} columns, frozen: {ident_cols}, "
          f"higher better: {sorted(higher_better)}, lower better: {sorted(lower_better)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--config", help="optional JSON config (see header)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cfg = json.loads(Path(a.config).read_text()) if a.config else {}
    build(a.csv, cfg, a.out)


if __name__ == "__main__":
    main()
