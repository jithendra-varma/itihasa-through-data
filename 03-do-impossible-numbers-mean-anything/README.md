# Paper 3: Do Impossible Numbers Mean Anything?

*Itihāsa Through Data*, Paper 3 (Test 4 in the book plan, a Tool test) · **Protocol registered; the test runs no earlier than 20 November 2026**

## The question

Paper 2 found that the Mahābhārata's main army numbers could not have been fielded and fed. But real wars carry impossible numbers too. This test asks whether impossible army numbers are more common in wars known only from one late tradition than in wars attested by independent evidence. The answer sets how much weight a failed number carries on where a story comes from.

## Where it stands

| Stage | Status |
|---|---|
| Protocol and inputs (`PROTOCOL.md`, `params.json`) | Written; to be committed and pushed as the public timestamp |
| A: frames, classification, regions, population table, human blind recode | To do before 20 November 2026. No army figure is extracted |
| B: figures, gate, analysis, paper | From 20 November 2026 |

## Stage A checklist

- [x] Extract Frame W's battle names, dates and places from revision 1382889923, with no army figures: **775 battles**, in `data/frame_w.csv`, by `extract_frame_w.py`, which drops the description column unread
- [x] Amendment 1: five coding clarifications, made before any figure was seen
- [x] List Frame T's war episodes by passage, with no army figures: 31 Hebrew Bible episodes and 17 from the other texts
- [x] Class each war A, U or M with an evidence note: the AI first pass, labelled as such (`data/stageA/`, checked by `validate_stageA.py`)
- [x] Amendment 2 (the author's decisions): whole realm as region, sub-national areas, Frame T army rule, conflicts to the author, lost-source rule
- [x] Merge records of the same war, and drop Frame T counts that are not armies: **815 records, 810 kept**; AI classes among the kept: 456 A, 66 U, 288 M (`data/stageA_frozen_ai_first_pass.csv`, by `freeze_stageA.py`)
- [ ] **Author:** blind recode of the 248 rows in `data/recode/author_blind_recode_sheet.csv` (read `data/recode/README.md` first)
- [ ] Recode regions to sub-national areas where a polity held part of a country (Amendment 2.2)
- [ ] Build the population table (HYDE 3.3 upper, McEvedy and Jones) by region and date. **Needs the author:** HYDE 3.3's download page is behind bot protection, so it has to be downloaded in a browser from the Utrecht University catalogue (https://catalog.data.uu.nl/dataset/oai-10-24416-uu01-67uhb4)
- [ ] Draw the 30% recode sample (seed 20261106). The author recodes it blind, and a second human coder if one can be found
- [ ] Commit the frozen Stage A files before 20 November 2026

Follows the book's pipeline (`book-plan/PIPELINE.md`) and Paper Standard.
