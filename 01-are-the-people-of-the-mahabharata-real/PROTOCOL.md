# Are the people of the Mahabharata real? Test protocol (fixed before the full run)

Scope: **names and identities only.** Dating is a later question.

## 1. Question

For each person in the Mahabharata, is there a person in the older Vedic texts who is, with stated
confidence, the same individual? A Vedic match is the only independent check available: the Vedic texts
are older than the epic, were memorised with cross-checks, and mention kings and priests incidentally
(they were not written to support the epic).

## 2. Assumptions (stated so they can be challenged)

| # | Assumption | Why | What breaks if wrong |
|---|---|---|---|
| A1 | The Vedic texts as edited today are faithful to their early form | Oral transmission with cross-check recitations; regional lineages agree | Matches could reflect later edits |
| A2 | The Vedic texts are older than the epic text | Scholarly consensus on relative order | Vedic mentions could copy the epic |
| A3 | A Vedic king or priest named incidentally in a ritual text was a real person of that period | Ritual texts cite patrons and teachers as authorities | A match would show identity, not existence |
| A4 | A shared name alone is not evidence | The epic's poets knew the Vedas and could borrow names | (Builds in caution; nothing breaks) |
| A5 | Indian naming practice: the patronymic names the **legal** father (e.g. Vaicitravīrya for Dhṛtarāṣṭra) | Standard Sanskrit usage | Wrong disqualifications |
| A6 | The Vedic Index (Macdonell & Keith, 1912) lists the persons of the Vedic texts with their key passages | Standard reference, still used | Missed candidates (false negatives only) |
| A7 | **Absence is not disproof.** A person not in the Vedic texts may still be real | The Vedic texts are ritual, not history | (Builds in caution) |

## 3. Data

- **Epic side** (`data/epic_people.json`): people of the Mahabharata, including the persons of its embedded
  stories, with father, mother, siblings, spouses, children, teachers or priests, people (Kuru, Pañcāla…) and role.
  Coded **from the epic's own genealogies and episodes, without looking at Vedic matches.**
  To be checked against the Critical Edition before publication.
- **Vedic side** (`data/vedic_persons.json`): every person entry parsed automatically from the Vedic Index's
  index of names, with the text of every passage where the Index discusses that name.
  **No hand-coding on this side.**

## 4. Method (published methods combined)

| Step | Method | Source |
|---|---|---|
| Source reliability | Oral-tradition criticism | Vansina 1985; Henige 1974 |
| Candidate pairs | Blocking on normalised name (transliteration-insensitive) | Standard record-linkage practice |
| Scoring | Fellegi–Sunter log-likelihood weights over identifying marks | Fellegi & Sunter 1969; marks from Mykytiuk 2004 |
| Verdict | Bayesian posterior mapped to Mykytiuk-style grades | Mykytiuk 2004 grade definitions |

**Identifying marks (fields), all scored automatically:**

