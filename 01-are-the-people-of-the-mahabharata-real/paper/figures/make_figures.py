"""Figures for the paper. Palette: validated categorical slots 1-2 (blue #2a78d6, orange #eb6834)."""
import json, csv, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
H = os.path.dirname(os.path.abspath(__file__))
BLUE, ORANGE, INK, MUTED, GRID = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"font.family": "serif", "font.size": 8, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.5, "axes.axisbelow": True})
d = json.load(open(f"{H}/v3_t1_null.json"))

# Fig: permutation null
null, obs = d["null"], d["observed"]
fig, ax = plt.subplots(figsize=(3.4, 1.9))
vals = list(range(min(null), max(null) + 1))
ax.bar(vals, [null.count(v) for v in vals], width=0.8, color=BLUE, label="Shuffled relatives (1,000 runs)")
ax.axvline(obs, color=ORANGE, lw=2, label=f"Observed ({obs})")
p99 = sorted(null)[989]
ax.axvline(p99, color=MUTED, lw=1, ls="--", label=f"Null 99th percentile ({p99})")
ax.set_xlabel("Grade 2+ matches"); ax.set_ylabel("Runs"); ax.grid(axis="x", visible=False)
ax.set_xticks(range(0, 23, 2)); ax.set_xlim(-0.5, 22.5)
ax.legend(frameon=False, fontsize=7, loc="upper center", bbox_to_anchor=(0.62, 1.0))
fig.tight_layout(); fig.savefig(f"{H}/fig_null.pdf"); plt.close(fig)

# Fig: versions
fig, (a1, a2) = plt.subplots(1, 2, figsize=(3.4, 1.8))
v = ["v1", "v2", "v3"]; fp = [1.30, 0.60, 0.48]
a1.bar(v, fp, width=0.55, color=BLUE)
a1.axhline(1.0, color=ORANGE, lw=1.5, ls="--"); a1.text(2.35, 1.03, "1% limit", ha="right", va="bottom", fontsize=7, color=INK)
for i, x in enumerate(fp): a1.text(i, x + 0.03, f"{x:.2f}%", ha="center", fontsize=7, color=INK)
a1.set_ylabel("T2 false positives (%)"); a1.set_ylim(0, 1.6); a1.grid(axis="x", visible=False)
prec, rec = [0.62, 0.71, 0.76], [0.83, 0.83, 0.84]
xs = range(3); w = 0.36
a2.bar([x - w/2 for x in xs], prec, w, color=BLUE, label="Precision")
a2.bar([x + w/2 for x in xs], rec, w, color=ORANGE, label="Recall")
a2.set_xticks(list(xs)); a2.set_xticklabels(v); a2.set_ylim(0, 1.25); a2.set_yticks([0, .25, .5, .75, 1]); a2.grid(axis="x", visible=False)
a2.legend(frameon=False, fontsize=7, loc="upper center", ncol=2, handlelength=1, columnspacing=0.8)
fig.tight_layout(); fig.savefig(f"{H}/fig_versions.pdf"); plt.close(fig)

# Fig: evidence bits per match, coloured by hand review
rev = {r["person"]: r["reviewed_grade"] for r in csv.DictReader(open(f"{H}/../../results/clerical_review.csv"))}
ok = lambda g: g.startswith(("Grade", "Same figure"))
rows = sorted(d["bits"], key=lambda r: r[1])
names = [r[0].replace(" (brother of Janamejaya)", " (brother)") for r in rows]
cols = [BLUE if ok(rev.get(r[0], "Grade")) else ORANGE for r in rows]
fig, ax = plt.subplots(figsize=(3.4, 3.4))
ax.barh(names, [min(r[1], 40) for r in rows], color=cols, height=0.7)
ax.axvline(3.32, color=MUTED, lw=1, ls="--")
ax.set_xlabel("Evidence W (bits, capped at 40)"); ax.grid(axis="y", visible=False)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=BLUE, label="Identity confirmed"), Patch(color=ORANGE, label="Not confirmed")],
          frameon=False, fontsize=7, loc="lower right")
fig.tight_layout(); fig.savefig(f"{H}/fig_bits.pdf"); plt.close(fig)
print("figures written")
