# Appendix K - Reproducibility and Provenance Manifest

## K.1 Environment

Locally verified on 30 July 2026:

| Component | Version |
|---|---:|
| Python | 3.12.13 |
| NumPy | 2.5.1 |
| pandas | 3.0.5 |
| Pillow | 12.3.0 |
| openpyxl | 3.1.5 |
| PyArrow | 21.0.0 |
| scikit-learn | 1.7.1 |
| SciPy | 1.16.1 |
| Matplotlib | 3.10.5 |
| seaborn | 0.13.2 |
| joblib | 1.5.1 |
| ReportLab | 4.4.9 |
| pdfplumber | 0.11.9 |
| pypdf | 6.10.0 |

The exact analysis/PDF package list is
[`reproducibility/requirements-pinned.txt`](../reproducibility/requirements-pinned.txt).
ESP-IDF, PlatformIO, camera libraries, CAD/PCB tools, and instrument SDKs are
**to be pinned** when the hardware implementation begins; Appendix F does not
pretend an unverified future version is current.

## K.2 Acquired-source identities

| Source | Bytes | SHA-256 / commit |
|---|---:|---|
| Primary Hass Mendeley ZIP | 418,384,370 | `FB14C3D8C6FB59A20BFFB579A5FE97C7EBA7030F4420882E8A75B575FF0C5BB6` |
| Kamat avocado/strawberry ZIP | 2,110,769,149 | `48B8E6B84DD3C58643F624C12689AF6E81A73E2A4CA8D7EB5BBFA7C507BE4224` |
| DeepHS annotations ZIP | 165,730 | `14275450E362684BC379A5AAF6C845CF82B0F9D5912036B9401D59A4B964A3F3` |
| DeepHS file-server readme | 298 | `F4CDD2EFC40FF49740EE7CAD118CB019E227BF119F24506194919E15380513CA` |
| Incomplete HF mirror Parquet | 301,458,815 | `05648F7B3761ED9B24A874FE08EE3BB62DAA6BAA0099D190AAC486E4737B360A` |
| Mirror workbook | 633,351 | `F8ABEABA6EEDF67869907B3A71EE132CD89B42BB3DCCE6B25DDB22E6269B51A7` |
| DeepHS official repository | - | `5f47812a3fb5bd8f0ed5367cedf9b464f83076c1` |
| RipeTrack official repository | - | `bf2a152eadfb322d55bb6345b34002e75fe97fb7` |

The machine-readable ledger is
[`reproducibility/source-checksums.csv`](../reproducibility/source-checksums.csv).
The 77.3-GB DeepHS fruit payload and RipeTrack fruit packages were not downloaded
because no explicit dataset reuse license was verified.

## K.3 Determinism and split controls

- Fixed project seed: `20260730`.
- Classification: five-fold shuffled `StratifiedGroupKFold`, group =
  biological fruit.
- Regression: five-fold shuffled `GroupKFold`, group = biological fruit.
- Random-forest estimators and gradient-boosting estimators receive the fixed
  seed.
- Fruit-cluster bootstrap: 1,000 iterations with fixed seeds.
- `ml/results/split-audit.csv` records zero fruit overlap in all ten folds.
- Predictor selection excludes fruit ID, filename, day, side, stage, and
  storage condition.
- All out-of-fold predictions are retained, not reconstructed from summary
  metrics.

Floating-point and parallel-tree results can vary at very small numerical
precision across operating systems or library builds. Scientific conclusions
must tolerate that variance; exact byte equality of all model artifacts is not
promised.

## K.4 Regeneration order

From a PowerShell prompt:

```powershell
Set-Location -LiteralPath 'C:\Users\DELL\Desktop\Avocado'
& '.\reproducibility\run_all.ps1'
```

The runner:

1. checks that the immutable primary archive and extracted dataset exist;
2. sets the workspace-local analysis dependency path;
3. regenerates metadata and image features;
4. regenerates EDA tables/figures;
5. reruns fruit-grouped ML and uncertainty;
6. redraws the prototype overview;
7. validates tables, selected metrics, split overlap, required files, and
   source checksums.

`-SkipLargeHashes` skips only checksum calculation for files above 500 MB. It
does not skip data/metric/split validation.

## K.5 Automated validation

[`reproducibility/validate_outputs.py`](../reproducibility/validate_outputs.py)
checks:

- expected row counts and unique column names for 11 CSV artifacts;
- 14,722 source records, 14,710 images/matches, and 12 missing-image records;
- zero fruit overlap;
- the selected balanced-accuracy and remaining-time MAE values;
- required proposal/model files;
- recorded source SHA-256 values.

Its machine-readable output is
`reproducibility/validation-report.json`. This is a structural and numerical
check, not a substitute for scientific peer review or claim-boundary review.

## K.6 PDF build and QA

The final PDF is built by:

```powershell
$env:PYTHONPATH='C:\Users\DELL\Desktop\Avocado\tmp\python_deps'
& 'C:\Users\DELL\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  '.\tmp\pdfs\build_proposal_pdf.py'
```

The release process renders the PDF to page images with the bundled Poppler
`pdftoppm`, inspects representative pages and montage/contact sheets, extracts
text with pdfplumber, and checks page count, blank pages, and required phrases.
All proposal dash characters are normalized to ASCII hyphens during PDF
generation to avoid renderer-specific dash substitution.

## K.7 Reproducibility boundaries

- The public RGB ground truth is an external composite ripening index, not
  instrumental chemistry.
- Dataset licenses remain source-specific.
- Current ML validation is one-study fruit-grouped validation.
- Storage holdout is a stress test, not an independent harvest.
- Candidate equations contain no fitted avocado rate constants.
- Hardware prices require re-quotation.
- A final prospective study requires preregistration, independent batches,
  device/chamber calibration, and locked external testing.