| Field | Agrees if | m | u | Bits if agrees / conflicts |
|---|---|---|---|---|
| Patronymic | The Vedic name's second element contains the consonant skeleton of the epic father's (or mother's) name | 0.85 | 0.01 | +6.4 / **disqualifies** |
| Each relative or associate | An epic relative's or teacher's name appears in the Vedic Index text for that person | 0.80 | 0.01 | +6.3 each |
| Role | Vedic Index role (king/prince vs priest/teacher/sage) matches the epic role class | 0.90 | 0.30 | +1.6 / −2.8 |
| People | The epic person's people (Kuru, Pañcāla, Yadu…) is named in the Vedic Index text | 0.90 | 0.20 | +2.2 / 0 |

**Rules:**
- R1. Name match only creates a candidate (0 bits).
- R2. A Vedic patronymic that matches no epic parent **disqualifies** (Mykytiuk: conflicting marks).
- R3. A Vedic person who is a god, river or mythic being, where the epic has a human, is disqualified.
- R4. Prior odds that a same-named candidate is the same person: **1:10** (sensitivity 1:3, 1:30).
- R5. Grades: posterior ≥ 0.95 **grade 3** (virtually certain to reliable); ≥ 0.50 **grade 2** (reasonable but uncertain);
  ≥ 0.05 **weak**; below, **not identified**. A person with several candidates takes the best one.

## 5. Battle tests (run before reading the Mahabharata results)

| Test | What it checks | Pass criterion (fixed now) |
|---|---|---|
| T1 Permutation null | Shuffle the epic relatives between people 1,000 times and rerun. How many grade 2+ matches arise by chance? | Observed grade 2+ count above the 99th percentile of the null |
| T2 Cross-pair false positives | Score every epic person against every Vedic person **with a different name** (ignoring R1). How often does a wrong pair reach grade 2+? | False-positive rate below 1% |
| T3 Known-identity recall | Epic figures that standard scholarship identifies with Vedic figures (Bharata Dauḥṣanti, Yayāti Nāhuṣa, Purūravas Aila, Māndhātṛ Yauvanāśva, Nala Naiṣadha, Uddālaka Āruṇi, Śvetaketu Āruṇeya, Yājñavalkya, Janaka Vaideha). Does the method find them? | At least 6 of 9 reach grade 2+ |
| T4 Sensitivity | Rerun with the prior at 1:3 and 1:30, and with every m and u moved ±25% | Report which verdicts change; a verdict is **robust** only if unchanged across all |
| T5 Clerical review | Read the Vedic Index text for every grade 2+ match and every disqualification by hand | Report every case where the automatic verdict is wrong |

If T1, T2 or T3 fails, the method is not trusted and the Mahabharata results are reported as exploratory only.

## 6. Honesty note

The author of this protocol had already seen a hand-made register of about 13 Kuru kings (v2). The parameters
above are the ones used there, unchanged. Everything else (the full epic list, the automatic Vedic coding,
the controls) is new to this run.

## Amendment 1 (made after the first run, before final results)

The first run showed three faults. They were fixed before any result was reported, and the first-run output is
kept in the commit history for transparency.

1. **Circularity.** The Vedic Index (1912) often describes what "the Epic" says about a name. Passages around
   a name therefore contained the epic's own genealogy. Fix: the Vedic text for a person is now **only the
   Index's own entry for that name**, and **every sentence mentioning the Epic, the Purāṇas, the Rāmāyaṇa,
   the Harivaṃśa or Pargiter is deleted** before scoring.
2. **Co-mention.** Names listed together anywhere in the Index (for example the Rigvedic tribes Yadu, Turvaśa,
   Druhyu, Puru) counted as relatives. Restricting to the person's own entry removes most of this.
   Remaining cases are checked by hand in T5.
3. **Loose blocking and OCR.** Very short names (Ayu, Rama) matched unrelated entries, and one-letter tolerance
   joined different names (Durvāsā / Turvaśa). Fix: names under 4 letters must match exactly; one-letter
   tolerance only for names of 8+ letters. Patronymic comparison now tolerates one OCR error
   (it had falsely disqualified Somaka Sāhadevya, read as "Sahadcvya").

## Amendment 2 (after battle test T2 failed)

With Amendment 1, **T2 failed**: 1.6% of deliberately wrong pairs reached grade 2+ (limit 1%). Cause: a fixed
chance-agreement value u = 0.01 for every relative's name, although common names (Bharata, Arjuna, Gaṅgā) appear in
many entries. Fix, standard in Fellegi & Sunter (1969): **value-specific u** = the share of Vedic Index entries that
contain that name (+1 smoothing, minimum 0.001). People names use the same frequency with a 5× multiplier
(peoples are mentioned far more often than persons). Also, anusvāra spellings are normalised (Śaṃtanu = Śantanu),
which had hidden Śaṃtanu. All battle tests were rerun after this amendment.

## Amendment 3 (after diagnosing the remaining T2 failures)

Diagnosis of the T2 false positives found two coding errors, fixed here:
1. **Patronymic test too loose.** It accepted any patronymic *containing* the parent's skeleton (Pratīpa matched
   "Supratīta"). A Sanskrit patronymic is formed on the parent's name and begins with it (Pārikṣita, Vaicitravīrya,
   Prātipīya), so it must now **start with** the parent's consonant skeleton (exactly, for 2–3 consonants; one OCR error allowed at 4+). A first version required 3+ consonants, which wrongly disqualified Śvetaketu Āruṇeya (son of Āruṇi); that was corrected, and the method was then frozen.
