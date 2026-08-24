# Appendix J - Statistical Analysis Plan

## J.1 Status

This is a **PROPOSED** preregistration scaffold. Endpoint thresholds, smallest
useful effects, final sample size, and confirmatory model degrees of freedom
must be locked after the metrology/pilot stages and before confirmatory outcomes
are inspected.

## J.2 Experimental units and hierarchy

- biological unit: individual avocado;
- repeated technical/longitudinal units: scan zone, side, image, spectrum, and
  session;
- higher units: storage chamber, harvest/receipt batch, orchard/season, and
  device;
- destructive aliquots: nested within a sacrificed fruit and zone.

Images, spectra, patches, wavelengths, and days do not increase the independent
fruit count. A condition effect requires independently replicated chambers or a
design that rotates conditions across chambers without carry-over.

## J.3 Primary estimands

1. Difference in locked-batch firmness MAE between the full multimodal model
   and calibrated RGB-only baseline.
2. Difference in locked-batch remaining-useful-life MAE between a longitudinal
   multimodal model and a current-observation model.
3. Coverage of nominal 90% or 95% prediction intervals for those targets.

The stakeholder-defined smallest useful differences and non-inferiority
margins are entered before confirmatory enrollment.

## J.4 Secondary estimands

- temperature, RH, and interaction effects on softening, mass-loss, pigment,
  and respiration rate parameters;
- external RMSEP/bias/RPD for moisture, dry matter, and oil calibration;
- sensor-channel incremental value;
- entry/exit event calibration and time-dependent Brier score;
- method agreement for low-cost versus reference gas channels;
- subgroup performance by batch, device, initial maturity, mass, and internal
  condition.

## J.5 Planning design and power

The working confirmatory layout is 360 fruit:

```text
3 temperatures x 2 RH levels x 3 independent batches x 20 fruit
```

Within each condition-by-batch cell, eight fruit are longitudinal sentinels and
12 are scheduled sacrifices, three at each of four windows. The final design is
chosen by simulation from pilot variance components, serial correlation,
chamber/batch intraclass correlation, censoring, endpoint incidence, and
expected assay loss. Power is reported for the independent-unit hierarchy, not
for the number of images.

## J.6 Allocation, masking, and protocol deviations

Within batch, stratify on initial mass and a prespecified initial maturity proxy,
then randomize chamber, position, cohort role, and destructive window. Randomize
measurement order. Destructive and image-condition assessors should be blinded
to model predictions. Record deviations before opening outcome labels.

## J.7 Models

### Repeated continuous outcomes

Use hierarchical mixed-effects or Bayesian state-space models with fixed
temperature, RH, time, and interactions; random batch, chamber, and fruit
effects; and residual correlation/heteroscedasticity selected from pilot data.

### Destructive outcomes

Use condition/time fixed effects and batch/chamber random effects. Aliquots are
not treated as independent fruit. Report adjusted contrasts and marginal means.

### Interval-censored events

Use interval-censored survival with batch/chamber frailty. Fruits not reaching
an endpoint are censored. Internal-defect failure can be a competing event or a
separate endpoint depending on the signed endpoint definition.

### Prediction models

Use nested fruit-grouped development and batch/season/device outer evaluation.
All preprocessing, imputation, feature selection, calibration transfer, and
hyperparameter selection occur inside training partitions.

## J.8 Metrics

| Outcome | Primary metrics | Supporting diagnostics |
|---|---|---|
| Firmness/chemistry | MAE, RMSE, bias | R-squared, calibration slope, coverage, RPD |
| Ordinal stage | Balanced accuracy, macro F1, ordinal MAE | Per-stage recall, weighted kappa |
| Event time | Integrated Brier score, time MAE | Concordance, calibration by horizon |
| Gas method agreement | Bias and limits of agreement | LOD/LOQ, drift, response/recovery |
| Dynamic model | Held-out likelihood/error and coverage | Residual autocorrelation, parameter recovery, physical violations |

Confidence intervals use fruit- and batch-aware bootstrap or hierarchical
posterior intervals. Image-wise resampling is prohibited.

## J.9 Missingness and exclusions

Preserve reason codes for saturation, sensor failure, assay failure, fruit
damage, contamination, missed visit, and endpoint not reached. The primary
analysis population and technical QC exclusions are fixed before data lock.
Sensitivity analyses cover complete cases, model-based missingness or
multiple imputation, and plausible informative attrition.

## J.10 Multiplicity

Use a short ordered primary family or a hierarchical gate. Secondary channel and
biomarker screens use false-discovery-rate control. Report estimates and
intervals regardless of threshold crossing. Exploratory equation discovery is
clearly separated from confirmatory tests.

## J.11 Model freeze and locked test

Before unlocking the final external cohort, archive:

- source and feature schema;
- endpoint code;
- training fruit/batch manifest;
- preprocessing and calibration objects;
- hyperparameters and seed;
- model artifact hash;
- exact metrics and subgroup tables;
- abstention/domain-shift rule.

The locked cohort is evaluated once. Any modification after inspection creates
a new development cycle and requires another independent test cohort.

## J.12 Reporting

Report the flow of fruits from receipt through analysis, condition/batch/chamber
counts, exclusions, missingness, all prespecified outcomes, deviations, negative
results, intervals, subgroup uncertainty, and the complete split manifest.
Model cards must state cultivar, endpoint, equipment, calibration, population,
validation boundary, and prohibited uses.

