# Appendix G - Repository Structure

## G.1 Implemented workspace

```text
Avocado/
  analysis/
    inspect_downloads.py
    prepare_rgb_dataset.py
    run_eda.py
    draw_prototype_overview.py
  appendices/
    appendix-a-existing-papers.md
    ...
    appendix-l-risk-evidence.md
  communications/
    collaborator-outreach-draft.md
  data/
    dataset_inventory.csv
    raw/                    immutable source archives and inspected repositories
    processed/              reproducibly derived metadata and RGB features
  docs/
    dataset-audit.md
    data-dictionary.md
    prototype-architecture.md
  figures/                  generated EDA, ML, and architecture figures
  ml/
    train_grouped_baselines.py
    artifacts/              reproducibility artifacts, not deployment models
    results/                folds, splits, OOF predictions, machine summaries
  models/
    kinetic/                candidate ODE scaffold and documentation
    sciml/                  scientific-ML implementation plan
  Papers(toReadAndCiteMaybeLater)/
                            user-supplied source PDFs
  procurement/
    bill-of-materials.csv
    equipment-catalogue.md
    source-ledger.md
    images/                 licence-verified exact-product photographs
  proposal/
    avocado-research-proposal.md
  reports/                  QA, EDA, and ML narrative reports
  reproducibility/
    requirements-pinned.txt
    source-checksums.csv
    validate_outputs.py
    run_all.ps1
  tables/                   publication-ready machine-readable tables
  output/pdf/               final rendered deliverable only
  tmp/                      disposable extraction, render, and support files
```

## G.2 Future experimental extensions

```text
firmware/
  esp32/                    sensor acquisition, LED control, SD logging
  raspberry-pi/             locked camera acquisition and session trigger
pcb/
  kicad/                    schematics, layout, BOM, fabrication outputs
cad/
  chamber/
  optical-fixture/
  fruit-cradle/
data/
  raw/
    study_id/device_id/date/session_id/
  calibration/
  interim/
  processed/
protocols/
  metrology/
  biological/
  destructive-assays/
  safety/
schemas/
  session.schema.json
  sensor-record.schema.json
  destructive-record.schema.json
models/
  chemometrics/
  temporal/
  fusion/
  kinetic/
  sciml/
tests/
  firmware/
  schema/
  analysis/
  model-splits/
model-cards/
preregistration/
```

## G.3 Data-layer contract

1. **Raw:** byte-preserved device/source output. Never edited.
2. **Calibration:** dark, white, colour, mass, gas, wavelength, blank, leak,
   and response records.
3. **Interim:** decoded but not scientifically transformed records.
4. **Processed:** validated, calibrated observations linked to immutable raw
   IDs and code/calibration versions.
5. **Features:** fold-safe derived predictors.
6. **Results:** split manifests, predictions, metrics, uncertainty, and
   diagnostics.

Every derived file must be reproducible from a lower layer. Destructive samples
retain fruit, session, zone, method, aliquot, operator, and calibration keys.

## G.4 Naming and identity rules

- `fruit_id` identifies the biological unit and never changes.
- `batch_id`, `chamber_id`, `device_id`, and `calibration_id` are explicit.
- filenames do not serve as hidden predictor labels;
- patches, sides, days, and augmented records retain their parent image/fruit;
- timestamps are stored in UTC with local context retained separately;
- units appear in the schema and metadata, not only in a notebook;
- raw inputs and locked test cohorts are read-only.

## G.5 Version-control and release rules

- Source code, schemas, small tables, documentation, calibration metadata, and
  manifests belong in version control.
- Large raw datasets and model artifacts use an institutional object store,
  data registry, or approved large-file mechanism; checksums remain in the
  repository.
- Dataset licensing is evaluated independently from article and code licensing.
- Secrets, personal data, supplier credentials, and unpublished participant
  information are excluded.
- A release includes environment lock, data/source manifest, split manifest,
  model card, known limitations, and exact regeneration command.

## G.6 Recommended branches/tags

- protected `main` for validated releases;
- short-lived feature branches for analysis, firmware, PCB, and protocol work;
- signed or annotated tags for `protocol-v1`, `data-lock-v1`,
  `model-freeze-v1`, and manuscript releases;
- a decision record for every post-lock change.

