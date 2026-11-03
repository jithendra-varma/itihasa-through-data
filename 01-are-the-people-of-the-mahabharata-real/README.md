# Paper 1: Are the People of the Mahābhārata Real?
### A Pre-Registered Record-Linkage Test Against the Vedic Corpus

*Itihāsa Through Data*, Paper 1 · Jithendra Varma Chamarthi ([ORCID 0000-0001-9467-5612](https://orcid.org/0000-0001-9467-5612))

**Published:** Zenodo, [doi:10.5281/zenodo.23875710](https://doi.org/10.5281/zenodo.23875710) (all versions; v1.0.1 = 10.5281/zenodo.23906648)

## Finding in one paragraph
Every person in the epic's main lineages and embedded stories (107) was compared with every person record in the
Vedic Index of Names and Subjects (2,051), using a pre-registered method that combines oral-tradition criticism,
Mykytiuk's identifying-mark criteria and Fellegi–Sunter record linkage. The court of **Janamejaya**, the generation
after the war, is securely attested in the Śatapatha Brāhmaṇa together with the same episode the epic tells.
Earlier Kuru figures are real Vedic names placed in a new genealogy. The war generation itself (the Pāṇḍavas,
the Kauravas, Bhīṣma, Droṇa, Karṇa, Draupadī) is **not yet found** in the older texts.

## The proofs: where to look
| Claim | Evidence in this folder |
|---|---|
| The method was fixed before the results | [`PROTOCOL.md`](PROTOCOL.md): assumptions, rules, pass criteria, and seven dated amendments |
| The method works better than chance | [`results/v3_battle_tests.json`](results/v3_battle_tests.json): permutation test, p = 0.001 |
| False positives are under 1% | Same file: T2, 0.48% of 219,343 wrong-name pairs |
| Known identities are recovered | Same file: T3, 7 of 9 |
| Version 1 failed, and how it was fixed | [`results/battle_tests.json`](results/battle_tests.json) (v1), [`results/v2_battle_tests.json`](results/v2_battle_tests.json), [`PROTOCOL.md`](PROTOCOL.md) amendments |
| Every match was read by hand | [`results/clerical_review.csv`](results/clerical_review.csv) |
| A blind second review agrees | [`review/second_review.csv`](review/second_review.csv), [`review/agreement.md`](review/agreement.md): κ = 1.00 on identity |
| Final verdicts | [`results/adjudicated_verdicts.csv`](results/adjudicated_verdicts.csv) |
| Epic relationships checked against the Critical Edition | [`RESULTS.md`](RESULTS.md) §7 and the paper's Table V |
| How the method developed | [`background/`](background/): first hand registers and the methods comparison |

## Folders
| Folder | Contents |
|---|---|
| `paper/` | LaTeX source, PDF, figures, arXiv-ready bundle, plain-text abstract |
| `data/` | `epic_people.json`, the epic side, coded from the epic's genealogies |
| `scripts/` | Parsing, linkage (v1 `link.py`, v2 `link_v2.py`, v3 `link_v3.py`), epic dataset builder |
| `results/` | Every run's outputs, battle tests and the hand review |
| `review/` | The blind second review and inter-rater agreement |
| `release/` | Licences, citation file, Zenodo metadata, `fetch_sources.sh` |
| `background/` | Working notes from before the full test |

## Reproduce
```bash
bash release/fetch_sources.sh          # downloads the Vedic Index texts (not redistributed) and checks checksums
python3 scripts/build_epic_people.py
python3 scripts/build_vedic_persons_v2.py data/vedic_index_cologne_vei.txt
python3 scripts/link_v3.py             # writes results/v3_* and prints the battle tests
```
Third-party texts (the Cologne Vedic Index transcription, the 1912 scan text, the Critical Edition) are not included;
the fetch script retrieves the first two, and the Critical Edition is cited.

## Licence
Code MIT; data, text and paper CC BY 4.0. See [`release/LICENSE.md`](release/LICENSE.md).
