# Independent review: what went well, what can be improved, even better if

**Date:** 16 November 2026
**Reviewed:** this repository at commit `5e61159` (release v1.0.0 plus the DOI badge): the
proposal, appendices A to L, the reports, the baseline code and its retained results, the
kinetic scaffold and the bill of materials.
**Reviewer:** Claude, an AI assistant made by Anthropic, at the author's request.

## How this review was done

- The documents and code were read in full.
- The retained out-of-fold predictions were re-analysed with
  [`analysis/review_checks.py`](../analysis/review_checks.py). It uses the Python standard
  library only. Its complete output is kept in
  [`independent-review-2026-11-16-checks.txt`](independent-review-2026-11-16-checks.txt).
- A few facts outside the repository were checked by web search; sources are listed at the end.

What was not done: no model was retrained, no raw image was opened, citations and prices were
not re-verified one by one, and the full text of the source dataset's paper could not be
opened (only its abstract and the dataset page).

Each finding carries one of this repository's own evidence labels. **DATA-DEMONSTRATED**
here means "printed by `analysis/review_checks.py` from files in this repository".

## Summary

1. The leakage controls, the uncertainty treatment and the claim boundaries are sound, and
   the retained predictions made it possible to check the results without retraining.
2. The days-to-stage-4 result does not show that an image forecasts remaining time: a
   predictor that uses only the storage group and the number of days elapsed is more accurate
   (1.15 days against 1.85).
3. The planned experiment cannot observe its own primary endpoint for the fruit it follows
   over time, and three batches cannot support a claim about unseen batches.
4. The minimum prototype has no reference measurement, so on its own it produces predictors
   without targets.
5. Two statements do not match the code (feature importance, "calibrated" colour), and
   fourteen smaller points are listed in section C.

## What went well

1. **The fruit is the unit of analysis, and the code enforces it.** Every image of a fruit
   stays in one fold, the script raises if a fruit appears on both sides of a split,
   `ml/results/split-audit.csv` records zero overlap, and the confidence intervals resample
   whole fruits.
2. **The failure is reported as prominently as the success.** The 10 C holdout (balanced
   accuracy 0.497) is presented as the main warning. Check 1 of this review supports that
   reading: the 10 C fruit are not harder in themselves (0.731 when in distribution).
3. **Claims are bounded.** Evidence labels are applied consistently, the days-to-stage-4
   target is described as derived from the same labels, and nothing is called a deployment
   result.
4. **Earlier work is read critically.** The proposal notes the patch-level split in Davur et
   al., the 13 independent avocados behind RipeTrack, and that kinetic and physics-informed
   models of avocado softening already exist, so it does not claim to be first.
5. **Data rights are respected.** Datasets without a stated licence were not downloaded,
   archives are checksummed, and code and content carry separate licences.
6. **The experimental instincts are right.** Chamber-condition confounding is named,
   endpoints are to be fixed before data collection, assessors are blinded, metrology comes
   before biology, and simple hierarchical models come before neural ones.
7. **The work is reproducible.** Versions are pinned, the seed is fixed, a validator exists,
   and out-of-fold predictions for every model are kept. Without that last file this review
   could not have tested anything.

## What can be improved

### A. What the baseline shows

#### A1. A predictor with no image beats the image model on days to stage 4 (DATA-DEMONSTRATED)

Mean absolute error in days, 8,834 observations from 426 fruits. The baselines are medians
of the target within a cell, estimated with five folds split by fruit.

| Predictor | Error (days) |
|---|---:|
| Global median (the published dummy) | 3.75 |
| True current stage | 2.21 |
| **Image model as published** | **1.85** |
| Storage group + true current stage | 1.40 |
| Storage group + days elapsed, no image | 1.15 |

By storage group the calendar predictor scores 1.41 (10 C), 0.83 (20 C) and 0.65 (ambient)
against 1.93, 1.67 and 1.79 for the image model.

