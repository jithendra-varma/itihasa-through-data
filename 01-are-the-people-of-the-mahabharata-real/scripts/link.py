"""Record linkage of Mahabharata people to Vedic Index persons, with battle tests T1-T4.
Implements PROTOCOL.md exactly. Run: python3 scripts/link.py"""
import json, math, os, random, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import norm, key, skeleton
D = os.path.join(os.path.dirname(__file__), "..")
EPIC = json.load(open(f"{D}/data/epic_people.json"))
VED = json.load(open(f"{D}/data/vedic_persons.json"))
BY_NAME = {e["name"]: e for e in EPIC}

BASE = dict(pat=(0.85, 0.01), rel=(0.80, 0.01), role=(0.90, 0.30), people=(0.90, 0.20))
PRIOR = 1 / 10
GRADES = [(0.95, "Grade 3"), (0.50, "Grade 2"), (0.05, "Weak"), (0.0, "Not identified")]
CONTROLS = ["Bharata", "Yayati", "Pururavas", "Mandhatri", "Nala", "Uddalaka", "Shvetaketu", "Yajnavalkya", "Janaka"]

def stem(w):
    return re.sub(r"[aeiou]+$", "", w)
for v in VED:                                         # precompute Vedic token stems
    v["stems"] = {stem(t) for t in norm(v["entry"]).split() if len(t) >= 4}   # Amendment 1: own entry only
    v["sk2"] = skeleton(v["second"]).replace("h", "") if v["second"] else ""

# Amendment 2: value-specific chance agreement (Fellegi & Sunter 1969, frequency-based weights).
# u for a relative or people name = share of Vedic entries containing it (with +1 smoothing), floor 0.001.
N_ENT = sum(1 for v in VED if v["entry"])
DF = {}
for v in VED:
    if v["entry"]:
        for t in v["stems"]: DF[t] = DF.get(t, 0) + 1
def u_of(stem_):
    return max(0.001, (DF.get(stem_, 0) + 1) / (N_ENT + 2))

def names_of(e):
    return [e["name"].split(" (")[0]] + e["alt"]
def relatives(e):
    """Relatives and associates, each with its alternative names from the epic dataset."""
    out = []
    for r in e["father"] + e["mother"] + e["siblings"] + e["spouses"] + e["children"] + e["associates"]:
        alts = [r] + BY_NAME.get(r, {}).get("alt", [])
        out.append((r, [a for a in alts]))
    return out
def parents(e):
    out = []
    for r in e["father"] + e["mother"]:
        out += [r] + BY_NAME.get(r, {}).get("alt", [])
    return out

def close(a, b):
    if a == b: return True
    if len(a) < 8 or abs(len(a) - len(b)) > 1: return False
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]: i += 1
    return a[i+1:] == b[i+1:] or a[i:] == b[i+1:] or a[i+1:] == b[i:]

def candidates(e):
    """Amendment 1: names shorter than 4 letters (after normalising) must match exactly;
    one-letter tolerance (for OCR) only for names of 8+ letters."""
    out = []
    for n in names_of(e):
        k, full = key(n), (norm(n).split() or [""])[0]
        if not k: continue
        for v in VED:
            vfull = (norm(v["head"]).split() or [""])[0]
            if len(k) < 4:
                hit = vfull == full
            elif len(k) >= 8:
                hit = close(v["key"], k)
            else:
                hit = v["key"] == k or v["key"].replace("l", "i") == k
            if hit and v not in out: out.append(v)
    return out

def starts_like(sub, s):
    """Amendment 3: a patronymic is built on the parent's name, so it must START with the parent's
    consonant skeleton (3+ consonants); one OCR error allowed when the skeleton has 4+ consonants."""
    if len(sub) < 2: return False
    if s.startswith(sub): return True             # 2-3 consonants: exact start only (Aruni -> Aruneya)
    return len(sub) >= 4 and any(close_any(sub, s[:L]) for L in (len(sub) - 1, len(sub), len(sub) + 1))

