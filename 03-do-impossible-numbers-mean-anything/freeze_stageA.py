"""Stage A freeze (Amendment 2): merge wars held in both frames, drop Frame T counts that are not armies,
flag conflicts, and draw the author's blind recode sample (random 30% plus every conflict, seed 20261106).
No army figure is read or written anywhere.
Run: python -I -X utf8 freeze_stageA.py"""
import csv
import os
import random
import re

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")
rows = {r["id"]: r for r in csv.DictReader(open(os.path.join(D, "stageA_merged_ai_first_pass.csv"), encoding="utf-8"))}

# Amendment 2, point 3: Frame T counts that are not armies
DROP = {
    "T-OT-008": "only count is of champions (Rome-Alba, the Horatii)",
    "T-HB-020": "contest of champions at the pool of Gibeon",
    "T-OT-014": "numeral is part of an epithet (takeru), not a count",
    "T-OT-015": "numeral is part of an epithet (takeru), not a count",
    "T-OT-016": "stock formula for 'the whole army'",
}
# Amendment 2, point 4: the same war in both frames (Frame W id kept as the record id)
SAME_WAR = [("W035", "T-HB-010"), ("W048", "T-HB-006"), ("W415", "T-OT-005"), ("W093", "T-OT-009"),
            ("W051", "T-HB-013"), ("W057", "T-HB-025"), ("W045", "T-OT-007"), ("W056", "T-HB-024")]
# Frame W entries that may be one battle listed twice
MAYBE_TWICE = [("W387", "W389"), ("W751", "W758"), ("W398", "W399"), ("W446", "W450")]

records, conflicts = [], []
absorbed = {t for _, t in SAME_WAR}
for rid, r in rows.items():
    if rid in absorbed:
        continue
    rec = dict(record_id=rid, member_ids=rid, **{k: v for k, v in r.items() if k != "id"})
    rec["status"] = "dropped" if rid in DROP else "included"
    rec["drop_reason"] = DROP.get(rid, "")
    rec["conflict"] = ""
    records.append(rec)
by_id = {r["record_id"]: r for r in records}
for w, t in SAME_WAR:
    rec, other = by_id[w], rows[t]
    rec["member_ids"] = f"{w};{t}"
    rec["passages"] = other["passages"]
    if rec["klass"] != other["klass"]:
        rec["conflict"] = f"coders differ: {w} {rec['klass']}, {t} {other['klass']}"
        conflicts.append(w)
for a, b in MAYBE_TWICE:
    for x, y in ((a, b), (b, a)):
        by_id[x]["conflict"] = f"may be the same battle as {y}"
    conflicts += [a, b]

fields = ["record_id", "member_ids", "frame", "name", "date", "year_num", "source_or_article", "passages", "status",
          "drop_reason", "conflict", "klass", "criterion", "evidence", "side1_polity", "side1_region",
          "side2_polity", "side2_region", "coder"]
with open(os.path.join(D, "stageA_frozen_ai_first_pass.csv"), "w", newline="", encoding="utf-8") as fh:
    wr = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
    wr.writeheader()
    wr.writerows(records)

included = sorted(r["record_id"] for r in records if r["status"] == "included")
rng = random.Random(20261106)
k = round(0.30 * len(included))
sample = set(rng.sample(included, k)) | set(conflicts)
order = sorted(sample)
rng2 = random.Random(20261106 + 1)
rng2.shuffle(order)  # so conflict cases are not identifiable by position

os.makedirs(os.path.join(D, "recode"), exist_ok=True)
with open(os.path.join(D, "recode", "author_blind_recode_sheet.csv"), "w", newline="", encoding="utf-8") as fh:
    wr = csv.writer(fh)
    wr.writerow(["record_id", "name", "date", "where_to_look", "passages", "your_class (A/U/M)", "your_criterion", "your_evidence_note"])
    for rid in order:
        r = by_id[rid]
        where = ("https://en.wikipedia.org/wiki/" + r["source_or_article"].replace(" ", "_")) if r["frame"] == "W" else r["source_or_article"]
        clean = lambda s: " ".join(re.sub(r"\[[^\]]*\]", "", s or "").split())  # no coder notes in the blind sheet
        wr.writerow([rid, clean(r["name"]), clean(r["date"]), where, clean(r["passages"]), "", "", ""])

n_inc = len(included)
cls = {c: sum(1 for r in records if r["status"] == "included" and r["klass"] == c) for c in "AUM"}
print(f"records: {len(records)} (included {n_inc}, dropped {len(records) - n_inc}); AI classes among included: {cls}")
print(f"conflicts for the author: {len(set(conflicts))}; random 30%: {k}; recode sheet: {len(order)} rows")
