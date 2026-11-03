# Are the people of the Mahabharata real? Results

Protocol: `PROTOCOL.md` (with Amendments 1–3). Data: `data/`. Code: `scripts/`. Outputs: `results/`.
To reproduce: `python3 scripts/build_epic_people.py`, `python3 scripts/build_vedic_persons.py data/vedic_index_1912_ocr.txt`,
`python3 scripts/link.py`.

## 1. What was tested

- **107 people of the Mahabharata** (main lineages plus the people of its embedded stories), coded from the epic only.
- **1,943 Vedic Index entries** (Macdonell & Keith 1912), parsed automatically.
- Every epic person was compared with every Vedic person of the same name, scoring father, relatives,
  associates, role and people (Fellegi–Sunter weights on Mykytiuk's identifying marks), then every match
  and disqualification was checked by hand against the Vedic Index text.

## 2. Battle tests (final frozen method)

| Test | Result | Pass? |
|---|---|---|
| T1 Chance matches: relatives shuffled 1,000 times | Real data: **24** grade 2+ matches. Shuffled: mean 9.4, 99th percentile 13, max 16. p = 0.001 | **Passed** |
| T2 False positives: 207,801 wrong-name pairs | **1.3%** reach grade 2+ (limit 1%). Mostly entries of a person's own relatives, which name the family | **Failed** |
| T3 Known identities (9 controls) | 6 of 9 found (Bharata, Purūravas, Māndhātṛ, Uddālaka, Śvetaketu, Janaka). Missed: Yayāti and Nala (not parsed from the scanned Index), Yājñavalkya (weak) | **Passed** (6 needed) |
| T4 Sensitivity: 2 priors and 16 parameter shifts | Only **8** automatic verdicts are unchanged across all 18 variants | Most verdicts fragile |
| T5 Hand review of every grade 2+ and disqualification | Of 24 automatic grade 2+ matches, **15 confirmed, 9 wrong**. Review also found 3 matches the automatic run missed (Śrutasena, Yājñavalkya, Somaka) | See below |

**What the tests mean.**
- The method finds far more matches than chance (T1), so the signal is real.
- But on its own it is **not reliable enough** (T2 failed; about 60% precision in T5). About 9 of 24 automatic
  matches are wrong, which agrees with T1's chance level of about 9.
- So **every verdict below is the hand-reviewed one**, and the automatic score is reported beside it.
  The method's job is to find and rank candidates; the evidence has to be read.

Three amendments were made during testing (circular use of the Index's own retelling of the epic; loose
patronymic rule; self-mention). They are documented in `PROTOCOL.md`; the failed runs are in the commit history.

## 3. Results: the people of the Mahabharata

### Confirmed (grade 3: virtually certain to reliable)

| Person | Vedic person | Evidence |
|---|---|---|
| **Janamejaya** | Janamejaya Pārikṣita (Śatapatha 13.5.4; Aitareya 8.21) | Father Parikṣit; three brothers; priest Indrota; same episode (horse sacrifice to cleanse the killing of a Brahmin) |
| **Ugrasena, Bhīmasena, Śrutasena** (Janamejaya's brothers) | The Pārikṣitīyas (Śatapatha 13.5.4.3) | Named together as brothers of Janamejaya |
| **Indrota Śaunaka** | Indrota Daivāpa Śaunaka (Śatapatha 13.5.4.1) | Janamejaya's priest in the same episode |
| **Bālhika** | Bālhika Prātipīya (Śatapatha 12.9.3.3) | Name; son of Pratīpa; Kuru king |
| **Somaka** | Somaka Sāhadevya (Rigveda 4.15) | Name; son of Sahadeva; king. *New: missed by the automatic run (OCR)* |
| **Bharata** | Bharata Dauḥṣanti (Śatapatha 13.5.4.11–14) | Son of Duṣyanta; mother Śakuntalā in the same passage |
| **Māndhātṛ** | Māndhātṛ Yauvanāśva | Name; son of Yuvanāśva; king |
| **Uddālaka Āruṇi**, **Śvetaketu** | Uddālaka Āruṇi; Śvetaketu Āruṇeya | Father and son; Pañcāla setting |
| **Janaka**, **Yājñavalkya** | Janaka of Videha; Yājñavalkya Vājasaneya | King and his court teacher in both |

### Probable (grade 2: reasonable but uncertain)

| Person | Why not grade 3 |
|---|---|
| **Parikṣit** | Some scholars read the Atharvaveda hymn as about the god Agni |
| **Dhṛtarāṣṭra** | Name, father Vicitravīrya and the Vaka Dālbhya quarrel match, but the Vedic king may not be a Kuru |
| **Śaṃtanu** | The Rigveda names him with Devāpi but gives "no hint of relationship"; the brother story is later (Nirukta) |
| **Vyāsa** | Only in late teacher lists; the Vedic Index calls him mythical |
| **Kṛṣṇa** | Name and mother Devakī match, but the Vedic Kṛṣṇa is a pupil with no royal context |
| **Kalmāṣapāda Saudāsa** | Same story (killing of Śakti), but the Vedic texts speak of a family |

### Same figure, but mythical in the Vedic texts
**Purūravas** (with the nymph Urvaśī) and **Śakuntalā** (an Apsaras). The epic took over Vedic legends.

### Disqualified: real Vedic people, but the epic's family tree is wrong
| Person | Conflict |
|---|---|
| **Devāpi** | Vedic father Ṛṣṭiṣeṇa, epic father Pratīpa. The Vedic Index: two Devāpi stories "confused" |
| **Śatānīka** | Vedic father Satrājit, epic father Janamejaya |
| **Pratīpa** | Different patronymic; may not be a name at all |

### Tribes turned into people
**Yadu** and **Puru** are Rigvedic **tribes** (named with Turvaśa and Druhyu). The epic makes them brothers,
sons of Yayāti.

### No independent trace (absence is not disproof)
**Bhīṣma, Pāṇḍu, Kuntī, Mādrī, Gāndhārī, Draupadī, Drupada, Dhṛṣṭadyumna, the five Pāṇḍavas, Duryodhana,
Duḥśāsana, Karṇa, Śakuni, Droṇa, Aśvatthāman, Kṛpa, Abhimanyu, Vidura, Satyavatī, Jarāsandha, Śiśupāla,
Virāṭa, Śalya, Ghaṭotkaca**, and others. Weak, name-only or wrong-namesake candidates for some of them
(Arjuna, Bhīma, Sahadeva, Yudhiṣṭhira, Karṇa, Śikhaṇḍin, Śakuni) did not survive review.

## 4. Findings

1. **The war generation has no independent trace.** None of the central heroes of the war, on either side,
   appears in the Vedic texts as the same person. Kṛṣṇa and Dhṛtarāṣṭra are the only partial exceptions.
2. **The generation after the war is real.** Janamejaya, his three brothers and his priest are securely attested,
   with the same episode in both sources. Parikṣit is probable.
3. **Earlier Kuru names are real people placed in a new family tree.** Bālhika, Śaṃtanu and Devāpi existed,
   but the epic's relationships between them conflict with the Vedic record. Tribes became brothers.
   This is the pattern Henige (1974) describes for oral genealogies: real names, merged and re-ordered.
4. **The epic's side stories rest on real Vedic figures.** Bharata, Somaka, Māndhātṛ, Uddālaka, Śvetaketu,
   Janaka and Yājñavalkya all match, several with father and associates.

**In one line:** the Mahabharata is built around a real late-Vedic Kuru court and real Vedic figures,
but its central war heroes cannot be found outside the epic.

## 5. Version 2: strengthened method (clean data, typed relationships)

Changes, fixed in the protocol before running: the clean Cologne digital Vedic Index replaced the 1912 scan
(Amendment 4), and a relative now counts only when the Vedic entry states **the same relationship** as the epic
(Amendment 5, Mykytiuk's rule). One parsing fix followed (Amendment 6: entries describing a person only by
kinship, such as "a brother of Janamejaya", were being dropped).

| Test | Version 1 | **Version 2** |
|---|---|---|
| T1 Better than chance | Passed (24 vs ≤16 in shuffles) | **Passed** (26 vs ≤14 in shuffles; p = 0.001) |
| T2 False positives < 1% | **Failed** (1.3%) | **Passed (0.60%)** |
| T3 Known identities (6 of 9 needed) | 6 | **7** (Bharata, Yayāti, Purūravas, Māndhātṛ, Uddālaka, Śvetaketu, Janaka); Nala still missing |
| T4 Verdicts unchanged across 18 variants | 8 | 17 robust automatic grades |
| T5 Agreement with hand review | precision 0.62 | **precision 0.71, recall 0.83** |

**What still goes wrong automatically:** category errors, not wrong identities. Tribes or peoples taken for persons
(Yadu, Pūru, Gāndhāra, Kuru), legendary figures counted like historical ones (Purūravas), and role conflicts the
scoring under-weights (Śikhaṇḍin the priest, Saubala the pupil). A version 3 should add a rule that an entry naming
"a tribe" or "a people" is not a person, and treat a role conflict as disqualifying.

**Conclusion on the method:** version 2 passes every pre-set battle test, so it is **trustworthy as a screening
method**. It is still not a substitute for reading the evidence: final verdicts remain hand-reviewed.

### Version 2 additions after hand review
| Person | Verdict | Note |
|---|---|---|
| **Śakti** (son of Vasiṣṭha) | **Grade 3** | Killed by fire at the instigation of the Viśvāmitras: same story as the epic |
| **Yayāti** | Same figure, legendary | Son of Nahuṣa; "an ancient sacrificer" in the Rigveda |
| **Viśvāmitra** | Same figure, legendary | Rigvedic seer, Kuśika line, rival of Vasiṣṭha in both |
| **Vasiṣṭha** | Same figure, a priestly family name | The Vedic Index doubts one individual is meant |
| Kuru | Not identified | Matched the wrong entry (Kuruśravaṇa) |

The main findings (section 4) are unchanged by version 2: the post-war court of Janamejaya is confirmed with typed
relationships (three brothers as siblings, Indrota as priest); the war generation still has no independent trace.

### Version 3: tribe rule (R6) and role-conflict rule (R7)

| Test | Version 2 | **Version 3** |
|---|---|---|
| T1 Better than chance | Passed | **Passed** (21 matches vs ≤11 in 1,000 shuffles; chance mean 5.8; p = 0.001) |
| T2 False positives < 1% | 0.60% | **0.48%** |
| T3 Known identities | 7 of 9 | **7 of 9** |
| T5 Precision / recall vs hand review | 0.71 / 0.83 | **0.76 / 0.84** |

- R6 removed Yadu, Pūru and Gāndhāra (tribes and peoples). R7 removed Śikhaṇḍin (a priest) and Saubala (a pupil).
- **Of the 5 remaining disagreements, 4 are not wrong identities**: Purūravas, Yayāti, Viśvāmitra and Vasiṣṭha are the
  right Vedic figures, but legendary (or a family name) there. Counting the identity alone, **precision is 0.95 (20 of 21)**.
  The one true error is Kuru, a parsing slip (the entry Kuruśravaṇa was read as "Kuru").
- **Misses (3):** Parikṣit, Yājñavalkya and Kalmāṣapāda Saudāsa. Their Vedic entries describe the link without the
  relation words the typed rule needs (Parikṣit's son is named in a different sentence; Yājñavalkya's link to Janaka is
  in Janaka's entry). The hand review keeps them.

**Status of the method:** passes every pre-set battle test with margin, and its matches are right about the identity
19 times out of 20. Remaining hand-review work is to label legendary figures and recover a few missed links.

## 6. Limitations

- **Hand review decides the final verdicts.** The automatic method alone is about 60% precise, so the final
  grades depend on the reviewer's reading. A second, independent reviewer should repeat T5.
- **Data:** version 1 used OCR of a 1912 scan; version 2 uses the clean Cologne transcription. Nala is still not found.
- **Epic side coded by one person** from the epic's genealogies; to be checked against the Critical Edition.
- **Identity, not existence.** A match shows the epic's person is the Vedic person; existence then rests on the
  Vedic text, which for Brāhmaṇa-period kings is close to contemporary but for Rigvedic figures may be legendary.
- **The Vedic texts are ritual texts.** Absence of a person is weak evidence.

## 7. Critical Edition check, second review, final verdicts

- **Critical Edition check** (BORI electronic text, GRETIL; books 1, 3, 9, 12): every relationship on which a verdict
  depends was confirmed, except Somaka "son of Sahadeva" (not in the CE; Purāṇic) and Arjuna's son by Draupadī
  (Śrutakīrti). Both corrected (Amendment 7). Somaka moves to grade 2. The CE also names Dhṛtarāṣṭra *vaicitravīryin*
  in the Baka Dālbhya episode (9.40.1), the same patronymic as the Vedic record.
- **Blind second review** (`review2/`): 61 people judged without scores or first-review verdicts. On the 37 shared
  people: identity accept/reject **κ = 1.00**; identified/legendary/not **κ = 0.77**; exact grade **κ = 0.52**.
  The second reviewer is an AI model; a human expert review is still recommended.
- **Final adjudicated verdicts** (`results/adjudicated_verdicts.csv`, conservative rule):
  - **Grade 3:** Janamejaya, Ugrasena, Indrota, Uddālaka, Śvetaketu, Janaka, Śakti.
  - **Grade 2:** Śrutasena (and Bhīmasena), Bālhika, Bharata, Māndhātṛ, Yājñavalkya, Somaka, Parikṣit, Dhṛtarāṣṭra,
    Śaṃtanu, Kṛṣṇa (and Parāśara, second reviewer only).
  - **Same figure, historicity disputed:** Vyāsa, Yayāti, Viśvāmitra, Vasiṣṭha, Kalmāṣapāda.
  - **Same figure, legendary:** Purūravas, Śakuntalā (and Agastya, Bharadvāja, Jamadagni, Nārada, second reviewer only).