def fuzzy_in(sub, s):
    """sub occurs in s, allowing one OCR error when sub has 4+ consonants."""
    if sub in s: return True
    if len(sub) < 4: return False
    for L in (len(sub) - 1, len(sub), len(sub) + 1):
        for i in range(0, max(0, len(s) - L) + 1):
            if close_any(sub, s[i:i + L]): return True
    return False
def close_any(a, b):
    if abs(len(a) - len(b)) > 1: return False
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]: i += 1
    return a[i+1:] == b[i+1:] or a[i:] == b[i+1:] or a[i+1:] == b[i:]

def w(field, agree, P):
    m, u = P[field]
    return math.log2(m / u) if agree else math.log2((1 - m) / (1 - u))

def score(e, v, P, rels=None, pars=None):
    """Return (bits, disqualified_reason, detail)."""
    rels = relatives(e) if rels is None else rels
    pars = parents(e) if pars is None else pars
    bits, det = 0.0, []
    # R3: a god or mythic being where the epic has a human
    if v["role"] == "divine" and e["role"] != "other":
        return -99, "Vedic namesake is a god or mythic being", det
    # patronymic (second element of the Vedic name)
    if v["sk2"] and len(v["sk2"]) >= 2:
        own = [skeleton(n).replace("h", "") for n in names_of(e)]
        ppl = [skeleton(p).replace("h", "") for p in e["people"]]
        psk = [skeleton(p).replace("h", "") for p in pars]
        if any(starts_like(s, v["sk2"]) for s in psk):
            bits += w("pat", True, P); det.append(f"patronymic {v['second']} = parent")
        elif any(s and (s in v["sk2"] or v["sk2"] in s) for s in own + ppl):
            det.append(f"second name {v['second']} = own epithet or people")
        elif pars:
            return -99, f"patronymic {v['second']} does not match epic parent(s) {', '.join(e['father'] + e['mother'])}", det
    # relatives and associates named in the Vedic passages
    found = []
    m_rel = P["rel"][0]; scale = P["rel"][1] / 0.01      # T4 moves u by scaling the frequency-based u
    for r, alts in rels:
        if r in [p for p in e["father"] + e["mother"]] and any("patronymic" in d for d in det):
            continue                                   # father already counted via patronymic
        selfnames = {stem(t) for t in norm(v["name"]).split()}          # Amendment 3: an entry never names itself
        hit = [stem(norm(a).split()[0]) for a in alts if len(norm(a)) >= 5 and stem(norm(a).split()[0]) in v["stems"]
               and stem(norm(a).split()[0]) not in selfnames]
        if hit:
            found.append(r)
            bits += math.log2(m_rel / min(0.5, u_of(hit[0]) * scale))
    if found: det.append("relatives named: " + ", ".join(found))
    # role
    er = "royal" if e["role"] in ("royal", "warrior") else e["role"]
    if v["role"] in ("royal", "sage", "woman") and er in ("royal", "sage", "woman"):
        agree = v["role"] == er
        bits += w("role", agree, P); det.append(f"role {v['role']} {'=' if agree else '!='} {er}")
    # people
    pl = [stem(norm(p)) for p in e["people"] if len(norm(p)) >= 4]
    hitp = [x for x in pl if x in v["stems"]]
    if hitp:
        m_p = P["people"][0]; scale = P["people"][1] / 0.20
        bits += math.log2(m_p / min(0.9, u_of(hitp[0]) * scale * 5)); det.append("people named")
    return bits, None, det

def verdict(bits, dq, prior=PRIOR):
    if dq: return 0.0, "Disqualified"
    lr = 2 ** max(min(bits, 200), -200)
    p = prior * lr / (1 + prior * lr)
    return p, next(g for t, g in GRADES if p >= t)

