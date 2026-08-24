# Avocado Ripeness Research Program - Progress Ledger

Last updated: 2026-07-30 (Asia/Dubai)

## Evidence status vocabulary

Every project artifact must classify substantive claims using one of these labels:

- **DATA-DEMONSTRATED** - directly supported by inspected observations in an accessible dataset.
- **LITERATURE-SUPPORTED** - reported by a cited primary source but not reproduced here.
- **INFERRED** - a reasoned interpretation not directly demonstrated by the available observations.
- **PROPOSED** - methodology or hardware intended for the future experiment.
- **NOT IDENTIFIABLE** - unavailable data do not support the requested conclusion or parameter.

## Phase status

| Phase | Deliverable | Status | Evidence / blocker |
|---|---|---|---|
| 0 | Evidence-check five local papers | Complete | PDFs extracted and key pages visually checked. |
| 1 | Dataset discovery and inventory | Complete | Nine sources inventoried with access, licence, scale, checksums, and use decisions. The licensed Mendeley Hass source was fully acquired; unlicensed/request-only payloads are held. |
| 2 | Dataset inspection and harmonisation | Complete | 14,722 workbook rows reconciled against 14,710 JPEGs from 478 fruits; 12 absent images and all lineage checks are recorded. |
| 3 | Exploratory data analysis | Complete | Fruit-, stage-, day-, and storage-level summaries and figures were generated from reconciled observations. |
| 4 | Baseline machine learning | Complete | Five-fold fruit-grouped classification and days-to-stage-4 regression completed, with frozen splits, bootstrap intervals, feature importance, ablations, and storage holdouts. |
| 5 | Governing relationships | Complete | Candidate coupled ODE/PDE/state-space models, assumptions, identifiability limits, and an executable kinetic scaffold are documented. No unmeasured rate constant is claimed as identified. |
| 6 | Questions and hypotheses | Complete | Primary and secondary questions, alternative/null hypotheses, estimands, and claim boundaries are specified. |
| 7 | Experimental design | Complete | Matched-cohort longitudinal/sacrifice design, chamber workflow, calibration, randomisation, and validation gates are specified. |
| 8 | Measurements and rationale | Complete | Minimum, optional, destructive, environmental, derived, and latent variables are separated with limitations. |
| 9 | Prototype architecture | Complete | MVP and research-grade sensing architectures, geometry, gas path, calibration, and mechanical concept are documented; physical construction remains future work. |
| 10 | Procurement catalogue | Complete | Forty-four BOM rows, manufacturer part numbers, dated price evidence, alternatives, datasheets, and licensed exact-model photos are recorded. |
| 11 | Statistical analysis plan | Complete | Repeated-measures models, fruit/batch grouping, uncertainty, missingness, multiplicity, locked external validation, and pilot-based power simulation are specified. |
| 12 | Full proposal | Complete | Integrated Markdown source and visually checked 92-page PDF produced. |
| 13 | Collaborator outreach | Complete | Send-ready email/message draft prepared. It has not been transmitted and no unverified private address was invented. |
| 14 | Appendices and reproducibility | Complete | Appendices A-L, pinned software manifest, source checksums, scripts, model artefacts, and automated validation report are present. |

## Confirmed Phase 0 findings

1. RipeTrack uses ethylene-curve-derived labels rather than a complete destructive avocado-quality panel.
2. RipeTrack contains many images but few independent avocado fruits.
3. Bratu et al. found clear cultivar-dependent ethylene/ethanol trends in apples, but their multispectral temporal patterns were mostly inconclusive.
4. Davur et al. used 80 Hass fruits and 551 longitudinal hyperspectral images, but their published train/validation/test construction allocated sub-images from the same source images across partitions. The reported patch-level results therefore do not establish unseen-fruit generalization.
5. Lee, Li, and Ma used 140 avocados from two acquisition batches and reported cross-batch results, but their image data are available only on reasonable request rather than through an open repository.
6. None of the five local papers jointly measures longitudinal RGB/NIR, mass, environment, firmness, gases, moisture, dry matter, oil, carbohydrate chemistry, pigments, and internal condition.

## Current permission boundary

The shared chat and attached continuation were successfully recovered. On
2026-07-30, the user explicitly authorized execution of Phases 1-14 and
download of public datasets into this workspace. Acquisition remains limited
to sources whose public access and licensing can be verified. No inaccessible
or request-only dataset will be represented as inspected, and no model result
will be generated from synthetic replacement data unless it is explicitly
labelled as a pipeline test rather than scientific evidence.

## Release decision

The research-design/computational package is complete. Biological data
collection, physical prototype construction, supplier purchasing, collaborator
contact, and any deployment claim remain future actions requiring the
go/no-go gates in Appendix L. The current public RGB model is approved only as
a controlled benchmark; its storage-domain shift precludes a deployment claim.

## Continuation rule

If work pauses before the full definition of done:

1. finish the current atomic artifact;
2. update this ledger;
3. identify the next unmet dependency;
4. provide the exact next command when a command is appropriate.
