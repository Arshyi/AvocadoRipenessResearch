# Data Quality Report

**Run date:** 2026-07-30  
**Primary dataset:** DOI
[10.17632/3xd9n945v8.1](https://doi.org/10.17632/3xd9n945v8.1)  
**Evidence class:** **DATA-DEMONSTRATED** unless explicitly marked otherwise

## Result

The primary archive is usable for fruit-grouped longitudinal RGB analysis.
Its 14,710 JPEGs map one-to-one to workbook records from 478 independent Hass
avocados. The source workbook contains 14,722 rows, so 12 labeled records have
no corresponding image. Those rows are retained with an explicit flag and are
not imputed.

## Integrity checks

| Test | Result | Disposition |
|---|---:|---|
| Primary archive SHA-256 | `FB14C3D8C6FB59A20BFFB579A5FE97C7EBA7030F4420882E8A75B575FF0C5BB6` | Recorded in inventory |
| Workbook records | 14,722 | Preserved |
| JPEG files | 14,710 | Preserved |
| Exact stem matches | 14,710 | Pass |
| Workbook rows missing JPEG | 12 | Flagged; excluded from image models |
| JPEGs missing workbook row | 0 | Pass |
| Duplicate workbook filename | 0 | Pass |
| Filename/storage-day-sample-stage disagreement | 0 | Pass |
| Within-fruit, same-side stage reversal | 0 | Pass |
| Feature-extraction output rows | 14,710 | Pass |

## Missing source images

```text
T10_d02_072_a_1
T10_d02_072_b_1
T10_d04_065_a_3
T10_d04_065_b_3
T20_d02_141_a_2
T20_d02_141_b_2
T20_d03_192_a_1
T20_d03_192_b_1
T20_d03_212_a_2
T20_d03_212_b_2
Tam_d02_052_a_2
Tam_d02_052_b_2
```

The missing files occur as six two-sided measurement pairs. No replacement
image was synthesized and no neighboring day was copied.

## Biological independence

| Storage group | Independent fruits | Workbook records | Available JPEGs |
|---|---:|---:|---:|
| T10: 10 C, 85% RH | 192 | 8,870 | 8,866 |
| T20: 20 C, 85% RH | 143 | 2,926 | 2,920 |
| Tam: ambient | 143 | 2,926 | 2,924 |
| **Total** | **478** | **14,722** | **14,710** |

The T10 group has longer recorded sequences and therefore contributes about
60% of image rows despite representing 40% of fruits. Observation-weighted
metrics consequently give more influence to long-followed fruits. The model
report provides fruit-cluster bootstrap intervals and keeps every fruit within
one fold, but users should still examine fruit-level and storage-specific
performance.

## Target quality

The five-stage label distribution is:

| Stage | Records |
|---:|---:|
| 1 | 3,572 |
| 2 | 2,234 |
| 3 | 2,758 |
| 4 | 3,294 |
| 5 | 2,864 |

The label is an ordered, manually assessed ripening index combining peel
appearance and texture descriptions. It is not a destructive chemistry panel.
Stages 4 and 5 can support a dataset-specific operational endpoint, but they
do not independently establish edible quality, internal rot, dry matter,
moisture, or oil.

Of 478 fruits, 426 reach stage 4 or later in the recorded period and 410 reach
stage 5. Endpoint variables remain missing for other fruits rather than being
extrapolated. This is incomplete follow-up/censoring, not evidence that the
fruit would never ripen.

## Image and feature quality

Images were captured under the source study's locked lightbox procedure:
Canon EOS 60D, EF-S 18-55 mm lens, ISO 100, f/8, 1/20 s, 5500 K illumination.
The project derives RGB/HSV distribution, chromaticity, brightness, edge, and
simple foreground features. The mask deliberately removes most white
background but is not a hand-verified segmentation. Feature importance and
predictive scores must therefore be interpreted as properties of the complete
capture pipeline, including any residual shadow/background effects.

No radiometric RAW linearization, spectral reflectance calibration, or
ColorChecker correction can be reconstructed from the distributed JPEGs.
Absolute chemical interpretation is **NOT IDENTIFIABLE**.

## Auxiliary archive warning

The acquired CC BY 4.0 Kamat et al. archive
([DOI 10.17632/zysvgmxcyz.1](https://doi.org/10.17632/zysvgmxcyz.1))
is not used for model fitting. The landing page describes 14,630 images
including augmentation, but the ZIP central directory exposes 760 JPEGs,
1,334 text files, and a bundled YOLOv5 Git repository. Biological fruit IDs and
augmentation lineage are not established. Treating augmented images as
independent observations would be pseudoreplication.

## Reproduction

Run:

```powershell
$env:PYTHONPATH='C:\Users\DELL\Desktop\Avocado\tmp\python_deps'
& 'C:\Users\DELL\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' analysis\prepare_rgb_dataset.py
```

The machine-readable result is `reports/data-quality-summary.json`.