The reason is in the dataset, not the model. All 478 fruits started on 3 and 4 April 2022,
all at stage 1, so they ripen in step: the first stage-4 day has a standard deviation of 1.1
to 1.2 days at 20 C and ambient, and 2.6 days at 10 C. The image model was denied day and
storage group on purpose, which is the right leakage policy. The consequence is that this
benchmark cannot show that an image forecasts remaining time.

The image does carry some fruit-specific information. Within one storage group on one day,
the model's deviation from that day's median correlates with the true deviation: +0.43
(10 C), +0.22 (20 C), +0.31 (ambient), which is 5 to 19 per cent of the within-day variance.

The proposal (sections 1 and 4.3), the README and `reports/ml-results.md` present 1.853 days
and R-squared 0.682 with a median dummy as the only comparator.

*Suggested change.* Add the calendar baseline to `tables/model-comparison.csv` and to the
text. Evaluate "image + days elapsed + storage group" against "days elapsed + storage group"
on the same folds, and report the difference. In the proposed study, make "time and
temperature history, no fruit sensor" a required arm of the ablations in section 7.6 and the
comparator in H1, H2 and the estimands of Appendix J.3.

#### A2. The feature-importance statement does not match the code (DATA-DEMONSTRATED)

`reports/ml-results.md` and Appendix I say the ranking is permutation importance for the
selected model, which is the gradient-boosting classifier. `ml/train_grouped_baselines.py`
fits a random forest on all images and writes its impurity-based `feature_importances_`; the
figure title says so correctly. Either compute permutation importance for the selected model
on held-out folds, or change the two sentences.

#### A3. The storage-shift comparison is not like for like, though its conclusion holds (DATA-DEMONSTRATED)

The held-out results are compared with the pooled figure of 0.731, and holding out the 10 C
group removes 60 per cent of the training images.

| Group | Balanced accuracy, in distribution | Held out | Drop | Training images when held out |
|---|---:|---:|---:|---:|
| 10 C | 0.731 | 0.497 | 0.233 | 5,844 |
| 20 C | 0.754 | 0.688 | 0.066 | 11,790 |
| Ambient | 0.710 | 0.632 | 0.078 | 11,786 |

*Suggested change.* Report the per-group in-distribution figures next to the held-out ones,
and add a control that trains on 5,844 images when 20 C or ambient is held out, so that
shift and sample size are separated. State that each storage condition is one chamber and
one batch.

#### A4. The evaluation unit is the image, and two cheap gains are unused (DATA-DEMONSTRATED)

- Every fruit-day has two images with the same label. The two predictions disagree on 24.4
  per cent of the 7,355 fruit-days, and in 22.6 per cent exactly one side is right. The
  decision unit is the fruit on a day, so the two sides should be fused (for example by
  averaging class probabilities) and metrics reported per fruit-day.
- True stages never go backwards. Predicted stages do in 4.7 per cent of consecutive steps,
  and at least once in 309 of 478 fruits. A monotone filter over the class probabilities is
  cheap, and it is a first test of H2 and H6 on data already in hand.
- Errors are almost all between neighbouring stages (24.5 per cent of images; 1.6 per cent
  are two or more stages off). The label is a human visual and tactile index whose
  repeatability is unknown, so part of the remaining error may be label noise. The report
  could say that the achievable ceiling is unknown.

#### A5. The fruits that "never reached stage 4" were withdrawn on a schedule (DATA-DEMONSTRATED; interpretation INFERRED)

All 52 of them left before their group's last day. In each storage group five fruits have no
record after day 1, then three more stop every second day, 75 in total. The reports describe
this as limited follow-up. The regular pattern looks like planned sampling in the source
study, possibly destructive; the paper's full text could not be opened to confirm it.

*Suggested change.* Describe the censoring as scheduled withdrawal in the data-quality
report. Ask the dataset authors whether measurements exist for the withdrawn fruits; if they
do, 75 fruits have an instrumental reference and a complete image history.

#### A6. The source paper's own results are not compared (LITERATURE-SUPPORTED, abstract only)

