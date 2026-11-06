"""Stage A merge: one table of every war in Frames W and T with its AI first-pass class, polities and regions.
Lists duplicate candidates (same Wikipedia article in Frame W; shared names between Frames W and T) for a decision.
Never reads or writes any army figure: the inputs contain none.
Run: python -I -X utf8 merge_stageA.py"""
import csv
import glob
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")
OUT = os.path.join(D, "stageA_merged_ai_first_pass.csv")

frame = {r["id"]: r for r in csv.DictReader(open(os.path.join(D, "frame_w.csv"), encoding="utf-8"))}


def norm_regions(s):
    parts = [p.strip() for p in re.split(r";", s or "") if p.strip()]
    return "; ".join(parts) if parts else "unknown"


rows = []
for f in sorted(glob.glob(os.path.join(D, "stageA", "class_w_chunk*.csv"))):
    for r in csv.DictReader(open(f, encoding="utf-8")):
        w = frame[r["id"]]
        rows.append(dict(id=r["id"], frame="W", name=w["battle"], date=w["year"], year_num=w["year_num"],
                         source_or_article=w["article"], passages="", klass=r["class"], criterion=r["criterion"],
                         evidence=r["evidence"], side1_polity=r["side1_polity"], side1_region=norm_regions(r["side1_region"]),
                         side2_polity=r["side2_polity"], side2_region=norm_regions(r["side2_region"]), coder=r["coder"]))
for f, label in ((os.path.join(D, "stageA", "frame_t_bible.csv"), "Hebrew Bible"), (os.path.join(D, "stageA", "frame_t_other.csv"), None)):
    for r in csv.DictReader(open(f, encoding="utf-8")):
        rows.append(dict(id=r["id"], frame="T", name=r["episode"], date=r["purported_date"], year_num="",
                         source_or_article=label or r.get("text", ""), passages=r["passages"], klass=r["class"],
                         criterion=r["criterion"], evidence=r["evidence"], side1_polity=r["side1_polity"],
                         side1_region=norm_regions(r["side1_region"]), side2_polity=r["side2_polity"],
                         side2_region=norm_regions(r["side2_region"]), coder=r["coder"]))

with open(OUT, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

# Duplicate candidates
by_article = {}
for r in rows:
    if r["frame"] == "W":
        by_article.setdefault(r["source_or_article"], []).append(r["id"] + " " + r["name"] + " (" + r["date"] + ")")
print("Frame W entries sharing one article:")
for a, ids in by_article.items():
    if len(ids) > 1:
        print("  ", a, "->", ids)

STOP = {"battle", "of", "the", "siege", "sack", "war", "campaign", "and", "in", "against", "at", "first", "second", "third",
        "bc", "bce", "ad", "river", "expedition", "invasion", "raid", "muster", "s", "s'", "his", "on", "to", "a", "by"}
def words(s):
    return {x for x in re.findall(r"[a-zāīūṣṇṭḍ]+", (s or "").lower()) if x not in STOP and len(x) > 3}
print("Frame T episodes with a name shared with a Frame W battle:")
w_rows = [r for r in rows if r["frame"] == "W"]
for t in (r for r in rows if r["frame"] == "T"):
    tw = words(t["name"]) | words(t["side1_polity"]) | words(t["side2_polity"])
    hits = [x["id"] + " " + x["name"] for x in w_rows if words(x["name"]) & words(t["name"])]
    if hits:
        print("  ", t["id"], t["name"][:60], "->", hits[:4])

total = {}
for r in rows:
    total.setdefault(r["frame"], {}).setdefault(r["klass"], 0)
    total[r["frame"]][r["klass"]] += 1
print("Merged:", len(rows), "records ->", OUT)
print("By frame and class:", total)
