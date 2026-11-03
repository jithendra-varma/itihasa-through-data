# Series question 1: Are the people of the Mahabharata real?

Working draft. Data, code and results are in this folder:
`data/vedic_index_name_counts.json`, `scripts/score_identities.py`, `results.csv`,
and the reference-checked register `mykytiuk_register_v2.md`.

## 1. The question

The Mahabharata names hundreds of kings, sages and warriors. Were any of them real people?
This paper asks a narrower, testable version: **which people in the epic can be matched, with
stated confidence, to people named in older, independent Vedic texts?** It does not ask whether
the war happened or whether the story is true.

## 2. Combined method

No single published method fits. This study combines four, each doing one job:

| Step | Job | Method taken from |
|---|---|---|
| 1. Source check | Is the independent source older than the epic and reliably transmitted? | **Vansina** (*Oral Tradition as History*, 1985) and **Henige** (*The Chronology of Oral Tradition*, 1974). Replaces Mykytiuk's "authentic inscription" test, because India has no inscriptions before Ashoka |
| 2. Candidates | Which Vedic people could be the epic's person? | **Blocking on the name**, as in record linkage. A name match only makes someone a candidate; it is never counted as evidence, because the epic's poets could borrow famous Vedic names |
| 3. Scoring | How strongly do the other details agree? | **Fellegi–Sunter record linkage** (1969), using **Mykytiuk's identifying marks** (2004) as the fields: father, role, people or dynasty, named relatives and associates, distinctive events |
| 4. Verdict | How sure are we? | **Bayesian posterior** from a stated prior, mapped onto **Mykytiuk's grades**. Hard rule from Mykytiuk: a conflicting father, or a Vedic god where the epic has a human, **disqualifies** |

### Parameters (fixed in the script before scoring)

| Field | m: chance it agrees if same person | u: chance it agrees by coincidence | Weight if agrees / conflicts (bits) |
|---|---|---|---|
| Father (patronymic) | 0.85 | 0.01 | +6.4 / disqualifies |
| Role (king, priest...) | 0.90 | 0.30 | +1.6 / −2.8 |
| People or dynasty (Kuru, Pancala...) | 0.90 | 0.20 | +2.2 / −3.0 |
| Each named relative or associate | 0.80 | 0.01 | +6.3 each |
| A distinctive shared episode | 0.70 | 0.05 | +3.8 / −1.7 |

- **Source reliability** multiplies the total: 1.0 for a core Saṃhitā or Brāhmaṇa passage; 0.5 for a late
  appendix, a formulaic teacher list, or a passage whose reading scholars dispute.
- **Prior**: odds of 1:10 that a same-named person is the same person (allowing for borrowing).
  Sensitivity checked at 1:3 and 1:30.
- **Grades**: posterior ≥ 0.95 = grade 3 (virtually certain to reliable); ≥ 0.50 = grade 2 (reasonable but uncertain);
  ≥ 0.05 = weak; below that, not identified.

**Honesty note:** these parameters were set after the qualitative register (v2) had been compiled,
so this run is not a blind test. The sensitivity table shows how much the verdicts depend on the prior.
A future replication should fix parameters before compiling a new register (for example, the Puranic dynasties).

## 3. Results