The paper that published the dataset reports 88.8 per cent stage accuracy and an average
shelf-life deviation of 0.96 days with convolutional networks. This repository reports 73.9
per cent and 1.85 days with fruit-grouped colour features and does not mention those
figures. The gap may come from the split, the model class or the paper's "best side" rule;
the paper's split could not be checked.

*Suggested change.* Cite the paper's figures beside yours, and rerun this pipeline once with
an image-level random split to measure how much such a split inflates the result here.

### B. The proposed study

#### B1. The primary endpoint cannot be observed for the fruit followed over time (INFERRED)

The primary targets are instrumental firmness and the time for a fruit to enter a
ready-to-eat window (section 7.1). Firmness is destructive. In each condition-by-batch cell,
eight sentinel fruits are followed and never cut, and twelve are cut once (section 8.1). So
no fruit has more than one firmness value, and no sentinel has an observed entry time. H2
and the second estimand of Appendix J.3 need a remaining time per fruit, which the design
does not produce. Section 15.2 concedes that destructive cohorts approximate the sentinel
state, but the endpoint is left as it is.

*Suggested change.* Add a repeatable non-destructive firmness measurement on the sentinels:
limited compression at a fixed small deformation, or an acoustic or impact response. Mishra
et al., already cited, used both. Calibrate it on the sacrifice cohort immediately before
cutting, and define the event on the calibrated scale, interval-censored between visits.
Alternatively, state the estimand at population level and drop per-fruit remaining-time
error. Add an unhandled control group, because daily handling may itself change ripening
(risk RS-05 names this but tests it only with a timing study).

#### B2. Three batches cannot support a claim about unseen batches (INFERRED)

H1 is tested with a batch-level bootstrap and the estimands refer to a locked batch. With
three batches there are three leave-one-batch-out folds and no usable estimate of
between-batch variance. The risk table says to prioritise batches, yet the planning design
fixes three. Finding A1 adds a reason: inside one synchronised batch the fruits differ by
about a day at room temperature, so most of what a sensor could explain lies between batches
and between fruits with different histories.

The same 360 fruits also fund six conditions with two chambers each. Twelve controlled
chambers or chamber cycles are assumed, and neither budget tier contains storage or humidity
control.

*Suggested change.* Fewer conditions and more batches, for example two temperatures, one
humidity and eight to ten batches entered on different dates. Cost the storage hardware.
Saturated salt solutions are an inexpensive way to hold humidity (potassium chloride gives
about 85 per cent near 20 C).

#### B3. Where the fruit comes from is not specified (INFERRED)

"Harvest or receipt batch" is left open. Fruit bought at retail in an importing country has
usually spent weeks in a cold chain and may have been conditioned with ethylene before sale;
confirm this with the supplier. Its ripening time then depends mainly on a history the study
cannot see. The motivation is consumer and retail waste, while the design is a physiological
chamber experiment. Choose one: sample as shoppers do across many purchase lots, or obtain
fruit of known harvest date through a packer or importer.

#### B4. The minimum prototype cannot test the primary hypothesis (DATA-DEMONSTRATED from the bill of materials)

- It has no reference measurement. The penetrometer (`RG-011`) is in the research tier, and
  no oven or balance for dry matter is in the MVP tier.
- The mass channel is a 10 kg load cell. The catalogue justifies it by saying resolution
  comes from the mechanics and converter, but a load cell's creep, hysteresis and thermal
  drift are fractions of its full scale. The fruit weighs a few hundred grams and probably
  loses a gram a day or less (an estimate to confirm in metrology). A 0.01 g balance or a
  cell of 1 kg or less suits the signal.
- Fruit from 10 C storage is measured in a warmer bay. Condensation adds mass and glare, and
  the carbon dioxide slope then reflects a fruit that is warming. Section 8.3 asks for short
  transfers but does not fix the bay temperature. Measure inside the storage environment, or
  log fruit surface temperature and set an equilibration rule.
