# Appendix H - Data Quality and Data Dictionary

## H.1 Primary dataset

The audited primary source is Xavier, Rodrigues, and Silva, *'Hass' Avocado
Ripening Photographic Dataset*, version 1 (2024), DOI
[10.17632/3xd9n945v8.1](https://doi.org/10.17632/3xd9n945v8.1), CC BY 4.0.

The immutable primary archive is
`data/raw/Hass-Avocado-Ripening-Photographic-Dataset-v1.zip`.

```text
Bytes:   418384370
SHA-256: FB14C3D8C6FB59A20BFFB579A5FE97C7EBA7030F4420882E8A75B575FF0C5BB6
```

## H.2 Reconciliation results

**DATA-DEMONSTRATED:**

| Check | Result |
|---|---:|
| Workbook records | 14,722 |
| JPEG files | 14,710 |
| Exact filename matches | 14,710 |
| Workbook rows missing an image | 12 |
| Images absent from workbook | 0 |
| Duplicate workbook filenames | 0 |
| Independent biological fruits | 478 |
| Filename/workbook metadata disagreements | 0 |
| Within-fruit, within-side stage reversals | 0 |

No missing JPEG was synthesized, imputed, or replaced. The reconciled metadata
table preserves all 14,722 workbook records with `image_present`; the feature
table contains only the 14,710 records with an available image.

## H.3 Biological and technical hierarchy

```text
study
  storage group
    biological fruit
      day/session
        side/view
          image pixels and derived features
```

The biological fruit is the minimum validation group. Image side, repeated day,
pixel, patch, or augmented copy is not an independent fruit. The defensive
project identifier is `fruit_id = storage_group + sample_id`.

## H.4 Core source and derived variables

| Variable | Unit/domain | Provenance | Modeling rule |
|---|---|---|---|
| `file_name` | string | Source workbook | Row key; never a predictor |
| `timestamp` | ISO datetime | Source workbook | Audit only |
| `storage_group` | T10/T20/Tam | Source workbook | Stress-test/covariate; excluded from image-only baseline |
| `sample_id` | 1-478 | Source workbook | Biological group; never a predictor |
| `fruit_id` | string | Derived | Mandatory split group |
| `day` | integer days | Source workbook | Longitudinal index; excluded from image-only baseline |
| `side` | a/b | Filename parse | Repeated view; excluded from predictor matrix |
| `ripening_stage` | ordered 1-5 | Source study composite index | Classification target |
| `image_present` | Boolean | File reconciliation | Quality flag |
| `first_stage4_day` | day/blank | First observed stage >=4 by fruit | Dataset-specific derived endpoint |
| `days_to_stage4_signed` | days/blank | endpoint day minus record day | Retrospective target, not independent shelf-life truth |
| RGB/HSV/gray/edge features | numeric | Reproducible image extraction | Predictor candidates |

The complete column-by-column specification, units, derivations, and
interpretation boundaries are maintained in
[`docs/data-dictionary.md`](../docs/data-dictionary.md).

## H.5 Endpoint limitations

The five-level ripening index combines external appearance and manual texture
assessment. It is not instrumental firmness, dry matter, moisture, oil,
ethylene, internal-condition, or sensory acceptability. A model trained on it
estimates the source study's operational index.

The first stage-4 day is the first *observed* record at that stage, not a
continuously observed transition. Fifty-two fruits did not reach stage 4 and 68
did not reach stage 5 during follow-up. A future event model must treat these as
censored observations rather than assigning arbitrary endpoint times.

## H.6 Quality gates for new experimental data

1. Validate identifiers, units, ranges, monotonic clocks, calibration IDs, and
   parent-child keys on ingestion.
2. Preserve raw images, spectra, and sensor counts unchanged.
3. Store calibration transforms and derived values in separate versioned
   tables.
4. Record missingness and exclusion reasons rather than deleting records.
5. Detect duplicate and near-duplicate images before splitting.
6. Assert zero fruit overlap in every model split.
7. Keep entire harvest batches and the locked external cohort outside model
   selection.
8. Link every destructive aliquot to fruit, zone, time, method, operator, and
   non-destructive history.

Machine-readable reconciliation results are in
[`reports/data-quality-summary.json`](../reports/data-quality-summary.json);
the narrative audit is
[`reports/data-quality-report.md`](../reports/data-quality-report.md).