| Person | Vedic source | Evidence (bits) | P (prior 1:3) | **P (prior 1:10)** | P (prior 1:30) | Verdict |
|---|---|---|---|---|---|---|
| **Janamejaya** | Śatapatha Br. 13.5.4; Aitareya Br. 8.21 | 39.3 | 1.00 | **1.00** | 1.00 | **Grade 3**, robust |
| **Bālhika** | Śatapatha Br. 12.9.3.3 | 10.2 | 0.997 | **0.991** | 0.975 | **Grade 3**, robust |
| Śaṃtanu | Ṛgveda 10.98 | 7.9 | 0.988 | **0.960** | 0.889 | Grade 3 at 1:10, grade 2 at 1:30 |
| Kṛṣṇa | Chāndogya Up. 3.17.6 | 6.3 | 0.964 | **0.889** | 0.727 | Grade 2 |
| Śikhaṇḍin | Kauṣītaki Br. 7.4 | 5.8 | 0.948 | **0.845** | 0.646 | Grade 2 (but a priest, not a warrior) |
| Parikṣit | Atharvaveda 20.127 | 5.0 | 0.916 | **0.767** | 0.523 | Grade 2 |
| Dhṛtarāṣṭra | Kāṭhaka Saṃhitā 10.6 | 3.6 | 0.803 | **0.549** | 0.289 | Grade 2, fragile |
| Vyāsa | Sāmavidhāna Br. teacher list | 3.2 | 0.754 | **0.480** | 0.235 | Weak |
| Devāpi | Ṛgveda 10.98 | 3.6 | | | | **Disqualified**: father Ṛṣṭiṣeṇa, not Pratīpa |
| Śatānīka | Śatapatha Br. 13.5.4.19 | 1.0 | | | | **Disqualified**: father Satrājit |
| Pratīpa | AV Khila 5.15.1 | −1.4 | | | | **Disqualified** |
| Arjuna | Śatapatha Br. | −2.8 | | | | **Disqualified**: a name of Indra |
| Sahadeva | Ṛgveda 4.15 | −5.7 | | | | **Disqualified**: a Sṛñjaya |
| Bhīṣma, Pāṇḍu, the five Pāṇḍavas, Duryodhana, Karṇa, Droṇa, Drupada, Jarāsandha, Śiśupāla, Virāṭa, Śalya | none | — | | | | **No candidate** |

**Strongest case, Janamejaya.** Six independent details agree: father Parikṣit; his three brothers
Ugrasena, Bhīmasena and Śrutasena (Śatapatha 13.5.4.3; epic 1.3.1); his priest Indrota Śaunaka; and the same
episode, a horse sacrifice performed by Indrota to cleanse him of killing a Brahmin (Śatapatha 13.5.4.1; epic 12.146–148).

## 4. Findings

1. **Real people stand at the edges of the epic's family tree.** The generation after the war (Janamejaya and
   his brothers) is virtually certain. Earlier Kuru names (Bālhika, Śaṃtanu) are well matched as people.
2. **The family tree itself is not reliable.** Devāpi is real but had a different father; Śatānīka is a real king
   but not Janamejaya's son; Pratīpa's Vedic trace fails. The pattern fits Henige's finding that oral genealogies
   join real but unrelated names into one line.
3. **The war generation is unattested.** None of the central heroes (the Pāṇḍavas, Duryodhana, Karṇa, Droṇa, Bhīṣma)
   appears in any Vedic text. Absence is weak evidence (Brāhmaṇas are ritual manuals), but it is consistent across all of them.
4. **What this supports:** the Mahabharata is framed around a **real late-Vedic Kuru court** (c. 1000–800 BCE
   on standard dating of the Brāhmaṇas). Whether its central heroes were real remains open.

## 5. Limitations

- **Borrowing vs identity.** A match shows the epic's person is the Vedic person. It cannot rule out that
  the epic's poets took the name and details from the Vedic text. Existence then rests on the Vedic text,
  which for Brāhmaṇa-period kings is near-contemporary.
- **Parameters were set after the register was compiled** (see the honesty note).
- **Name counts** come from an OCR parse of the Vedic Index name index (846 persons parsed; the true number is higher).
  Names are used only for blocking, so this affects candidate selection, not scores.
- **Epic references** for Janamejaya are checked; others still need checking against the Critical Edition.
- **Lower Mykytiuk category names** still need confirming from the 2004 book.

## 6. References (to verify before submission)

Fellegi, I. P. & Sunter, A. B. (1969). A theory for record linkage. *JASA* 64(328).
Henige, D. (1974). *The Chronology of Oral Tradition: Quest for a Chimera*. Oxford.
Macdonell, A. A. & Keith, A. B. (1912). *Vedic Index of Names and Subjects*. London.
Mykytiuk, L. J. (2004). *Identifying Biblical Persons in Northwest Semitic Inscriptions of 1200–539 B.C.E.* SBL.
Mykytiuk, L. J. (2009). Corrections and updates. *Maarav* 16(1).
Vansina, J. (1985). *Oral Tradition as History*. Wisconsin.
Witzel, M. (1995). Early Sanskritization: origins and development of the Kuru state. *EJVS* 1(4).