- Four LEDs and one photodiode in reflectance mostly see the skin. The proposal already
  hedges this with a stop rule. The 11-channel sensor listed as optional (`OPT-001`,
  US$18.95) and a separated, shielded source and detector would add information at low cost.

#### B5. Commercial and industry context is missing (LITERATURE-SUPPORTED, trade press)

The review of prior work covers papers only. A near-infrared scanner that reports avocado
ripeness and expected shelf life to shoppers (OneThird) has been in retail trials since
2023, including an Australian trial in 2026, and a handheld near-infrared dry-matter meter
made for avocado (Felix Instruments F-751) is sold commercially. Neither appears in the
proposal. Industry firmness-based ripeness stages also exist and could anchor the endpoint
instead of a new definition; this last point was not verified for this review.

*Suggested change.* Add a short section on existing devices and state the contribution
against them: an open, audited benchmark and protocol with published error, which the
commercial products do not provide.

#### B6. The kinetic scaffold is not connected to what the prototype measures (DATA-DEMONSTRATED from the code)

`models/kinetic/candidate_models.py` has eight states and thirty parameters. It has no
respiration or carbon dioxide state and no total-mass output, although the scale and the
carbon dioxide sensor are two of the four MVP channels. Its ethylene rates do not depend on
temperature, while section 5.4 writes them as functions of temperature, and latent ripeness
is an outside input, not a state. There is no observation model.

*Suggested change.* Add observation functions for mass and headspace carbon dioxide. Before
buying hardware, simulate the planned sampling schedule with published parameter ranges and
check which rates can be recovered from three temperatures.

### C. Smaller points

Each of these was checked against the files named.

1. **"Calibrated" colour.** `reports/ml-results.md` (Interpretation) and the outreach draft
   say the public-data result concerns calibrated peel colour. The feature code
   (`analysis/prepare_rgb_dataset.py`) applies a brightness mask and no colour reference.
   The accurate wording is "peel colour from uncalibrated lightbox photographs".
2. **Ablations in the ledger.** `PROGRESS_LEDGER.md` records Phase 4 as complete "with
   frozen splits, bootstrap intervals, feature importance, ablations, and storage holdouts".
   No ablation result exists under `ml/`, `tables/` or `reports/`. Add one or remove the
   word.
3. **The "best" classifier is not distinguishable from the runner-up.** Gradient boosting
   scores 0.731 [0.719, 0.743] and the random forest 0.726 [0.714, 0.739]. The winner is
   also chosen on the folds it is scored on, and no hyperparameter was tuned. Say the two
   are equivalent here.
4. **The holdout table has no intervals.** `tables/storage-holdout-results.csv` gives point
   values only. The fruit-cluster bootstrap used for the main table applies unchanged.
5. **The dataset holds two regimes, not three.** The 20 C and ambient groups behave alike
   (median first stage-4 day 7 in both, standard deviations 1.16 and 1.10). When either is
   held out its twin is still in training, so only the 10 C holdout tests a real shift.
6. **Per-fruit error deserves a look.** Fruit-weighted accuracy is 0.748 against 0.739
   image-weighted, and 16 of 478 fruits are below 0.5. Listing those fruits by storage
   group and trajectory would show whether the errors cluster.
7. **One predictor is not a colour feature.** `foreground_fraction` measures how much of
   the frame the fruit fills. It ranks 44th of 86 by importance, so it matters little, but
   it can carry fruit size or session information. Drop it, or show the result is
   unchanged without it.
8. **The regression drops fruits a survival model would keep.** The 52 withdrawn fruits
   and every record after stage 4 are excluded. With scheduled withdrawal this is benign,
   and a discrete-time survival model, which Appendix J already plans for the new study,
   would use them. The target also has one-day resolution because visits were daily.
9. **Three hypotheses are hard to test as written.** H4 has a two-part alternative and a
   two-part null; split it. H6 relies on a "predeclared composite" with no weights; define
   them. H8 takes agreement as the null, so an underpowered comparison leaves agreement
   standing; if a low-cost channel is ever to carry an ethylene label, test equivalence
   with disagreement as the null.
