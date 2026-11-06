# Your blind recode (Paper 3, Stage A)

`author_blind_recode_sheet.csv` lists 248 wars: a random 30% of the frame (seed 20261106), plus the cases where coders disagreed or one battle may be listed twice. They are shuffled, so the two kinds can't be told apart. Your code stands wherever it differs from the AI first pass.

## Keep it blind

- **Don't open** `../stageA_frozen_ai_first_pass.csv`, `../stageA_merged_ai_first_pass.csv` or anything in `../stageA/` until you've finished. They hold the AI's classes.
- **Don't look at army sizes.** On Wikipedia, skip the infobox's Strength and Casualties rows and any sentence giving numbers of soldiers, ships or dead. Use the article's sources and historiography only. For Frame T episodes (ids starting `T-`), read the passage for who fought, not how many.

## The classes (PROTOCOL.md §4, Amendments 1 and 2)

| Class | What it takes |
|---|---|
| **A** | (i) a written source composed within 50 years of the event that names or describes it. This includes narrative histories, and lost sources explicitly cited by a later author for this event. Or (ii) archaeology specific to the event. Or (iii) two ancient narrative sources independent of each other: neither derived from the other, nor both from one source |
| **U** | Known only from one tradition whose earliest surviving form is 300 years or more after the event's purported date, with none of (i) to (iii). For texts first composed orally, use the scholarly date at which the text was fixed |
| **M** | Anything else |

Fill in `your_class`, `your_criterion` (i, ii or iii for A; "late single tradition" for U; a few words for M) and a one-line `your_evidence_note`. If a row looks like the same battle as another row, say so in the note.