2. **Self-mention.** An entry's own headword was counted as naming a relative of the same name
   (the entry for Bhīmasena "named" Bhīmasena). An entry can no longer name itself.
Remaining T2 false positives are mostly entries of a person's own **relatives**, which naturally name the family.
That is reported as a limit of co-mention evidence, not hidden.

## Version 2 (written before running; pass criteria unchanged)

Version 1 failed T2 (1.3% false positives) and was only ~60% precise in hand review. Version 2 makes two changes,
fixed here before any version 2 result is seen.

**Amendment 4: clean data.** The Vedic side is rebuilt from the Cologne Digital Sanskrit Lexicon transcription of the
Vedic Index (`sanskrit-lexicon/csl-orig`, `v02/vei/vei.txt`), which has one record per entry, the headword marked,
diacritics, and footnotes separated. This replaces the OCR of the 1912 scan. Only the entry's main text is used
(footnotes removed), and sentences mentioning the Epic, Purāṇas, Rāmāyaṇa, Harivaṃśa or Pargiter are still deleted.
A record is a person if its first sentence calls it a name of a person (king, prince, priest, teacher, sage, seer, man,
woman, patron…) or the headword carries a patronymic; peoples, rivers, places and words are excluded.

**Amendment 5: typed relationships (Mykytiuk's rule).** A relative or associate now counts only if the Vedic entry states
**the same kind of relationship** as the epic, within 80 characters of the relative's name:

| Epic relation | Vedic wording that counts |
|---|---|
| father or mother | son of, daughter of, descendant of, father, mother, bore, patronymic |
| child | son, daughter, father of, mother of, whose son, his son |
| sibling | brother, brothers, sister |
| spouse | wife, husband, queen, married, consort |
| teacher, priest or associate | priest, Purohita, pupil, teacher, taught, patron, officiated, sacrifice, court |

A bare co-mention scores nothing. Everything else (weights, frequency-based u, prior, grades, disqualification rules,
battle tests T1–T5 and their pass criteria) is unchanged. The version 1 hand review (`results/clerical_review.csv`) is used
as the reference to measure version 2's precision and recall.

## Amendment 6 (parsing fix after the first version 2 run)

The first version 2 run passed T1, T2 and T3 (T2: 0.60%), but the person filter dropped entries that describe a person
only through kinship (e.g. "Ugrasena … a Pārikṣitīya and a brother of Janamejaya"), because the Cologne text capitalises
every headword and the filter looked only for role words. Fix: kinship words (brother, son, father, mother, husband,
grandson, sister) in the opening of an entry also mark it as a person. Nothing else changed. Both runs are reported.

## Version 3 (written before running; pass criteria unchanged)

Version 2 passed T1–T3, but hand review showed its remaining errors were category errors. Two rules are added;
everything else is version 2 unchanged.

- **R6 (tribe or people):** a Vedic entry whose opening (first 150 characters) describes a tribe or a people
  ("name of a tribe", "a people", "the people called…") is not a person. Such a candidate is excluded, labelled
  "tribe or people, not a person".
- **R7 (role conflict):** when both sides have a known role class (royal, sage/priest, woman) and they differ,
  the candidate is **disqualified** (Mykytiuk: a conflicting identifying mark disqualifies). Before, a conflict only
  subtracted 2.8 bits.

Measured against the hand review as in version 2. Battle tests T1–T5 and pass criteria unchanged.

## Amendment 7 (data correction from the Critical Edition check)

The epic dataset was checked against the BORI Critical Edition electronic text (GRETIL; books 1, 3, 9, 12) for every
relationship on which a verdict depends. Two coding errors were corrected: (1) the Critical Edition does not make Somaka the
son of Sahadeva (they are only listed together at 3.125.23; the father comes from Purāṇic genealogies), so Sahadeva is
recoded as an associate and Somaka has no epic father; (2) Arjuna's son by Draupadī is Śrutakīrti (1.90.82), and
Sahadeva's is Śrutasena (1.57.103) or Śrutakarman (1.90.82). No method change. Version 3 was rerun.
