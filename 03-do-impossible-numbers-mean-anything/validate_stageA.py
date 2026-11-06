"""Stage A check: each coded file matches its input, uses valid classes, is labelled as an AI first pass,
and contains nothing that looks like an army figure. Prints only ids and the matched pattern's kind, never the text.
Run: python -I -X utf8 validate_stageA.py <data/stageA folder>"""
import csv
import glob
import os
import re
import sys

folder = sys.argv[1]
FORCE_WORDS = r"(men|troops|soldiers|warriors|infantry|foot|horse|horsemen|cavalry|chariots?|elephants?|ships?|vessels|army of|strong|killed|slain|dead|casualt)"
SUSPECT = [
    ("comma-grouped number", re.compile(r"\b\d{1,3}(,\d{3})+\b(?!\s*(BC|BCE|AD|CE))")),
    ("number next to a force word", re.compile(r"\b\d[\d,.]*\s*" + FORCE_WORDS + r"\b|\b" + FORCE_WORDS + r"\s*(of\s*)?\d", re.I)),
    ("large bare number", re.compile(r"\b\d{5,}\b")),
]
ok = True
for out in sorted(glob.glob(os.path.join(folder, "class_w_chunk*.csv")) + glob.glob(os.path.join(folder, "frame_t_*.csv"))):
    rows = list(csv.DictReader(open(out, encoding="utf-8")))
    name = os.path.basename(out)
    problems = []
    m = re.search(r"chunk(\d)", name)
    if m:
        inp = [r["id"] for r in csv.DictReader(open(os.path.join(folder, f"frame_w_chunk{m.group(1)}.csv"), encoding="utf-8"))]
        if [r["id"] for r in rows] != inp:
            problems.append("ids don't match the input in order")
    for r in rows:
        if r.get("class") not in ("A", "U", "M"):
            problems.append(f"{r['id']}: class '{r.get('class')}'")
        if r.get("coder") != "AI first pass (Claude)":
            problems.append(f"{r['id']}: coder label")
        text = " ".join(v for k, v in r.items() if k not in ("id",) and v)
        for kind, rx in SUSPECT:
            if rx.search(text):
                problems.append(f"{r['id']}: {kind} (review by hand)")
    counts = {c: sum(1 for r in rows if r.get("class") == c) for c in "AUM"}
    print(f"{name}: {len(rows)} rows, {counts}, " + ("clean" if not problems else f"{len(problems)} flags: {problems[:12]}"))
    ok &= not problems
sys.exit(0 if ok else 1)
