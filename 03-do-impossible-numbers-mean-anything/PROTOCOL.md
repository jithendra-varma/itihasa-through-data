# Protocol: Do Impossible Numbers Mean Anything?

*Itihāsa Through Data*, Paper 3 (Test 4 in the book plan, a Tool test) · Draft protocol, 6 November 2026

This protocol is written before any army figure is collected. It is committed and pushed to the public repository as its timestamp. **The test will not run before 20 November 2026**, 14 days after that public timestamp, as the book's rules require. Every later change will be a dated amendment at the end of this file, with its reason. The values are in `params.json`, committed with this file.

## 1. The question

Paper 2 found that the Mahābhārata's main army numbers could not have been fielded and fed. But accounts of real wars also carry numbers that cannot be true: Herodotus gives Xerxes 5,283,220 men. So how much does a failed number say about where a story comes from?

**Primary question.** Are army numbers that could not be true more common in wars known only from one late tradition than in wars attested by independent evidence?

**Secondary questions.**
- The same, for numbers beyond the highest documented mobilization.
- Does the mix of arms (foot soldiers per chariot and elephant) differ between the two groups?
- Where do the Mahābhārata's readings from Paper 2 fall among the two groups?

## 2. What this test can and cannot show

- **It measures an association in a fixed list of wars.** It cannot show that the Mahābhārata is history or that it is legend.
- **If impossible numbers are as common in attested wars,** a failed number carries no weight on origin. Paper 2's results then say nothing about where the story comes from, only about its numbers.
- **If they cluster in unattested wars,** a failed number becomes one sign among many, to be weighed under the book's rules. It is never a verdict on its own.
- **"Unattested" does not mean "invented".** It means no independent evidence survives.

## 3. The wars: two frames, fixed now

**Frame W.** Every entry in Wikipedia's *List of battles before 301*, revision 1382889923 (30 October 2026). Wikipedia is used as a fixed, public list, not as a source of figures.

**Frame T.** Every war episode that gives a number for an army in these texts. They are chosen because they report wars from traditions that also contain legend:
- Diodorus, *Library* 1.53–58 (Sesoösis) and 2.1–20 (Ninus and Semiramis, from Ctesias);
- Homer, *Iliad* 2.484–877 (the Catalogue of Ships);
- the Hebrew Bible, Exodus to 2 Chronicles;
- Livy, Book 1;
- the *Táin Bó Cúailnge* (Recension I);
- the *Hervarar saga* (the battle of the Goths and Huns);
- the *Nihon shoki*, Books 1–10.

**Excluded:** the Mahābhārata, the Rāmāyaṇa and the Purāṇas. The Mahābhārata is the subject, and the book keeps the Rāmāyaṇa separate. The Mahābhārata's readings are compared with the frames (Q4), never pooled into them.

**One record per war.** A war that appears in both frames, or in several sources, is one record.
- Its **headline figure** is the largest force any ancient source gives for any one side. An ancient source is one written before 500 CE.
- Modern estimates are never used as figures.
- A war with no ancient force figure drops out at Stage B, whatever its class.

## 4. Classification, frozen before any figure is collected

Each war gets one class, with a one-line note of the evidence.

| Class | What it takes |
|---|---|
| **A, independently attested** | At least one of: (i) a document or inscription made within 50 years of the event that names or describes it; (ii) archaeological evidence specific to the event; (iii) two ancient narrative sources that are independent of each other |
| **U, unattested** | Known only from one tradition whose earliest surviving form is at least 300 years after the event's purported date, with none of (i) to (iii) |
| **M, middle** | Anything else |

**How it is coded:**
- From each war's name, date, place and historiography, before any force figure is extracted.
- The first pass is by an AI, which is not blind to famous figures. This is disclosed.
- A human then recodes a random 30% (seed 20261106), blind to the first pass and to all figures, before the run. Where they disagree, the human's code stands, and the share of disagreements is reported as a check on the AI pass.
- Under the book's rules, an AI never counts as a coder in a reliability figure [rules §9]. The reliability figure is Cohen's kappa between two humans coding the same 30%. If no second human is available before the run, no reliability figure is reported, and that is a stated limit.
- Every AI-coded class is labelled as such in the data.
- The polity that raised each force, and the modern countries covering its home region, are coded at the same time.

## 5. Measures

**Population.** P is the highest published estimate for the polity's home region at the nearest date. It is the larger of the HYDE 3.3 upper scenario, summed over the region's modern countries, and McEvedy and Jones (1978). For a war with a range of purported dates, the date giving the largest P is used. This favours the source, as in Paper 2.

