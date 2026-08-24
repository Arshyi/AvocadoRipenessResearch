# Multimodal Avocado Ripeness Research Program

Phases 1-14 are complete as a research-design and computational-baseline
release. The workspace contains an evidence-audited proposal for non-destructive
Hass avocado ripeness and remaining-useful-life estimation, a licensed public
dataset acquisition, fruit-grouped RGB baselines, candidate kinetic models, a
prototype architecture and procurement catalogue, a statistical plan, and a
send-ready collaborator message.

## Primary deliverables

- [Integrated 92-page proposal (PDF)](output/pdf/avocado-research-proposal.pdf)
- [Editable proposal source](proposal/avocado-research-proposal.md)
- [Dataset inventory and rights decisions](data/dataset_inventory.csv)
- [Data acquisition and quality audit](reports/data-quality-report.md)
- [Exploratory analysis report](reports/exploratory-analysis.md)
- [Machine-learning results](reports/ml-results.md)
- [Prototype architecture](docs/prototype-architecture.md)
- [Audited bill of materials](procurement/bill-of-materials.csv)
- [Equipment catalogue and source ledger](procurement/equipment-catalogue.md)
- [Collaborator outreach draft](communications/collaborator-outreach-draft.md)
- [Reproducibility validation report](reproducibility/validation-report.json)
- [Phase and claim-status ledger](PROGRESS_LEDGER.md)

## Data acquired

The primary modeling dataset is the CC BY 4.0 *Hass Avocado Ripening
Photographic Dataset*, preserved as its source ZIP and extracted under
`data/raw/hass_avocado_mendeley_v1/`. It contains 14,710 reconciled JPEGs from
478 fruits and 14,722 workbook records; the audit documents the 12 records whose
referenced images are absent.

The licensed *Avocado and Strawberry Ripening Stages* archive is preserved
unmodified but excluded from modeling because its internal structure and
lineage require clarification. DeepHS-Fruit annotations and official repository
metadata were acquired, while its approximately 77 GB avocado payload and the
RipeTrack data payload were not downloaded because this audit did not verify an
explicit dataset licence. These holds are deliberate rights decisions, not
acquisition failures.

## Baseline result

With five-fold cross-validation grouped by biological fruit, the best compact
colour/texture classifier achieved balanced accuracy **0.7307** (95% bootstrap
CI **0.7192-0.7428**). The corresponding grouped days-to-stage-4 model achieved
MAE **1.853 days** (95% CI **1.783-1.922**). Storage-condition holdouts were
substantially weaker, so these results support a controlled internal benchmark,
not deployment or universal smartphone claims.

## Evidence policy

Substantive claims are labelled as data-demonstrated, literature-supported,
inferred, proposed, or not identifiable. Candidate ODE/PDE relationships are
hypotheses for calibration and intervention testing; they are not presented as
discovered biological laws. Hardware prices are dated planning estimates, not
supplier quotations.

## Workspace structure

```text
analysis/                 reproducible exploratory analysis
communications/           correspondence drafts
data/
  raw/                    immutable source datasets
  processed/              derived, reproducible data products
docs/                     audits, protocol, architecture, and data dictionary
figures/                  generated analytical and conceptual figures
ml/                       grouped-validation baseline models
models/
  kinetic/                candidate kinetic models and fitting code
  sciml/                  state-space and scientific-ML prototypes
procurement/              bill of materials, catalogue, and sourced images
proposal/                 editable integrated proposal
output/pdf/                final rendered proposal
reproducibility/           pinned environment, checksums, and release validator
reports/                  data, EDA, ML, and governing-model reports
tables/                   machine-readable study and result tables
tools/                    proposal PDF builder
```

Run `reproducibility/run_all.ps1` to regenerate the processed analysis and
validate the release. Raw source archives are immutable inputs and are not
redownloaded by that script.

Rebuild the proposal PDF with:

```bash
pip install reportlab
python tools/build_proposal_pdf.py
```

## What this repository does not contain

Three things are deliberately excluded, and none of them are outputs of this
work:

- **`data/raw/`** — 3.2 GB of third-party source archives. The project's own
  raw-data policy treats these as immutable inputs rather than committed
  artefacts, and every one is redownloadable from the DOI recorded in
  [`data/dataset_inventory.csv`](data/dataset_inventory.csv).
- **Published papers** — copyrighted by their publishers and citable but not
  redistributable. Full references are in
  [`appendices/appendix-b-bibliography.md`](appendices/appendix-b-bibliography.md).
- **`tmp/`** — non-deliverable intermediates, including a vendored Python
  environment.

The derived feature tables under `data/processed/` **are** included. They come
from the *Hass Avocado Ripening Photographic Dataset*, which is CC BY 4.0 and
therefore redistributable with attribution; the two datasets recorded in the
inventory as `NO VERIFIED LICENSE` were never downloaded or used.
