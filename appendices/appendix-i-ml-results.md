# Appendix I - Machine-Learning Results

## I.1 Evidence boundary

The completed models use only the CC BY 4.0 Xavier et al. RGB dataset and
foreground-aware colour/texture summaries. Results are
**DATA-DEMONSTRATED internal validation** for 478 fruits in one source study.
They are not an external-device, independent-season, chemistry, or deployment
validation.

Filename, fruit identity, elapsed day, image side, storage condition, and
targets were excluded from predictors. Every observation from one fruit stayed
within one fold. The split audit reports zero fruit overlap.

## I.2 Five-stage classification

Five-fold stratified, fruit-grouped out-of-fold results:

| Model | Accuracy | Balanced accuracy | Macro F1 | Ordinal MAE |
|---|---:|---:|---:|---:|
| Prior-only dummy | 0.243 | 0.200 | 0.078 | 1.977 |
| Multinomial logistic | 0.704 | 0.699 | 0.698 | 0.321 |
| Random forest | 0.737 | 0.726 | 0.727 | 0.280 |
| Histogram gradient boosting | **0.739** | **0.731** | **0.730** | **0.278** |

Fruit-cluster bootstrap 95% intervals for the selected model were:

- accuracy 0.727-0.751;
- balanced accuracy 0.719-0.743;
- macro F1 0.719-0.742;
- ordinal MAE 0.264-0.293.

## I.3 Storage-condition holdout

| Held-out group | Test fruits | Accuracy | Balanced accuracy | Macro F1 |
|---|---:|---:|---:|---:|
| 10 C / 85% RH | 192 | 0.478 | 0.497 | 0.463 |
| 20 C / 85% RH | 143 | 0.680 | 0.688 | 0.677 |
| Ambient | 143 | 0.618 | 0.632 | 0.608 |

The low 10 C result demonstrates material condition shift. It is stronger
evidence for the need for multimodal and external validation than a single
pooled score is evidence for deployment.

## I.4 Days to first observed stage 4

The retrospective target includes only observations on or before the first
record at stage 4 for the 426 fruits that reached stage 4. It contains 8,834
images and is derived from the same ordinal labels.

| Model | MAE (days) | RMSE (days) | R-squared |
|---|---:|---:|---:|
| Median dummy | 3.746 | 4.754 | -0.034 |
| Ridge | 2.158 | 2.978 | 0.595 |
| Random forest | 1.881 | 2.656 | 0.677 |
| Histogram gradient boosting | **1.853** | **2.636** | **0.682** |

The selected model's fruit-cluster bootstrap 95% intervals were 1.783-1.922
days for MAE, 2.542-2.727 days for RMSE, and 0.655-0.704 for R-squared.

## I.5 Most influential features

Permutation importance ranked red-to-green ratio, excess green, green
chromaticity, green-to-blue ratio, and foreground hue summaries highest. These
are predictive associations and do not establish that peel colour uniquely
determines internal readiness.

## I.6 Reproducibility map

- Narrative with full intervals and interpretation:
  [`reports/ml-results.md`](../reports/ml-results.md)
- Training code: [`ml/train_grouped_baselines.py`](../ml/train_grouped_baselines.py)
- Model table: [`tables/model-comparison.csv`](../tables/model-comparison.csv)
- Storage stress test:
  [`tables/storage-holdout-results.csv`](../tables/storage-holdout-results.csv)
- Split audit: [`ml/results/split-audit.csv`](../ml/results/split-audit.csv)
- Fold metrics: [`ml/results/fold-metrics.csv`](../ml/results/fold-metrics.csv)
- All out-of-fold predictions:
  [`ml/results/oof-predictions.csv`](../ml/results/oof-predictions.csv)
- Machine-readable summary:
  [`ml/results/summary.json`](../ml/results/summary.json)
- Full-data comparison artifact:
  `ml/artifacts/final_color_stage_model.joblib` (not deployment qualified)

## I.7 Required next validation

No model should be advanced to use until it is tested on independent harvest
batches and a locked season/device cohort, with instrumental firmness,
internal-condition, and a prespecified remaining-useful-life endpoint. The
storage holdout should be repeated for the multimodal model. Calibration,
subgroup error, prediction interval coverage, and abstention under domain shift
are mandatory.