**Mobilization ratio.** m = F / (0.30 × P), where F is the headline figure. 0.30 is the highest adult male share used in Paper 2.

| Label | Test |
|---|---|
| **Impossible by manpower** | m > 1: more men than every adult man in the region, at its highest estimate |
| **Beyond documented mobilization** | m > 0.25: more than a quarter of adult men |

**Mix of arms.** Foot soldiers ÷ (chariots + elephants), for wars that give both.

## 6. Gate

Before the main analysis, the measure is applied to three armies with modern estimates, from Paper 2's gate: Hydaspes, Panipat and the Mughal camp. Each must give m < 0.25. If any fails, the population table is too low to judge, and every answer is Not settled.

## 7. Decision rules

The book's statistical bar is p < 0.0011 (0.05 divided by 45 non-tool tests) [rules §8]. Results with 0.0011 ≤ p < 0.05 are reported as suggestive and change no answer.

**Q1 (primary).** Is the share with m > 1 higher among U wars than among A wars?
- LR = share in U ÷ share in A. Its 95% interval uses the Katz log method, with 0.5 added to every cell if any cell is zero.
- **Yes:** one-sided Fisher exact p < 0.0011, and LR > 1.
- **No:** the 95% interval for LR lies wholly inside [0.5, 2], or wholly below 1.
- **Not settled:** anything else.
- At least 30 wars with a figure are needed in each of A and U. With fewer, Q1 is Not settled.
- **What the test can detect** [rules §5]: with 30 wars per group, a difference in shares of about 50 percentage points; with 60, about 37 (preflight register). A No needs a narrow interval inside the equivalence band, so a small sample can only give Yes or Not settled.

**Q2.** The same, for m > 0.25.

**Q3.** Does the mix of arms differ? One-sided Mann–Whitney U test, with the same bar; Yes, Not settled or No as in Q1. The equivalence rule uses the ratio of medians, with the same band [0.5, 2].

**Q4 (descriptive).** Paper 2's readings are measured the same way, with P = 75 million, the highest estimate for South Asia before 1 CE:
- R1: 3,936,600, the text's own count of units, one man each;
- R2a: 18,000;
- R2b: 1,800,000;
- R3a: 16,500,000.

Each reading's percentile is reported within A and within U. Q4 has no ledger entry. It bears on origin only if Q1 is Yes.

**Sensitivity**, reported without changing an answer:
- M wars counted as A, then as U;
- each war's median ancient figure in place of its largest;
- McEvedy and Jones alone;
- Frame W alone.

**What each Q1 answer means for the book:**

| Q1 | Effect |
|---|---|
| No | Paper 2's failed numbers carry no weight on origin. The Part 6 summary says so |
| Yes | A failed number is one sign towards a tradition without independent attestation, weighed with the other tests under rules §7 |
| Not settled | No weight |

## 8. Already seen

- Herodotus's 5,283,220 and the Semiramis figures, as the test's entry in the book plan names them.
- All of Paper 2's results.
- The author and the AI know many famous ancient army figures: Xerxes, Gaugamela, the 700,000 at Muye in the *Shiji*, and the census numbers in Numbers and 2 Samuel. The classification criteria are mechanical to limit this, and the human recode is blind.
- No frame has been searched for figures, and no war's ratio has been computed.
- **Q4's ratios follow from registered values by arithmetic,** so they are known now: R1 0.17, R2a 0.001, R2b 0.08 and R3a 0.73. None exceeds 1 at South Asia's highest estimate.

## 9. Limits stated in advance

- **The frames lean towards the Mediterranean and the Near East,** because that is where ancient numbers survive.
- **Population estimates for antiquity are uncertain.** The highest estimate is used for that reason.
- **The figures have text-critical problems.** Copyists alter numbers. The largest figure is used, and the median is a sensitivity check.
- **Assigning a region is a judgment.** It is coded before any figures are seen.
- **Frame T's choice of texts is the author's.** It was fixed now, before figures, and Frame W alone is a sensitivity check.
- **The measure tests manpower only.** Paper 2's failures came mainly from grain, which needs a supply model for every war and is out of reach here. So this test bears directly on Paper 2's manpower results, and on its grain results only by analogy.

## 10. Timeline

| Stage | When | What |
|---|---|---|
| A | Now to 20 November 2026 | Freeze the frames, the classification, the regions and the population table. The human blind recode. No force figure is extracted |
| B | From 20 November 2026 | Extract figures, run the gate, then the analysis; write the paper to the Paper Standard |

## 11. Amendments

None yet.
