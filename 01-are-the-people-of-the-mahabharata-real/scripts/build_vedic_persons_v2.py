"""Version 2 Vedic side: every person record in the Cologne digital Vedic Index (csl-orig v02/vei/vei.txt).
Main text only (footnotes removed); sentences about the Epic/Puranas deleted. Fully automatic."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import norm, key
src = sys.argv[1]
raw = open(src, encoding="utf8").read()
recs = re.findall(r"<L>(\d+)<pc>([^<]+)<k1>([^<]+)<k2>[^\n]*\n(.*?)<LEND>", raw, flags=re.S)
EPIC_WORDS = re.compile(r"\b(Epic|epic|Mahābhārata|Mahabharata|Purāṇa|Purāṇas|Purāṇic|Purana|Puranas|Rāmāyaṇa|Ramayana|Harivaṃśa|Pargiter)\b")
ROLE = [("royal", r"king|prince|chief|emperor|monarch|patron|warrior|hero|ruler|Kṣatriya"),
        ("woman", r"woman|queen|princess|wife|daughter"),
        ("sage", r"priest|teacher|sage|seer|Ṛṣi|poet|singer|pupil|Brahmin|Purohita|authority|ascetic"),
        ("divine", r"god|goddess|demon|Apsaras|serpent|snake|deity|Asura|nymph|Gandharva"),
        ("other", r"man|person|individual|descendant|brother|son|father|mother|husband|grandson|sister")]
NONPERSON = r"\b(people|tribe|river|country|town|city|mountain|plant|tree|animal|bird|disease|constellation|month|metre|measure|school|family)\b"
def clean(t):
    t = re.sub(r"<F>.*?</F>", " ", t, flags=re.S)
    t = re.sub(r"<sup>.*?</sup>|<[^>]+>|\{[@%]|[@%]\}|¦|\[Page[^\]]*\]", " ", t)
    return re.sub(r"\s+", " ", t).strip()
persons = []
for L, pc, k1, body in recs:
    m = re.search(r"\{@(.+?)@\}", body)
    if not m: continue
    head = re.sub(r"^\d+\.\s*", "", m.group(1)).strip(" .,—-")
    text = clean(body)
    first = text[:300]
    gloss = re.search(r"name of (?:an? )?(?:[\w\-ṛṣṇāīūśṭḍñṅ]+ )?(\w+)|is (?:an? )(?:[\w\-ṛṣṇāīūśṭḍñṅ]+ )?(\w+)|patronymic|descendant of", first)
    role = None
    for r, pat in ROLE:
        if re.search(r"\b(" + pat + r")s?\b", first[:220]):
            role = r; break
    toks = [t for t in re.split(r"[\s,]+", head) if t]
    has_patr = len(toks) >= 2 and toks[1][:1].isupper()
    if re.search(NONPERSON, first[:160]) and not has_patr and role in (None, "other"):
        continue
    if re.search(r"\b(people|tribe)\b", first[:100]) and not re.search(r"\bking\b", first[:100]) and not has_patr:
        continue
    if role is None and not has_patr and not gloss:
        continue
    if role is None: role = "unknown"
    sentences = re.split(r"(?<=[.;])\s", text)
    entry = " ".join(s for s in sentences if not EPIC_WORDS.search(s))
    headname = toks[0].replace("-", "")
    persons.append(dict(L=int(L), page=pc, name=" ".join(toks).replace("-", ""), head=headname,
                        second=" ".join(toks[1:]).replace("-", ""), role=role, role_word="", key=key(headname),
                        entry=entry[:8000], n_entry_chars=len(entry), text=""))
# "X is the patronymic of Y": also file the record under Y (Dauḥṣanti -> Bharata Dauḥṣanti)
extra = []
for p in persons:
    for y in re.findall(r"is the patronymic of ([A-ZĀĪŪṚŚṢ][\wāīūṛṣṇśṭḍñṅṃḥ\-]+)", p["entry"][:300]):
        y = y.replace("-", "")
        extra.append(dict(p, name=f"{y} {p['head']}", head=y, second=p["head"], key=key(y), alias_of=p["name"]))
persons += extra
json.dump(persons, open(os.path.join(os.path.dirname(__file__), "..", "data", "vedic_persons_v2.json"), "w"), indent=0, ensure_ascii=False)
import collections
print(len(recs), "records;", len(persons), "persons;", collections.Counter(p["role"] for p in persons))
