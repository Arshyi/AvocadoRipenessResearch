# Data Dictionary

**Primary source:** Xavier, Rodrigues, and Silva, version 1, DOI
[10.17632/3xd9n945v8.1](https://doi.org/10.17632/3xd9n945v8.1)  
**License:** CC BY 4.0  
**Processed-table generation:** `analysis/prepare_rgb_dataset.py`

## File roles

| Path | Role | Rows | Mutation policy |
|---|---|---:|---|
| `data/raw/Hass-Avocado-Ripening-Photographic-Dataset-v1.zip` | Exact downloaded archive | N/A | Immutable |
| `data/raw/hass_avocado_mendeley_v1/` | Extracted raw JPEGs and source workbook | 14,710 JPEGs; 14,722 workbook rows | Immutable |
| `data/processed/hass_avocado_rgb_metadata.csv` | Reconciled longitudinal metadata, including 12 absent-image rows | 14,722 | Regenerated only |
| `data/processed/hass_avocado_rgb_features.csv` | Metadata joined one-to-one to available images and derived features | 14,710 | Regenerated only |
| `reports/data-quality-summary.json` | Machine-readable reconciliation and consistency tests | One object | Regenerated only |

## Identifier and source variables

| Variable | Type | Unit/domain | Definition and provenance | Modeling role |
|---|---|---|---|---|
| `file_name` | string | Unique source stem | Workbook filename without `.jpg`; encodes storage, day, sample, side, and stage | Row key; excluded from predictors |
| `timestamp` | ISO datetime | Local source timestamp; timezone not supplied | Source workbook capture time | Audit only |
| `storage_group` | category | `T10`, `T20`, `Tam` | Source group: 10 C/85% RH, 20 C/85% RH, or ambient | Subgroup/stress-test variable; excluded from image-only predictors |
| `sample_id` | integer | 1–478 | Source biological avocado identifier | Mandatory grouping variable; excluded from predictors |
| `fruit_id` | string | `<storage>-<sample>` | Defensive project identifier combining storage and zero-padded sample | Mandatory validation group |
| `day` | integer | Days from study start | Source workbook `Day of Experiment` | Longitudinal index; excluded from image-only predictors |
| `side` | category | `a`, `b` | Opposite photographed peel sides, parsed from filename | Repeated view; excluded from predictors |
| `ripening_stage` | ordered integer | 1–5 | Source composite ripening-index classification | Classification target |
| `image_present` | boolean | true/false | Whether a JPEG stem exactly matches the workbook row | Quality flag |
| `relative_image_path` | string | Workspace-relative path | Exact raw JPEG location, blank when missing | Data loader input; excluded from predictors |
| `image_file` | string | Filename with extension | Available JPEG name from the filesystem | Audit only |
| `image_width_px` | integer | pixels | JPEG width reported by Pillow | Quality control; excluded from baseline predictor list |
| `image_height_px` | integer | pixels | JPEG height reported by Pillow | Quality control; excluded from baseline predictor list |

## Derived endpoint variables

| Variable | Type | Unit/domain | Derivation | Interpretation boundary |
|---|---|---|---|---|
| `first_stage4_day` | integer/blank | day | Minimum observed day with source stage >=4 for that fruit | Dataset-defined shelf-life endpoint, not an instrumental or universal biological endpoint |
| `first_stage5_day` | integer/blank | day | Minimum observed day with source stage >=5 | First recorded overripe stage |
| `days_to_stage4_signed` | integer/blank | days | `first_stage4_day - day` | Derived from the same ordinal labels; not independent ground truth |
| `eligible_days_to_stage4` | boolean | true/false | Endpoint exists and current day <= first stage-4 day | Defines nonnegative remaining-time regression subset |

Fifty-two fruits never reach stage 4 in the recorded workbook, and 68 never
reach stage 5. Their endpoint values are missing rather than extrapolated.

## Image-derived feature families

All features are computed from a 96 x 96 RGB resize. A provisional foreground
mask is `mean(R,G,B) < 0.88`, which removes most of the white lightbox
background. If fewer than 256 pixels pass, the full image is used. Values are
dimensionless in the [0,1] scale unless noted. These are engineered optical
summaries, not chemical concentrations.

| Pattern / variable | Type | Definition |
|---|---|---|
| `foreground_fraction` | float | Fraction of resized pixels passing the foreground mask |
| `rgb_{r,g,b}_fg_{mean,std,q10,q50,q90}` | float | Per-channel descriptive statistics over foreground pixels |
| `rgb_{r,g,b}_all_{mean,std,q10,q50,q90}` | float | Per-channel statistics over the entire resized frame |
| `rgb_{r,g,b}_hist_{0..7}` | float | Eight-bin foreground histogram proportions for each RGB channel |
| `hsv_{h,s,v}_fg_{mean,std,q10,q50,q90}` | float | Foreground HSV descriptive statistics; hue is encoded linearly and should not be interpreted near the circular wrap point without checking |
| `gray_fg_{mean,std,q10,q50,q90}` | float | Luminance \(0.2126R + 0.7152G + 0.0722B\) summaries over foreground pixels |
| `edge_abs_mean` | float | Mean absolute first difference of luminance in horizontal and vertical directions |
| `edge_abs_q90` | float | 90th percentile of absolute horizontal/vertical luminance differences |
| `chromatic_r` | float | `mean(R) / (mean(R)+mean(G)+mean(B))` over foreground |
| `chromatic_g` | float | `mean(G) / (mean(R)+mean(G)+mean(B))` over foreground |
| `chromatic_b` | float | `mean(B) / (mean(R)+mean(G)+mean(B))` over foreground |
| `red_green_ratio` | float | Foreground mean R divided by foreground mean G |
| `green_blue_ratio` | float | Foreground mean G divided by foreground mean B |
| `excess_green` | float | `2G - R - B` using foreground channel means |
| `rgb_{r,g,b}_center_mean` | float | Channel mean in the central 48 x 48 pixels |

## Missingness and flags

- Twelve workbook records lack a JPEG. They remain in the metadata table with
  `image_present=false` and are excluded from the image-feature table.
- No JPEG lacks a workbook row.
- No duplicate source filename was observed.
- No parsed filename disagrees with the corresponding workbook storage, day,
  sample, or stage.
- No within-fruit, within-side stage reversal was observed after ordering by
  day.
- Missing endpoint values are structural censoring/limited follow-up, not
  assumed failures.

## Split contract

For every predictive analysis:

```text
group = fruit_id
```

All sides and days from one fruit remain in a single fold. `file_name`,
`relative_image_path`, `storage_group`, `sample_id`, `fruit_id`, `day`, `side`,
and endpoint/target columns are excluded from the RGB feature matrix.
