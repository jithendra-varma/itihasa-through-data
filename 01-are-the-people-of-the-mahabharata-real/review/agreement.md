# Second review and inter-rater agreement

**Design.** A second reviewer (an AI model run separately, given only `review_packet.json`: the epic record and the
candidate Vedic Index entries, in shuffled order, with no automatic scores and no first-review verdicts) judged 61 people
with the same verdict categories. The second reviewer is not a human Sanskritist; a human second review remains the
recommended next step.

**Agreement on the 37 people both reviewers judged** (Cohen's kappa):

| Level | Agreement | Kappa | Reading |
|---|---|---|---|
| Is the epic person the Vedic person? (accept / reject) | 37 / 37 | **1.00** | perfect |
| Identified / same figure but legendary / not identified | 32 / 37 | **0.77** | substantial |
| Exact grade | 22 / 37 | **0.52** | moderate |

**Where they differed.** Never on identity. Five cases differ on historical vs legendary (Vyāsa, Kalmāṣapāda, Vasiṣṭha,
Yayāti, Viśvāmitra); five differ on grade 3 vs grade 2, the second reviewer being stricter each time (Śrutasena, Bālhika,
Yājñavalkya, Māndhātṛ, Bharata).

**Adjudication rule (conservative).** Agreement stands. Grade 3 vs 2: the lower grade. Identified vs legendary:
"same figure, historicity disputed". People judged by one reviewer only are marked as such.
Final verdicts: `results/adjudicated_verdicts.csv`.
