"""Vedic side: parse every person from the Vedic Index (Macdonell & Keith 1912) name index, with the
text of every passage in the Index where the name occurs. Fully automatic: no hand-coding.
Input: Vedic Index full text (archive.org vedicindexofname01macduoft + 02macduoft, djvu.txt), concatenated."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import norm, key, ocr_variants
src = sys.argv[1]
lines = open(src, encoding="utf8", errors="ignore").read().splitlines()
IDX = 81600                                   # start of the name index in the concatenated text
body = re.sub(r"\s+", " ", " ".join(lines[:IDX]))
index = re.sub(r"\s+", " ", " ".join(lines[IDX:]))
ROLES = {"king": "royal", "prince": "royal", "emperor": "royal", "chief": "royal", "patron": "royal", "hero": "royal",
         "warrior": "royal", "queen": "woman", "woman": "woman", "princess": "woman", "teacher": "sage", "priest": "sage",
         "seer": "sage", "sage": "sage", "Rsi": "sage", "poet": "sage", "singer": "sage", "Brahmin": "sage", "man": "other",
         "god": "divine", "demon": "divine", "deity": "divine", "goddess": "divine", "Apsaras": "divine", "serpent": "divine"}
NONPERSON = ("river", "people", "tribe", "country", "constellation", "plant", "tree", "town", "mountain", "animal",
             "bird", "disease", "lake", "place", "region", "metal", "weapon", "measure", "family", "school", "clan")
entries = []
for raw in lines[IDX:]:
    t = re.sub(r"\s+", " ", raw).strip()
    m = re.match(r"^(?:\d\.\s)?([A-Z\^\$][A-Za-z\^\$&\-]+(?:\s[A-Z\^\$][A-Za-z\^\$&\-\(\)']+){0,3})(?:\s(?:or|and)\s[^,]+)?,\s(.*)$", t)
    if not m: continue
    name, rest = m.group(1), m.group(2)
    if rest.startswith(("'", "\u2018", "\u2019", "(", "*")): continue          # a word gloss, not a person
    d = re.match(r"^an?\s([A-Za-z]+(?:\sof\sSamans|\sking)?)", rest)
    if d:
        w = d.group(1).split()[0]
        if w.lower().startswith(NONPERSON): continue
        role = ROLES.get(w, ROLES.get(d.group(1), "other"))
        role_word = d.group(1)
    elif re.match(r"^(i|ii)\.", rest):
        role, role_word = "unknown", ""
    else:
        continue
    entries.append((name.replace("&", "a"), role, role_word))
def within_one(a, b):
    """True if a and b differ by at most one substitution, insertion or deletion."""
    if abs(len(a) - len(b)) > 1: return False
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]: i += 1
    return a[i+1:] == b[i+1:] or a[i:] == b[i+1:] or a[i+1:] == b[i:]
EPIC_WORDS = re.compile(r"\b(Epic|epic|Mahabharata|Mahdbhdrata|Purana|Puranas|Puranic|Ramayana|Harivamsa|Pargiter)\b")
HEAD_LINE = re.compile(r"^\s*(?:\d\.\s+|[ivx]+\.\s+)?([A-Z\^\$l][A-Za-z\^\$!\-]+)")
def entry_text(head):
    """Amendment 1: the Index's own entry for this name only (headword at line start, ~30 lines),
    with every sentence that mentions the Epic, the Puranas or the Ramayana removed."""
    targets = {norm(v) for v in ocr_variants(head)}
    out = []
    for i in range(IDX):
        m = HEAD_LINE.match(lines[i])
        if not m: continue
        h = norm(m.group(1))
        if h not in targets and not (len(h) >= 7 and any(within_one(h, t) for t in targets)): continue
        prev = lines[i - 1].strip() if i else ""
        if prev and not (prev.endswith((".", ")", ":")) or len(prev) < 45 or re.match(r"^\d", prev)):
            continue                                   # a wrapped line inside a paragraph, not an entry start
        nxt = " ".join(lines[i + 1:i + 3])
        if not re.search(r"\b(is|are|appears|was|occurs|seems|denotes|mentioned)\b", lines[i] + " " + nxt): continue
        chunk = [lines[i]]
        for j in range(i + 1, min(i + 30, IDX)):
            mj = HEAD_LINE.match(lines[j])
            if mj and re.search(r"\b(is|appears|denotes)\b", lines[j]) and norm(mj.group(1)) not in targets and len(lines[j].split()) > 4 and lines[j][:1].isupper() and re.match(r"^\s*[A-Z\^\$][a-z\^\$\-]+(\s[A-Z\^\$][a-z\^\$\-]+)?\s+(\(|is |appears)", lines[j]):
                break
            chunk.append(lines[j])
        txt = re.sub(r"\s+", " ", " ".join(chunk))
        sentences = re.split(r"(?<=[.;])\s", txt)
        out.append(" ".join(x for x in sentences if not EPIC_WORDS.search(x)))
    return " ".join(out)[:8000]
TOK, TOK_BY_LEN = {}, {}
for mm in re.finditer(r"[A-Za-z\^\$!][A-Za-z\^\$!\-]*", body):
    for v in ocr_variants(mm.group()):
        n = norm(v)
        if len(n) >= 3:
            TOK.setdefault(n, []).append((mm.start(), mm.end()))
for n, locs in TOK.items():
    TOK_BY_LEN.setdefault(len(n), {})[n] = locs
persons, seen = [], set()
for full, role, role_word in entries:
    if full in seen: continue
    seen.add(full)
    toks = full.split()
    head = toks[0]
    # every passage in the Index body mentioning the head name (any OCR reading), 700 characters each
    windows = []
    targets = {norm(v) for v in ocr_variants(head)}
    for t in targets:
        for (st, en) in TOK.get(t, []):
            windows.append(body[max(0, st - 200): en + 500])
            pass
    for t in list(targets):
      if len(t) >= 7:                       # tolerate one OCR error in long names
        for L in (len(t) - 1, len(t), len(t) + 1):
            for k2, locs in TOK_BY_LEN.get(L, {}).items():
                if k2 != t and k2[:2] == t[:2] and within_one(k2, t):
                    windows.extend(body[max(0, st - 200): en + 500] for st, en in locs)
    entry = entry_text(head)
    persons.append(dict(name=full, head=head, second=" ".join(toks[1:]), role=role, role_word=role_word, entry=entry,
                        n_entry_chars=len(entry),
                        key=key(head), text=" ".join(windows)[:20000], n_passages=len(windows)))
json.dump(persons, open(os.path.join(os.path.dirname(__file__), "..", "data", "vedic_persons.json"), "w"), indent=0)
print(len(persons), "Vedic persons;", sum(1 for p in persons if p["n_passages"] == 0), "with no passage found")