def run(P=BASE, prior=PRIOR, perm=None):
    """Best candidate per epic person. perm: optional dict name->relatives list (for T1)."""
    out = {}
    for e in EPIC:
        rels = perm[e["name"]][0] if perm else None
        pars = perm[e["name"]][1] if perm else None
        best = None
        for v in CANDS[e["name"]]:
            b, dq, det = score(e, v, P, rels, pars)
            p, g = verdict(b, dq, prior)
            row = dict(person=e["name"], vedic=v["name"], vedic_role=v["role_word"], bits=round(b, 1) if not dq else None,
                       p=round(p, 3), grade=g, why=dq or "; ".join(det))
            rank = (p, 0 if dq else 1, b)
            if best is None or rank > best[0]: best = (rank, row)
        out[e["name"]] = best[1] if best else dict(person=e["name"], vedic="", vedic_role="", bits=None, p=0.0,
                                                    grade="No Vedic candidate", why="")
    return out

CANDS = {e["name"]: candidates(e) for e in EPIC}
ok = lambda g: g in ("Grade 3", "Grade 2")

if __name__ == "__main__":
    random.seed(1)
    main = run()
    n_obs = sum(ok(r["grade"]) for r in main.values())
    report = {"n_epic": len(EPIC), "n_vedic": len(VED), "observed_grade2plus": n_obs}

    # T1 permutation null: shuffle relatives and parents between epic people
    names = [e["name"] for e in EPIC]
    pool = [(relatives(e), parents(e)) for e in EPIC]
    null = []
    for i in range(1000):
        sh = pool[:]; random.shuffle(sh)
        res = run(perm=dict(zip(names, sh)))
        null.append(sum(ok(r["grade"]) for r in res.values()))
    null.sort()
    report["T1"] = dict(null_mean=sum(null) / len(null), null_p99=null[989], null_max=null[-1],
                        p_value=(1 + sum(x >= n_obs for x in null)) / (1 + len(null)),
                        passed=n_obs > null[989])

    # T2 cross-pair false positives: epic person vs every Vedic person with a different name
    fp = tot = 0
    for e in EPIC:
        own = {v["name"] for v in CANDS[e["name"]]}
        rels, pars = relatives(e), parents(e)
        for v in VED:
            if v["name"] in own: continue
            b, dq, _ = score(e, v, BASE, rels, pars)
            tot += 1; fp += ok(verdict(b, dq)[1])
    report["T2"] = dict(pairs=tot, false_grade2plus=fp, rate=fp / tot, passed=fp / tot < 0.01)

    # T3 known-identity recall
    hits = {c: main[c]["grade"] for c in CONTROLS}
    report["T3"] = dict(results=hits, found=sum(ok(g) for g in hits.values()), needed=6,
                        passed=sum(ok(g) for g in hits.values()) >= 6)

    # T4 sensitivity: priors and every m,u moved +-25%
    variants = {"prior 1:3": (BASE, 1/3), "prior 1:30": (BASE, 1/30)}
    for f in BASE:
        for k, mult in (("m", 0.75), ("m", 1.25), ("u", 0.75), ("u", 1.25)):
            P = dict(BASE); m, u = P[f]
            P[f] = (min(m * mult, 0.99), u) if k == "m" else (m, min(u * mult, 0.9))
            variants[f"{f}.{k} x{mult}"] = (P, PRIOR)
    alt = {k: run(P, pr) for k, (P, pr) in variants.items()}
    for name, r in main.items():
        gs = {main[name]["grade"]} | {alt[k][name]["grade"] for k in alt}
        r["robust"] = "yes" if len(gs) == 1 else "no (" + " / ".join(sorted(gs)) + ")"
    report["T4"] = dict(variants=list(variants), changed=[n for n, r in main.items() if r["robust"] != "yes"])

    rows = sorted(main.values(), key=lambda r: (-r["p"], r["grade"] == "Disqualified", r["person"]))
    import csv
    with open(f"{D}/results/linkage_results.csv", "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); wr.writeheader(); wr.writerows(rows)
    json.dump(report, open(f"{D}/results/battle_tests.json", "w"), indent=1)
    print(json.dumps(report, indent=1))
    for r in rows:
        if r["grade"] != "No Vedic candidate":
            print(f"{r['person'][:28]:28} {r['vedic'][:28]:28} {r['grade']:15} p={r['p']:<6} robust={r['robust'][:40]} | {r['why'][:110]}")
    print("No Vedic candidate:", ", ".join(r["person"] for r in rows if r["grade"] == "No Vedic candidate"))
