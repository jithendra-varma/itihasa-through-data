# Is Mykytiuk the best rule? Other methods for identifying real people in old texts

| Method | What it does | Fits our case? |
|---|---|---|
| **Mykytiuk (2004)** | Authentic data + matching setting + count of identifying marks; grades 3 / 2 / lower | Clear and citable, but **inscriptions only**. Strictly applied, it identifies no Mahabharata king. Needs adapting. |
| **Probabilistic record linkage (Fellegi & Sunter, 1969)** | Standard data-science method for deciding whether two records are the same person. Each matching field (name, father, title, place) gets a weight based on **how rare that value is**; weights add up to a match score with thresholds | **Best fit for a data-science paper.** It is Mykytiuk's mark-counting made quantitative, and it handles common vs rare names properly |
| **Name-frequency statistics** (Fuchs 2004 on the James ossuary; Feuerverger 2008, *Annals of Applied Statistics*, on the Talpiot tomb) | Estimates how many people with the same name and father would have existed, using a database of names from the period | Useful as the "rarity" input for Fellegi–Sunter; needs a Vedic names database (the Vedic Index itself could serve) |
| **Prosopography** | Builds a database of every attested person, then links records by name, filiation, office and date | The natural format for the register itself |
| **Oral tradition method (Vansina, *Oral Tradition as History*, 1985; Henige, *The Chronology of Oral Tradition*, 1974)** | Judges how reliable orally transmitted sources and king lists are; Henige shows how genealogies get lengthened and merged | **Needed**, because our sources are oral texts, not inscriptions. Replaces Mykytiuk's "authentic inscription" test |
| **Criteria of authenticity** (Meier 1991 and others: multiple attestation, embarrassment, coherence) | Judges whether a story detail goes back to a real event | Secondary: for events (the war), not for identifying people |
| **Synchronisms** (Assyriology, Egyptology) | Cross-dates kings through foreign records naming them | Only works from Ashoka onward in India |

## Recommendation

No single rule fits. The strongest setup:

1. **Fellegi–Sunter record linkage** as the scoring engine, using Mykytiuk's identifying marks as the fields.
   Report Mykytiuk-equivalent grades so historians can read the result.
2. **Vansina and Henige** for the source check, in place of Mykytiuk's inscription requirement.
3. **Name-frequency weights** from the Vedic Index, so a match on a rare name counts for more than one on a common name.

The references here are from memory; check each before citing.
