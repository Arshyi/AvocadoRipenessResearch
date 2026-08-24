# Appendix L — Risk, Evidence, Claims Boundaries, and Go/No-Go Gates

**Decision status:** pre-experimental planning  
**Evidence-audit date:** 30 July 2026  
**Scope:** Hass avocado metrology, pilot experimentation, confirmatory study, modeling, and release decisions

## L.1 Purpose

This appendix prevents a technically plausible prototype from becoming an unsupported scientific or deployment claim. It:

1. defines the evidence labels used throughout the project;
2. records what the present work does and does not establish;
3. links each material risk to the evidence that motivates it; and
4. defines staged go, conditional-go, and no-go decisions.

The gates are intentionally asymmetric. A failed optional sensor can be removed or relabeled without cancelling a well-designed experiment, but failed biological independence, endpoint validity, safety, data rights, or core metrology blocks the affected claim or phase.

---

## L.2 Evidence and decision labels

### Evidence labels

| Label | Meaning | Permitted use |
|---|---|---|
| **DATA-DEMONSTRATED** | Directly reproduced from files inspected and analyzed in this workspace | May be reported with its dataset, validation unit, uncertainty, and scope |
| **LITERATURE-SUPPORTED** | Reported by a cited primary source but not independently reproduced here | May motivate a method or hypothesis; must retain the source’s population and limitations |
| **INFERRED** | Reasoned interpretation of available evidence | May guide design; must not be presented as an observed result |
| **PROPOSED** | Future method, apparatus, equation, threshold, or analysis | Requires preregistration, calibration, and experimental validation |
| **NOT IDENTIFIABLE** | Current data cannot estimate the quantity, mechanism, or causal effect | The corresponding claim is prohibited until new evidence is collected |

These definitions match the [integrated proposal](../proposal/avocado-research-proposal.md) and the evidence corrections in [Appendix A](appendix-a-existing-papers.md).

### Decision labels

| Label | Meaning |
|---|---|
| **GO** | All mandatory evidence for the phase exists and has passed its locked acceptance criteria |
| **CONDITIONAL GO** | Work may continue only with a narrower endpoint, downgraded sensor label, exploratory analysis, or documented limitation |
| **NO-GO** | Continuing would make the result unsafe, legally unsupported, scientifically uninterpretable, or non-reproducible |
| **HOLD** | A decision awaits external permission, a resource owner, a safety review, or a prespecified measurement |

Numerical acceptance thresholds must be selected and signed before the data used to judge them are collected. They must not be chosen after viewing biological or locked-test outcomes.

---

## L.3 Evidence anchors

