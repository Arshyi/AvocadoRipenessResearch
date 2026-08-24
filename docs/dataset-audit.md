# Dataset Discovery, Acquisition, and Suitability Audit

**Audit date:** 2026-07-30  
**Scope:** Public and cited datasets relevant to non-destructive avocado ripeness, remaining shelf life, and internal-quality estimation  
**Machine-readable inventory:** [`../data/dataset_inventory.csv`](../data/dataset_inventory.csv)

## Executive finding

Only one located fruit-ripening dataset is both clearly reusable and suitable
for immediate longitudinal avocado analysis: Xavier, Rodrigues, and Silva's
[`'Hass' Avocado Ripening Photographic Dataset`](https://data.mendeley.com/datasets/3xd9n945v8/1)
(CC BY 4.0, DOI
[10.17632/3xd9n945v8.1](https://doi.org/10.17632/3xd9n945v8.1)).
Its complete primary archive has been downloaded, checksummed, extracted, and
inspected. It contains 14,710 JPEGs linked to 478 biological fruits. Its
workbook contains 14,722 rows; exactly 12 rows have no corresponding JPEG.

RipeTrack and DeepHS Fruit expose public download links, but neither the
dataset landing material nor the inspected repository states a dataset
license. Public accessibility is not equivalent to permission to reproduce,
redistribute, or train deployable models. Their large binary payloads were
therefore not acquired. Small code/annotation artifacts were retained only for
schema and reproducibility inspection and are marked `LICENSE_BLOCK`.

The main implication is methodological: image count is not sample size. All
days, sides, patches, spectra, and views from a single avocado must remain in
one validation partition. A model evaluated by random image or patch splitting
can memorize the fruit, lighting, day sequence, or source image while appearing
to generalize.

## Evidence vocabulary

- **DATA-DEMONSTRATED:** observed directly in downloaded, inspected files.
- **LITERATURE-SUPPORTED:** reported by a primary source but not reproduced
  here.
- **INFERRED:** a reasoned interpretation not directly measured.
- **PROPOSED:** planned future method.
- **NOT IDENTIFIABLE:** the available data cannot support the quantity or
  causal claim.

## Acquired datasets

### 1. Primary longitudinal Hass RGB dataset

**Source.** Pedro Xavier, Pedro Rodrigues, and Cristina L. M. Silva,
`'Hass' Avocado Ripening Photographic Dataset`, version 1 (2024), DOI
[10.17632/3xd9n945v8.1](https://doi.org/10.17632/3xd9n945v8.1), licensed
CC BY 4.0. The associated study is
[Shelf-Life Management and Ripening Assessment of 'Hass' Avocado Using Deep Learning Approaches](https://doi.org/10.3390/foods13081150).

**Acquisition.** The exact 418,384,370-byte primary ZIP was downloaded from
Mendeley Data and stored at
`data/raw/Hass-Avocado-Ripening-Photographic-Dataset-v1.zip`. Its SHA-256 is:

```text
FB14C3D8C6FB59A20BFFB579A5FE97C7EBA7030F4420882E8A75B575FF0C5BB6
```

**DATA-DEMONSTRATED contents.**

| Quantity | Inspected value |
|---|---:|
| Biological fruits | 478 |
| Workbook rows | 14,722 |
| JPEG files | 14,710 |
| Matched workbook/JPEG rows | 14,710 |
| Workbook rows without a JPEG | 12 |
| Unlisted JPEG files | 0 |
| Duplicate workbook filenames | 0 |
| Storage assignment | 192 fruits at 10 C/85% RH; 143 at 20 C/85% RH; 143 ambient |
| Stage-record counts | 3,572 / 2,234 / 2,758 / 3,294 / 2,864 for stages 1–5 |
| Filename-to-workbook disagreements | 0 |
| Within-fruit, within-side stage reversals | 0 |

The workbook labels each record with filename, timestamp, storage group, sample
number, day, and a five-level ripening index. The filename also encodes storage,
day, sample, side, and stage; those encodings agree with the workbook for every
row.

**Ground-truth limitation.** The ripening index is an operational composite
based on peel appearance and manual texture assessment. It is not a
destructive chemical assay, instrumental firmness measurement, ethylene
measurement, or internal-disorder label. A model trained on it estimates this
study's index, not dry matter, moisture, oil, edible quality, or universal
remaining shelf life.

**Validation rule.** `sample_id` is the biological grouping variable.
`fruit_id = storage_group + sample_id` is used defensively even though the 478
sample numbers are unique. The two sides and every day of a fruit stay in the
same fold.

### 2. Auxiliary four-stage avocado/strawberry archive

**Source.** Kamat et al.,
[Comprehensive Dataset on Ripening Stages of Strawberries and Avocados: From Unripe to Rotten](https://data.mendeley.com/datasets/zysvgmxcyz/1),
version 1 (2024), DOI
[10.17632/zysvgmxcyz.1](https://doi.org/10.17632/zysvgmxcyz.1), CC BY 4.0.

The 2,110,769,149-byte archive was downloaded and checksummed:

```text
48B8E6B84DD3C58643F624C12689AF6E81A73E2A4CA8D7EB5BBFA7C507BE4224
```

The landing page advertises 1,333 original images and 14,630 total images after
augmentation. **DATA-DEMONSTRATED:** the ZIP's central directory exposes only
760 `.jpg` entries and 1,334 `.txt` entries, plus a bundled YOLOv5 source
repository (including its `.git` objects). The advertised augmentation lineage,
biological fruit IDs, and ordinary-image count are not recoverable directly
from the archive structure. The archive is retained intact for provenance but
is excluded from longitudinal modeling and performance claims.

## Publicly linked but license-blocked datasets

### DeepHS Fruit v2

The [official repository](https://github.com/cogsys-tuebingen/deephs_fruit)
links to an [institutional file index](https://cogsys.cs.uni-tuebingen.de/webprojects/DeepHS-Fruit-2023-Datasets/).
The index advertises a 77,300,002,282-byte `Avocado.zip`; the repository states
that labels include fruit flesh firmness, ripeness, and sugar where applicable.
The v1 paper is
[Measuring the Ripeness of Fruit with Hyperspectral Imaging and Deep Learning](https://doi.org/10.1109/IJCNN52387.2021.9533728).

No `LICENSE` file or dataset reuse statement was found in the inspected
repository or file index. The full 72-GiB avocado package was therefore not
downloaded. The 162-KB official annotations package and shallow repository
commit `5f47812a3fb5bd8f0ed5367cedf9b464f83076c1` were retained for schema
inspection only. They must not be redistributed as though their reuse terms
were known.

The published unit structure also requires care: front/back camera recordings
and repeated records can represent the same fruit. Any use requires a verified
fruit identifier before splitting.

### RipeTrack

The [RipeTrack repository](https://github.com/ShahzaibWaseem/RipeTrack) links
Google Drive packages for Hass avocado, organic avocado, other fruit, and a
mobile RGB+NIR subset. The paper is Muhammad Shahzaib Waseem, Neha Sharma, and
Mohamed Hefeeda,
[RipeTrack: Assessing Fruit Ripeness and Remaining Lifetime Using Smartphones](https://doi.org/10.1109/TMC.2025.3599917).

**LITERATURE-SUPPORTED:** RipeTrack contains 13 independent avocado fruits
(10 organic and 3 Hass), 694 avocado hyperspectral images, and 347 avocado
ethylene readings. Its overall study contains 48 fruits, 1,913 HSI images,
1,144 gas readings, and 3,865 mobile RGB-NIR pairs. Labels are derived from
ethylene trajectories.

No dataset license was found in the inspected repository. Only the code
repository at commit `bf2a152eadfb322d55bb6345b34002e75fe97fb7` was cloned
for audit. The linked 8.2-, 16.8-, and 12.2-GB avocado packages were not
downloaded.

## Cited datasets not publicly downloadable

| Source | Independent units | Access | Suitability finding |
|---|---:|---|---|
| [Davur et al. 2023](https://doi.org/10.3390/horticulturae9050599) | 80 Hass fruits, 551 HSI source images | Unavailable due IP arrangements | Published patch allocation sends patches from each source image to train/validation/test. Reported patch results do not establish unseen-fruit generalization. |
| [Han et al. 2023](https://doi.org/10.1007/s11119-023-10022-y) | 316 Hass + 160 Shepard | Reasonable request | Fruit-level PLSR split is useful; subimage DCNN splitting may leak fruit identity. |
| [Lee, Li, and Ma 2025](https://doi.org/10.1016/j.crfs.2025.101196) | 140 fruits, 1,400 images, two batches | Reasonable request | Random image split can leak fruit identity; supplementary cross-batch evaluation is more credible and shows directional dataset shift. |
| [Pinto et al. 2019](https://doi.org/10.22430/22565337.1232) | 7 fruits over about 10 days | Dataset unavailable | Too few independent fruits for defensible predictive training. |

## Leakage and pseudoreplication audit

The project adopts the following non-negotiable split hierarchy:

1. all patches or pixels from one source image remain together;
2. both sides, scan zones, devices, and repeated days of one fruit remain
   together;
3. tuning occurs inside the training fruits only;
4. a final external assessment withholds a harvest batch, orchard, season, or
   acquisition device when such data exist;
5. image count is never used as the denominator for biological independence.

This distinction changes interpretation:

- a patch-level score estimates discrimination of patches sampled from already
  represented source images;
- an image-level score estimates discrimination of new images and may still
  include the same fruit;
- a fruit-grouped score estimates new-fruit generalization within the study;
- a batch/season/device holdout probes domain shift;
- only a genuinely independent prospective cohort supports deployment claims.

## Dataset gaps

No inspected dataset jointly measures longitudinal RGB/NIR, mass, temperature,
RH, airflow, firmness, CO2, ethylene, VOCs, moisture, dry matter, oil, starch,
soluble solids, pigments, and internal condition. Therefore:

- internal moisture, oil, and starch-conversion rates are **NOT IDENTIFIABLE**
  from the downloaded RGB dataset;
- a peel-color model cannot be represented as an internal-quality model;
- causal temperature/RH effects are **NOT IDENTIFIABLE** without a controlled
  randomized storage experiment and full environmental records;
- literature equations may be proposed and structurally tested, but their rate
  constants must not be fitted to missing variables.

These gaps directly motivate the matched longitudinal/destructive-cohort
experiment specified elsewhere in this workspace.