10. **The budget omits what produces the targets.** There is no line for fruit (360 plus
    the pilot), for storage hardware, or for assay and instrument time beyond a US$500
    consumables allowance. The US$723.62 headline therefore buys sensors only.
11. **The plan assumes a team that is not named.** It needs an endpoint panel of four
    roles, blinded assessors and daily operators over fifteen months. State the minimum
    people and hours.
12. **Outsiders cannot rerun the pipeline easily.** `reproducibility/run_all.ps1` is
    PowerShell only, looks first for an interpreter at a path specific to one machine, and
    does not fetch the raw archive. A cross-platform entry point with a fetch-and-verify
    step would close this.
13. **Licence metadata disagrees with itself.** `CITATION.cff` declares `license: MIT`
    while its `license-url` points to `LICENSE-CONTENT.md`, the CC BY 4.0 file, and most of
    the deposit is CC BY content. Archives read the licence from this file.
14. **The shipped model is a pickle.** `ml/artifacts/final_color_stage_model.joblib` runs
    code when loaded and needs the pinned library versions. A sentence beside it would warn
    readers.

## Even better if

1. **A first pilot that one person can run.** Forty to sixty fruits from six to eight
   separate purchases, kept at room temperature and measured daily: locked-exposure
   photographs with a colour card, mass to 0.01 g, and a non-destructive compression
   reading. Cut a third of them on a schedule for penetrometer firmness and oven dry matter.
   One question: does any measurement beat the calendar for an individual fruit, within a
   purchase and across purchases? The answer decides whether the larger study is worth
   funding, and it supplies the variance estimates the power simulation needs.
2. **The leakage premium as a number.** A random image split against a fruit-grouped split
   on the public dataset, same features and model. It is the repository's central
   methodological point, and one small table would make it.
3. **A sequence model on the data already here.** Fuse the two sides, enforce monotone
   stages, include days elapsed, forecast the stage-4 day, and report the gain over the
   calendar.
4. **The withdrawn-fruit measurements,** if the dataset authors have them.
5. **Two primary hypotheses instead of eight,** each with the calendar as comparator and a
   smallest useful difference fixed in advance.
6. **Outreach to named laboratories.** The draft message is general. A version for a
   specific postharvest group, stating which instrument is needed and for how long, is more
   likely to get an answer.

## Reproducing the checks

```text
python analysis/review_checks.py
```

It reads `ml/results/oof-predictions.csv`, `data/processed/hass_avocado_rgb_metadata.csv`
and `tables/storage-holdout-results.csv`, and prints eight sections. The retained output is
`reports/independent-review-2026-11-16-checks.txt`.

## Limits of this review

- The checks re-read stored predictions. They do not replace a retrained comparison such as
  the one suggested in A1.
- The baselines in A1 are cell medians. They use the day and the storage group, which the
  image model was correctly not given; the comparison shows what the benchmark can
  establish, not that the model was built badly.
- Statements about commercial devices come from trade press and manufacturer material.
- Section B is a reading of plans, not of results, and other designs could answer the same
  questions.

## Sources checked outside the repository

- Xavier, Rodrigues and Silva (2024), abstract:
  <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11049431/>
- Dataset page: <https://data.mendeley.com/datasets/3xd9n945v8/1>
- OneThird scanner, 2023 announcement:
  <https://www.freshplaza.com/north-america/article/9490044/onethird-solves-the-avocado-problem-and-addresses-one-trillion-dollar-food-waste-challenge-at-ces-2023/>
- OneThird scanner, 2026 Australian trial:
  <https://www.freshfruitportal.com/news/2026/03/20/avo-scanner-australia/>
- Felix Instruments avocado quality meter:
  <https://www.freshfruitportal.com/news/2019/05/02/felix-instruments-launches-major-upgrade-to-avocado-quality-meter/>
