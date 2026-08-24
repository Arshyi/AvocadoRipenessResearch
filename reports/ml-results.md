# Fruit-grouped RGB baseline results

## Status and evidence boundary

**Evidence status: DATA-DEMONSTRATED within one public study only.** These
results come from the CC BY 4.0 Hass Avocado Ripening Photographic Dataset
(DOI: [10.17632/3xd9n945v8.1](https://doi.org/10.17632/3xd9n945v8.1)).
They are internal, fruit-grouped validation results. They are not evidence of
performance on a new harvest season, orchard, camera, lighting system, or
commercial deployment.

## Leakage controls

All photographs from the same biological fruit - across day, side, and repeated
measurement - were kept in the same fold. The split audit records zero fruit
overlap in every fold. Filename, fruit identity, storage condition, elapsed day,
image side, and target labels were excluded from the predictors. Models used
only foreground-aware RGB, HSV, chromaticity, grayscale, histogram, and compact
edge summaries extracted from the photographs.

Classification used five-fold `StratifiedGroupKFold` grouped by fruit.
Days-to-stage-4 regression used five-fold shuffled `GroupKFold` grouped by
fruit. Reported 95% intervals are percentile intervals from 1,000 bootstrap
resamples of whole fruit clusters, rather than independent image resamples.

## Ripening-stage classification

The target is the dataset's five-level external ripening index. It is not a
direct firmness, dry-matter, oil, moisture, or chemical measurement.

| Model | Accuracy | Balanced accuracy | Macro F1 | Ordinal MAE |
|---|---:|---:|---:|---:|
| Prior-only dummy | 0.243 [0.233, 0.251] | 0.200 [0.200, 0.200] | 0.078 [0.076, 0.080] | 1.977 [1.942, 2.011] |
| Multinomial logistic regression | 0.704 [0.693, 0.716] | 0.699 [0.688, 0.711] | 0.698 [0.687, 0.710] | 0.321 [0.305, 0.336] |
| Random forest | 0.737 [0.724, 0.750] | 0.726 [0.714, 0.739] | 0.727 [0.715, 0.739] | 0.280 [0.265, 0.296] |
| Histogram gradient boosting | **0.739 [0.727, 0.751]** | **0.731 [0.719, 0.743]** | **0.730 [0.719, 0.742]** | **0.278 [0.264, 0.293]** |

Values in brackets are fruit-cluster bootstrap 95% intervals. The test set
contains out-of-fold predictions for all 14,710 available images from 478
fruits.

The most influential permutation features for the selected model were
red-to-green ratio, excess green, green chromaticity, green-to-blue ratio, and
upper-tail foreground hue. This is consistent with external peel colour carrying
useful information, but importance is predictive rather than causal and does not
show that colour uniquely determines internal eating readiness.

## Storage-condition stress test

The selected classifier was trained on two storage groups and tested on the
third. This is a distribution-shift stress test, not an independently collected
external validation.

| Held-out storage group | Test fruits | Accuracy | Balanced accuracy | Macro F1 | Ordinal MAE |
|---|---:|---:|---:|---:|---:|
| T10 | 192 | 0.478 | 0.497 | 0.463 | 0.605 |
| T20 | 143 | 0.680 | 0.688 | 0.677 | 0.337 |
| Tam | 143 | 0.618 | 0.632 | 0.608 | 0.395 |

The large T10 degradation is the clearest warning in the benchmark: colour
relationships learned under warmer conditions do not transfer reliably to the
10 degree C group. A future model must explicitly validate temperature,
pre-storage history, season, cultivar, illumination, and device shifts.

## Days until first stage-4 observation

For fruits that reached stage 4 during follow-up, each observation on or before
the first stage-4 record was labelled with the dataset-derived number of days
remaining. This is a retrospective interval-to-an-observed-external-stage
target, not a direct measurement of remaining edible shelf life. The analysis
contains 8,834 images from 426 fruits.

| Model | MAE, days | RMSE, days | R-squared |
|---|---:|---:|---:|
| Median dummy | 3.746 [3.615, 3.876] | 4.754 [4.597, 4.908] | -0.034 [-0.054, -0.018] |
| Ridge regression | 2.158 [2.083, 2.233] | 2.978 [2.784, 3.251] | 0.595 [0.515, 0.645] |
| Random forest regressor | 1.881 [1.810, 1.948] | 2.656 [2.570, 2.740] | 0.677 [0.652, 0.699] |
| Histogram gradient boosting regressor | **1.853 [1.783, 1.922]** | **2.636 [2.542, 2.727]** | **0.682 [0.655, 0.704]** |

## Interpretation

The benchmark demonstrates that calibrated peel-colour information is useful
for this dataset, while the storage holdout demonstrates that it is not
sufficiently invariant. The results support a multimodal experimental design:
controlled RGB should remain in the sensor suite, but it should be paired with
NIR measurements, firmness, fruit mass, temperature, relative humidity, and
destructive reference assays. Any claimed remaining-life model should be
retrained against an operational endpoint defined before data collection and
validated on fruit-group-held-out batches and independent harvests.

## Reproducibility artifacts

- `ml/train_grouped_baselines.py`: complete deterministic training workflow.
- `ml/results/split-audit.csv`: fold sizes and zero-overlap audit.
- `ml/results/fold-metrics.csv`: fold-level model metrics.
- `ml/results/oof-predictions.csv`: all out-of-fold predictions.
- `ml/results/summary.json`: machine-readable point estimates and intervals.
- `tables/model-comparison.csv`: publication-ready comparison table.
- `tables/storage-holdout-results.csv`: storage-shift stress test.
- `tables/feature-importance.csv`: selected-model permutation importance.
- `ml/artifacts/final_color_stage_model.joblib`: model fitted to the full source
  dataset for reproducibility and future method comparison; it is not a
  deployment-qualified artifact.