| Evidence anchor | What it establishes | Boundary |
|---|---|---|
| [Dataset discovery and suitability audit](../docs/dataset-audit.md) | One located longitudinal avocado dataset is immediately reusable; RipeTrack and DeepHS are licence-blocked; image/patch count is not biological sample size | Does not establish performance outside the inspected datasets |
| [Data-quality report](../reports/data-quality-report.md) | 14,710 JPEGs match 478 fruits; 12 workbook rows have no corresponding image; labels are external visual/tactile stages | Does not provide firmness, moisture, oil, starch, pigment, or internal-quality truth |
| [Fruit-grouped ML results](../reports/ml-results.md) | Best five-stage balanced accuracy is 0.731 internally; held-out T10 balanced accuracy falls to 0.497; days-to-stage-4 MAE is 1.853 days | Internal validation in one study; the time target is retrospective and not direct edible shelf life |
| [Prototype architecture](../docs/prototype-architecture.md) | Direct sensor observations, prohibited sensor claims, calibration controls, and eight readiness checks | Hardware selection does not itself validate biological meaning |
| [Appendix A — supplied papers](appendix-a-existing-papers.md) | RipeTrack feasibility and limitations; Bratu et al. gas method and mostly inconclusive imaging result | Literature findings are not replicated avocado results |
| [Appendix C — dataset register](appendix-c-public-datasets.md) | Access, licence, leakage, and recommended-use status for candidate datasets | Public download links without explicit rights remain blocked |
| [Appendix D — hardware catalogue](appendix-d-hardware-catalogue.md) | Proposed parts, specifications, alternatives, and sourcing evidence | Prices, availability, and vendor claims require re-verification before purchase |
| [Mendeley Hass dataset](https://doi.org/10.17632/3xd9n945v8.1) | CC BY 4.0 source of the reproduced RGB analysis | Controlled DSLR/lightbox domain, not uncontrolled smartphone deployment |
| [RipeTrack](https://doi.org/10.1109/TMC.2025.3599917) | Published mobile RGB/NIR and remaining-life precedent | Only 13 independent avocado fruits, including three Hass; data licence unresolved |
| [Bratu et al.](https://doi.org/10.1038/s41598-021-87530-2) | LPAS ethylene/ethanol workflow in apples | Apple gas trajectories are not avocado rate constants; imaging evidence was weak |

---

## L.4 Current claims and prohibited overclaims

| Topic | Defensible current statement | Evidence label | Statement that must not be made |
|---|---|---|---|
| Public RGB corpus | The audited CC BY 4.0 corpus contains 14,710 available images from 478 Hass fruits under three storage groups | **DATA-DEMONSTRATED** — [quality report](../reports/data-quality-report.md) | “There are 14,710 independent avocado samples” |
| RGB stage prediction | Compact colour features carry information about the dataset’s five-stage external ripening index under fruit-grouped validation | **DATA-DEMONSTRATED** — [ML results](../reports/ml-results.md) | “A camera can determine internal eating readiness” |
| Storage transfer | The selected colour model degraded materially when a storage group was held out; T10 balanced accuracy was 0.497 | **DATA-DEMONSTRATED** — [ML results](../reports/ml-results.md) | “The RGB model generalizes across storage temperatures, seasons, or cameras” |
| Remaining life | A retrospective days-to-first-stage-4 target was modeled with 1.853-day MAE in internal fruit-grouped validation | **DATA-DEMONSTRATED** — [ML results](../reports/ml-results.md) | “The system predicts remaining edible shelf life to 1.853 days” |
| Peel colour biology | Chlorophyll loss and later anthocyanin accumulation contribute to Hass peel colour, and colour can desynchronize from softening | **LITERATURE-SUPPORTED** — [bibliography](appendix-b-bibliography.md) | “Darkness alone is a universal ripeness meter” |
| NIR feasibility | NIR can predict calibrated avocado properties such as dry matter under study-specific instruments and populations | **LITERATURE-SUPPORTED** — [bibliography](appendix-b-bibliography.md) | “A 970 nm LED directly measures internal moisture percentage” |
| 970 nm channel | A repeatable 970 nm response may be retained as a water-sensitive feature after destructive calibration and ablation | **PROPOSED** — [architecture](../docs/prototype-architecture.md) | “The 970 nm signal is specific to water rather than scattering or other constituents” |
| Fruit mass | A calibrated load cell can estimate net mass change after tare, creep, and contact-force correction | **PROPOSED** — [architecture](../docs/prototype-architecture.md) | “All measured mass loss is water loss” |
| Ambient RH | A chamber sensor directly measures surrounding air temperature and RH | **PROPOSED** — [architecture](../docs/prototype-architecture.md) | “An RH sensor measures internal fruit water” |
| CO₂ | An in-range, leak-corrected NDIR accumulation slope can provide an apparent respiration-related feature | **PROPOSED** — [architecture](../docs/prototype-architecture.md) | “A single chamber CO₂ value is total respiration without volume, time, leakage, and fruit-mass correction” |
| MOX gas sensor | A conditioned MOX response can be analyzed as a broad, humidity-sensitive VOC/odour trajectory | **PROPOSED** — [architecture](../docs/prototype-architecture.md) | “The BME688 measures ethanol or ethylene concentration” |
| Low-cost ethylene bridge | An electrochemical channel may be exploratory if compared with a reference method across relevant interferents | **PROPOSED** — [architecture](../docs/prototype-architecture.md) | “The low-cost sensor is selective quantitative ethylene in fruit headspace” |
| Governing equations | First-order, Arrhenius, logistic, Gompertz, state-space, and transport equations are candidate model families | **PROPOSED** — [proposal](../proposal/avocado-research-proposal.md) | “The equations are established biological laws for this apparatus and cultivar” |
| Rate identification | Current public RGB data cannot identify water, pigment, respiration, oil, starch, or softening rate parameters | **NOT IDENTIFIABLE** — [dataset audit](../docs/dataset-audit.md) | Any numerical mechanistic rate inferred from RGB labels alone |
| Dataset rights | The Mendeley Hass dataset has a verified CC BY 4.0 licence | **DATA-DEMONSTRATED** — [dataset record](https://doi.org/10.17632/3xd9n945v8.1) | “RipeTrack and DeepHS are reusable because their files are publicly linked” |
| Prototype status | The architecture and procurement catalogue define a buildable research prototype | **PROPOSED** | “The prototype is a validated consumer, clinical, food-safety, or commercial instrument” |

---

## L.5 Risk scoring

Likelihood and impact use **L** (low), **M** (medium), or **H** (high). A risk is **critical** when it can invalidate the main endpoint, create a safety or rights breach, or make the experimental unit unknowable. Ratings are planning judgments, not observed frequencies.

### Scientific and biological risks

| ID | Risk | L | I | Evidence or warning signal | Control and decision rule |
|---|---|:---:|:---:|---|---|
| SB-01 | “Ready,” “ripe,” and “expired” remain ambiguously defined | H | H | Dataset labels are external stages, not universal eating quality: [quality report](../reports/data-quality-report.md) | Stakeholder panel signs instrumental firmness, internal-condition, event, censoring, and error thresholds before confirmatory collection; otherwise **NO-GO** for remaining-useful-life claims |
| SB-02 | Peel pigmentation and internal softening desynchronize | H | H | Storage holdout failure and pigment literature: [ML results](../reports/ml-results.md), [bibliography](appendix-b-bibliography.md) | Retain colour only as a complementary channel; require firmness/internal reference; colour-only consumer readiness claim is **NO-GO** |
| SB-03 | Harvest batch, season, supplier, temperature, or device shift causes failure | H | H | Held-out T10 balanced accuracy 0.497: [ML results](../reports/ml-results.md) | Lock independent batches and report group-specific calibration; no independent cohort means **CONDITIONAL GO** for feasibility only |
| SB-04 | Too few independent fruits, batches, or chambers produce unstable estimates | H | H | Public studies often have many images but few fruit: [dataset audit](../docs/dataset-audit.md) | Prioritize independent fruit and batches over extra views; choose confirmatory n by blinded pilot simulation |
| SB-05 | One chamber per condition confounds chamber with temperature/RH | M | H | Experimental hierarchy: [proposal](../proposal/avocado-research-proposal.md) | Replicate chambers/cycles; otherwise label environmental effects exploratory and prohibit causal condition claims |
| SB-06 | Matched sacrifice cohorts do not perfectly reveal a sentinel fruit’s hidden state | M | H | Design limitation: [proposal](../proposal/avocado-research-proposal.md) | Randomized matched cohorts, destructive windows, hierarchical uncertainty; explicitly retain approximation boundary |
| SB-07 | Destructive assays are operator-, site-, or protocol-dependent | M | H | Required protocol controls: [proposal](../proposal/avocado-research-proposal.md) | Freeze probe/site/speed/depth and chemical SOPs; duplicates and blinded QC; failed repeatability blocks that ground-truth claim |
| SB-08 | Fruit attrition, rot, damage, or non-ripening biases time-to-event analysis | M | M | Censored source endpoints: [quality report](../reports/data-quality-report.md) | Intention-to-observe population, reason codes, interval censoring, competing-defect reporting, missingness sensitivity |

### Metrology and hardware risks

| ID | Risk | L | I | Evidence or warning signal | Control and decision rule |
|---|---|:---:|:---:|---|---|
| MH-01 | NIR response confounds water, lipid/carbohydrate absorption, skin, geometry, and scattering | H | H | Sensor claims matrix and NIR literature: [architecture](../docs/prototype-architecture.md), [bibliography](appendix-b-bibliography.md) | Broad-spectrum reference subset, dark/white calibration, fixed geometry, destructive calibration and ablation; otherwise use only “optical feature” wording |
| MH-02 | Low-cost gas sensors respond to interferents, temperature, RH, or drift | H | H | Cross-sensitivity boundary: [architecture](../docs/prototype-architecture.md) | Challenge gases and reference F-900/GC comparison; failure downgrades channel to nonspecific VOC trend or removes it |
| MH-03 | CO₂ saturation, leaks, or variable chamber volume biases the accumulation slope | M | H | Headspace controls: [architecture](../docs/prototype-architecture.md) | Empty/inert blanks, leak test, volume correction, range flags, shorter accumulation; out-of-range records are invalid |
| MH-04 | Enclosure, tubing, adhesives, or printed parts outgas or adsorb volatiles | H | H | Mechanical limitations: [architecture](../docs/prototype-architecture.md) | Blank/recovery testing; inert wetted path for analytical work; persistent carry-over is **NO-GO** for compound claims |
| MH-05 | LEDs, camera, fan, or condensation perturb fruit and sensor readings | M | M | Phase-separation requirement: [architecture](../docs/prototype-architecture.md) | Separate optical/headspace phases, fixed fan duty, thermal logging, recovery; excessive perturbation triggers redesign |
| MH-06 | Scale creep, fan force, cradle contact, or repositioning creates false mass loss | M | M | Calibration requirements: [architecture](../docs/prototype-architecture.md) | Fan/pump off, isolated cradle, check masses, 24-hour creep and reposition tests |
| MH-07 | Device-to-device or session calibration transfer fails | H | H | Controlled JPEGs lack absolute radiometric calibration: [quality report](../reports/data-quality-report.md) | Device IDs, calibration records, transfer study, locked external device; no transfer evidence means device-specific claim only |
| MH-08 | Sensor clocks or record keys are misaligned | M | H | File contract: [architecture](../docs/prototype-architecture.md) | One time standard, synchronization check, immutable session manifest; schema failure blocks biological collection |
| MH-09 | Procurement substitution changes spectral, gas, or metrological behavior | M | M | [Hardware catalogue](appendix-d-hardware-catalogue.md) | Re-quote and engineering review; no substitute is “equivalent” until range, accuracy, optical geometry, and interface are revalidated |

### Data, modeling, and reproducibility risks

| ID | Risk | L | I | Evidence or warning signal | Control and decision rule |
|---|---|:---:|:---:|---|---|
| DM-01 | Same fruit, source image, day, side, or patch appears across partitions | H | H | Published leakage examples: [dataset audit](../docs/dataset-audit.md) | Immutable fruit IDs and automated zero-overlap audit; any overlap is **NO-GO** for reported test performance |
| DM-02 | Retrospective endpoint construction leaks future information or changes the estimand | M | H | Days-to-stage-4 boundary: [ML results](../reports/ml-results.md) | Define event and observation window prospectively; use survival/censoring methods; prohibit edible-life wording for retrospective external-stage targets |
| DM-03 | Long-followed fruit dominate image-weighted metrics | H | M | T10 contributes about 60% of images but 40% of fruit: [quality report](../reports/data-quality-report.md) | Fruit-cluster uncertainty, fruit-level summaries, storage-specific metrics, and weighting sensitivity |
| DM-04 | Missing images, sensor failures, or assay failures are silently dropped | M | M | Twelve source records lack images: [quality report](../reports/data-quality-report.md) | Immutable missingness flags, reason codes, population flow, sensitivity analyses; never synthesize replacements |
| DM-05 | Hyperparameter tuning or feature selection sees the external cohort | M | H | Validation hierarchy: [dataset audit](../docs/dataset-audit.md) | Nested/grouped tuning inside training fruits; external batch remains untouched until model freeze |
| DM-06 | Flexible ODE/PINN/SINDy models return plausible but non-identifiable mechanisms | H | H | Identifiability boundary: [proposal](../proposal/avocado-research-proposal.md) | Start with descriptive/mixed/state-space baselines; structural/practical identifiability, priors, perturbation validation; otherwise report prediction only |
| DM-07 | Multiple sensor/biomarker screens create selective reporting | M | M | Statistical plan: [proposal](../proposal/avocado-research-proposal.md) | Small primary family, hierarchical testing or FDR, effect sizes and intervals, publish null ablations |
| DM-08 | Reproducibility fails because raw records or calibration lineage are overwritten | M | H | Data flow contract: [architecture](../docs/prototype-architecture.md) | Immutable raw layer, checksums, calibration and code versions, machine-readable manifests; provenance failure blocks release |

### Rights, safety, operational, and communication risks

| ID | Risk | L | I | Evidence or warning signal | Control and decision rule |
|---|---|:---:|:---:|---|---|
| RS-01 | Publicly linked data are treated as licensed | H | H | RipeTrack and DeepHS licence blocks: [dataset audit](../docs/dataset-audit.md), [Appendix C](appendix-c-public-datasets.md) | Acquire/use/redistribute only under explicit written terms; unresolved rights are **NO-GO** for that dataset |
| RS-02 | Article, dataset, code, weights, and product images are assumed to share one licence | H | H | Rights distinctions: [Appendix C](appendix-c-public-datasets.md) | Maintain a separate source/licence ledger for every asset and derivative |
| RS-03 | Solvents, compressed gases, heated ovens, or electrical hardware are used without institutional controls | M | H | Experimental methods and BOM: [proposal](../proposal/avocado-research-proposal.md), [hardware catalogue](appendix-d-hardware-catalogue.md) | Institutional SOP, training, fume hood/ventilation, waste handling, electrical review; absent approval is **NO-GO** |
| RS-04 | Budget or availability changes silently downgrade reference measurements | M | H | Staged procurement: [proposal](../proposal/avocado-research-proposal.md) | Re-quote before purchase; protect ground truth and calibration first; narrow claims rather than substituting unvalidated parts |
| RS-05 | Measurement burden changes the ripening process or causes unacceptable missingness | M | M | Repeated transfer warning: [proposal](../proposal/avocado-research-proposal.md) | Metrology-stage timing study, shortened sessions, randomized order; excessive perturbation triggers redesign |
| RS-06 | Results are communicated as deployment, food-safety, or commercial validation | M | H | Explicit limitations: [proposal](../proposal/avocado-research-proposal.md) | Claims matrix, model card, uncertainty and abstention, review before external communication |
| RS-07 | Contact details are guessed or an unverified address is used | M | M | No public email address verified for the intended recipient | Deliver through an established channel or verified LinkedIn profile; never infer an email address |

---

## L.6 Go/no-go gates

### Gate 0 — collaborator fit and endpoint ownership

**Evidence required**

- Named scientific, statistical, engineering, data-governance, and laboratory responsibilities.
- Agreed primary use case and intended user.
- Draft operational definitions for ready-to-eat, end of useful life, internal defect, and actionable forecast error.
- Confirmation of access to at least two independent fruit batches for the pilot.
- Resource decision for firmness, moisture/dry matter, and any additional chemistry or reference gas claims.

**GO:** responsibilities, access, and endpoint-development process are accepted.  
**CONDITIONAL GO:** proceed with a narrower optical/environmental feasibility study if chemistry or reference gas facilities are unavailable; remove the affected internal-chemistry claims.  
**NO-GO:** no independent batches, no owner for ground-truth protocols, or no agreement on the primary endpoint.

### Gate 1 — rights, safety, and procurement review

**Evidence required**

- Explicit licence or written permission for every external dataset, codebase, weight file, image, and redistributed asset.
- Current quotations and specification review for selected components.
- Institutional approval/SOPs for solvents, gas standards, ovens, electrical systems, waste, and any food handling.
- Approved materials for the headspace wetted path.

**GO:** rights and safety evidence are recorded in the source ledger and procurement review.  
**HOLD:** permission, quotation, or laboratory approval is pending.  
**NO-GO:** unresolved rights for a proposed dataset, unapproved chemical work, or an unsafe chamber/electrical design.

### Gate 2 — metrology readiness before biological data collection

The prototype passes only when the numerical thresholds have been declared in advance and all of the following are documented:

1. 20 repeated scans of a stable optical reference satisfy the locked repeatability criterion;
2. fruit-removal and repositioning error is quantified for every scan zone;
3. mass calibration residuals, zero stability, and 24-hour creep pass;
4. CO₂ empty-chamber drift, leak rate, range compliance, recovery, and step response pass;
5. fixed camera settings and colour-target patches are reproducible across sessions;
6. clocks align within one logging interval;
7. chamber blank and VOC carry-over/recovery pass; and
8. every raw record validates against the data schema and retains calibration provenance.

Source: [prototype acceptance criteria](../docs/prototype-architecture.md).

**GO:** all mandatory channels pass.  
**CONDITIONAL GO:** remove or relabel an optional failed modality and repeat its affected integration tests. Examples: a failed 970 nm calibration becomes a generic optical feature; a failed low-cost ethylene comparison becomes a nonspecific VOC feature or is removed.  
**NO-GO:** failure of fruit identity, clocks, raw-data provenance, camera/optical repeatability, mass integrity for a mass endpoint, chamber safety, or uncontrollable gas carry-over.

### Gate 3 — pilot feasibility

**Evidence required**

- Metrology/feasibility work using stable controls and approximately 24–30 non-study fruits.
- A biological pilot using at least two independent receipt or harvest batches.
- Estimates of batch/chamber/fruit variance, missingness, endpoint frequency, censoring, assay repeatability, session burden, and candidate effect sizes.
- Evidence that the measurement process does not materially heat, dehydrate, bruise, or delay the fruit beyond the prespecified tolerance.
- Blinded simulation of confirmatory sample size and destructive windows.

**GO:** endpoints occur often enough, ground truth is repeatable, burden and missingness are manageable, and variance estimates support a feasible confirmatory design.  
**CONDITIONAL GO:** narrow conditions, remove a non-performing sensor, simplify assays, or change the primary target before preregistration.  
**NO-GO:** endpoint cannot be measured reproducibly, no independent batch effect can be estimated, or the apparatus materially changes the process it is meant to observe.

### Gate 4 — confirmatory protocol lock

**Evidence required**

- Preregistered questions, hypotheses, primary endpoints, exclusions, censoring, multiplicity, model family, metrics, and actionable error thresholds.
- Sample size selected by pilot-based simulation; the 360-fruit layout in the proposal remains a planning design, not a fixed-power claim.
- Independent chamber replication or an explicit decision to treat condition effects as exploratory.
- Frozen fruit-grouped outer partitions and a locked independent batch/season/device cohort.
- Model and calibration freeze plan; no outcome-driven retuning on the external cohort.

**GO:** protocol, power simulation, external-cohort lock, and analysis code review are approved.  
**CONDITIONAL GO:** proceed as exploratory if chamber or batch replication is insufficient, with causal/generalization claims removed.  
**NO-GO:** endpoint or split can still change after outcomes are viewed, same fruit can cross partitions, or the external cohort is used for tuning.

### Gate 5 — sensor and model adoption

**Evidence required**

- Comparison on identical fruit/batch folds against prior-only, RGB-only, and simple statistical baselines.
- Paired fruit/batch errors, calibration, prediction-interval coverage, subgroup results, and computational burden.
- Predeclared ablations: colour only, NIR only, environment/mass only, gas only, colour+NIR, and all available channels.
- Independent batch/device performance and explicit domain-shift failure analysis.
- For rate/mechanism claims: structural and practical identifiability plus intervention or perturbation validation.

**GO:** the added channel/model provides a meaningful, externally robust improvement with acceptable uncertainty and burden.  
**CONDITIONAL GO:** retain a channel for research/teaching or as a nonspecific predictive feature if it is repeatable but not chemically specific.  
**NO-GO:** improvement exists only under image-level leakage, internal folds, post hoc endpoint changes, or a non-identifiable mechanistic model.

### Gate 6 — publication, data release, and deployment boundary

**Evidence required**

- Reproducibility audit from immutable raw data to figures and reported metrics.
- Rights review for every released file, image, model, and derivative.
- Model card/measurement statement defining intended use, excluded use, subgroup performance, domain limits, uncertainty, abstention, and failure modes.
- Null results and failed modalities retained in the technical record.
- Independent scientific review of claims against this appendix.

**GO:** release research results and permitted artifacts with evidence labels and limitations.  
**CONDITIONAL GO:** publish a feasibility or methods paper without consumer-readiness, chemistry, or deployment claims.  
**NO-GO:** advertise a food-safety, commercial sorting, universal avocado, phone-only, or internal-chemistry capability without independent prospective validation and the necessary regulatory/quality system.

---

## L.7 Current decision snapshot

| Area | Current state | Decision |
|---|---|---|
| Public RGB data | Licensed, acquired, checksummed, reconciled, and analyzed | **GO** for scoped reproducible RGB research |
| RGB deployment | Internal grouped results and storage-shift warning only | **NO-GO** for deployment claims |
| RipeTrack/DeepHS data | Public links; explicit dataset licences not verified | **HOLD / NO-GO** for acquisition or reuse until permission |
| Prototype design | Architecture and BOM prepared; metrology not yet executed | **HOLD** before biological collection |
| Low-cost ethylene | Proposed bridge with known cross-sensitivity | **HOLD** pending reference validation |
| Internal moisture/oil/starch/pigment claims | No matched experimental ground truth yet | **NOT IDENTIFIABLE / NO-GO** |
| Candidate differential models | Mathematically specified as hypotheses | **GO** for simulation and identifiability planning; **NO-GO** as discovered laws |
| Two-batch pilot | Proposed and awaiting collaborators/resources | **HOLD** pending Gate 0 and Gate 1 |

---

## L.8 Decision record template

Every gate decision should be appended to the project ledger with:

```text
decision_id:
date:
gate:
decision: GO | CONDITIONAL GO | NO-GO | HOLD
decision_owner:
reviewers:
evidence_files_or_links:
locked_thresholds:
failed_checks:
scope_or_claims_removed:
corrective_action:
next_review_date:
```

Silence or an undocumented hardware substitution is not a gate approval.

