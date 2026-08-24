# Appendix C — Public and Potentially Obtainable Datasets

**Dataset-audit date:** 30 July 2026

## Evidence and status labels

- **[V-P] Primary-source verified:** checked against the dataset repository, publisher, or associated paper.
- **[V-L] Local-full-text verified:** checked in a supplied local PDF.
- **[A] Audit assessment:** quality, leakage, or recommended-use assessment derived from the published protocol.
- **[U] Unresolved:** licence, access, grouping key, or raw-data status needs confirmation.

### Access-status vocabulary

- **Open and licensed:** downloadable and accompanied by an explicit reusable dataset licence.
- **Publicly linked; licence unresolved:** files are linked publicly, but no explicit dataset reuse licence was found.
- **Request-only:** data are available only by contacting the authors.
- **Unavailable:** the article states the data are unavailable or no raw release could be found.
- **Domain-adjacent:** public data exist but do not measure the target object or target outcome.

“Publicly visible” and “licensed for reuse” are not synonyms. Article licences and repository/code licences must not be assumed to cover separate raw datasets.

---

## C.1 Dataset decision table

| Dataset | Target and scale | Modalities and labels | Licence and access | Quality assessment | Recommended use | Evidence |
|---|---|---|---|---|---|---|
| [‘Hass’ Avocado Ripening Photographic Dataset](https://data.mendeley.com/datasets/3xd9n945v8/1), DOI [10.17632/3xd9n945v8.1](https://doi.org/10.17632/3xd9n945v8.1) | 478 independent Hass fruits; 14,710 labeled 800×800 JPEGs; two opposite sides photographed daily | RGB photographs; fruit/sample number; storage group; day; side; five-stage ripening index; timestamps supporting days-left derivation | **Open and licensed: CC BY 4.0** | **High for controlled RGB longitudinal baselines.** Strong sample count and explicit fruit IDs; the associated paper states that each fruit/sample was assigned wholly to one model partition. Labels are researcher-assigned visual/tactile stages, not destructive chemistry for every fruit: only eight separate fruits were used for the initial dry-matter assessment. DSLR lightbox imagery creates a domain gap to uncontrolled smartphones. | Acquire first. Split by sample number. Keep all days and sides from one fruit in one fold. Use storage group for domain-shift evaluation; do not randomly split images. | **[V-P, A]** |
| [RipeTrack datasets](https://github.com/ShahzaibWaseem/RipeTrack) | 48 total fruits across seven fruit/cultivar groups; avocado subset is 10 organic + 3 Hass; 1,913 HSI and 1,144 ethylene readings overall; 3,865 mobile RGB-NIR pairs | 400–1000 nm HSI, RGB/NIR phone captures, ethylene, time/ripeness and remaining-life labels | **Publicly linked; licence unresolved.** GitHub links to Google Drive; no explicit dataset licence found | **Scientifically relevant but biologically small for avocado.** Effective avocado n=13, Hass n=3; repeated images must not be treated as independent fruit. Reconstruction split grouping is unclear. | Use only after written licence clarification. If obtained, preserve fruit identity, day, cultivar, phone, illumination, and capture distance. Suitable for transfer-learning and sensor-comparison experiments, not as a definitive external test set. | **[V-P, V-L, A, U]** |
| [DeepHS Fruit v2](https://github.com/cogsys-tuebingen/deephs_fruit) and [file server](https://cogsys.cs.uni-tuebingen.de/webprojects/DeepHS-Fruit-2023-Datasets/) | Fruits include avocado, kiwi, persimmon/kaki, papaya, and mango across four measurement series; avocado archive advertised as 72 GB | HSI from Specim FX10, INNO-SPEC Redeye 1.7, and Corning microHSI 410; destructive flesh firmness, sugar content, and overall ripeness labels | **Publicly linked; licence unresolved.** Direct/torrent downloads exist; no explicit dataset or repository licence found | **Potentially high scientific value, high operational cost.** Multiple cameras and destructive labels enable spectral-domain work. v1 had 1,038 avocado recordings but only 180 destructively labeled avocado recordings. Front/back/repeated records create leakage risk unless grouped by fruit. | Do not download for routine use until licence and storage budget are approved. First inspect the small annotation archive and verify stable fruit IDs, camera IDs, series IDs, sides, and label completeness. Use grouped fruit/series/camera validation. | **[V-P, A, U]** |
| [Estrada et al. avocado/olive/grape leaf dataset](https://figshare.com/articles/dataset/_b_A_multi-spectral_and_hyperspectral_image_dataset_for_evaluating_the_health_status_of_avocado_olive_and_vineyard_b_/26950660), DOI [10.6084/m9.figshare.26950660.v2](https://doi.org/10.6084/m9.figshare.26950660.v2) | 106 avocado leaves, 111 olive leaves, 106 grape leaves; five dehydration stages | Five-band multispectral TIFFs; 350–2500 nm spectra; weight; chlorophyll/SPAD; nitrogen; dry- and fresh-basis fuel moisture | **Domain-adjacent; item licence unresolved.** Article links the repository, but this audit could not verify the separate figshare item licence | **High for leaf water spectroscopy; low for fruit ripeness.** Leaf anatomy and forced oven dehydration differ materially from avocado peel/mesocarp ripening. Paper reports 2,600 avocado TIFFs although 106 leaves × 5 stages × 5 bands implies 2,650, requiring a file-manifest audit. | Use only for wavelength-selection, spectral-index code tests, or water-sensitivity method development. Never use as a fruit-ripeness train/test set. Confirm item licence and missing-file pattern first. | **[V-P, A, U]** |
| Han et al. 2023 Hass/Shepard HSI | 316 Hass and 160 Shepard fruits; one HSI per fruit after cold storage | 462 bands, 388–1005 nm; days to full ripeness; cultivar; firmness threshold used to define ripeness | **Request-only.** Publisher states data are available from the corresponding author on reasonable request | **Strong sample count.** Fruit-level PLSR calibration/test design is useful. The DCNN used randomly split subimages, allowing likely same-fruit leakage between partitions. | Request for a confirmatory HSI benchmark. Prefer the one-record-per-fruit ROI spectra or split all subimages by fruit. Retain cultivar and harvest-date groups. | **[V-P, A]** |
| Davur et al. 2023 Hass longitudinal HSI | 80 independent Hass fruits; 551 daily HSI; paper reports 44,096 subimages | Pika XC2/Resonon HSI, 462 bands, 388.9–1005.3 nm; days until ripeness | **Unavailable due to intellectual-property arrangements** | **Valuable longitudinal design but unsuitable published split.** Patches from each original HSI were allocated across training, validation, and test, causing direct same-image and same-fruit leakage. The reported patch totals and described allocation also require arithmetic reconciliation. | Use as a protocol and leakage caution, not as a performance benchmark. Seek IP permission only if raw fruit/day IDs and a new grouped analysis are possible. | **[V-P, V-L, A]** |
| Lee, Li, and Ma 2025 smartphone dataset | 140 Hass fruits in two 70-fruit batches; 10 views per fruit; 1,400 images; eight-day study | Smartphone RGB; destructive firmness; fresh/rotten internal labels; storage day and batch | **Request-only.** Data-availability statement says available on reasonable request | **Useful multimodal ground truth, but main random image split likely leaks fruit identity.** Cross-batch results are more credible and show substantial direction-dependent domain shift. | Request images with fruit and batch identifiers. Rebuild grouped fruit splits and leave-one-batch-out tests. Use for smartphone-domain validation, not as a direct comparison to image-random headline metrics. | **[V-P, A]** |
| Pinto, Rueda-Chacón, and Arguello 2019 Hass HSI | Seven Hass fruits followed for 10 days; three maturity categories | HSI; PCA; NDVI, RVI, PRI, CIE L\*a\*b\*, and TGI analyses | **Unavailable.** Article is accessible, but no raw dataset download was identified | **Low statistical power.** Useful for feature ideas only; seven fruits cannot support a generalizable model. | Cite for exploratory spectral indices and Colombian context. Do not use its results as an expected-accuracy benchmark. Contact authors only if raw cubes would aid method debugging. | **[V-P, A]** |
| Bratu et al. 2021 apple gas and imaging study | 20 apples, five per cultivar, six weekly time points over 35 days | LPAS ethylene and ethanol; eight-filter visible multispectral imaging; external appearance | **Unavailable.** No public machine-readable raw release identified | **Domain mismatch and small n.** Gas system is precise, but the imaging analysis was mostly inconclusive. Apple gas trajectories are not avocado kinetic parameters. | Use to design gas-chamber controls and synchronized measurements. Do not train an avocado model or infer avocado rate constants from it. | **[V-P, V-L, A, U]** |

---

## C.2 Priority acquisition plan

### Priority 1 — acquire and audit now

**‘Hass’ Avocado Ripening Photographic Dataset (Mendeley Data).**

Reasons:

- explicit CC BY 4.0 dataset licence;
- 478 biological fruits;
- stable sample number suitable for grouped validation;
- longitudinal days and opposite-side views;
- controlled storage and imaging metadata; and
- manageable RGB format compared with tens of gigabytes of HSI.

Minimum intake checks:

1. verify archive hashes and preserve the untouched download;
2. retain the dataset DOI, version, licence text, and retrieval date;
3. reconcile 14,710 image files with the spreadsheet;
4. check for missing/duplicate filenames and sample numbers;
5. quantify samples per storage group, day, stage, and side;
6. confirm no sample number occurs in more than one partition;
7. document whether shelf-life endpoint derivation uses stage 5 while the narrative also describes stage 4 as the end of optimal shelf life; and
8. distinguish controlled DSLR performance from smartphone performance.

### Priority 2 — permission and metadata first

**RipeTrack** and **DeepHS Fruit** should not enter the project’s reusable data corpus until the rights holder supplies or points to explicit licence terms. Before downloading large files:

- request data and code reuse/redistribution terms;
- request a data dictionary and stable fruit identifiers;
- inspect small annotations/manifests first;
- estimate storage and preprocessing costs;
- confirm whether pre-trained weights have separate terms; and
- record any restrictions on commercial use, redistribution, or derived models.

### Priority 3 — author requests

Request the Han et al. and Lee et al. datasets because their independent-fruit counts and ground truth could materially improve external validation. A request should ask for:

- raw files and checksums;
- fruit, batch, cultivar, orchard/harvest, date, side/view, and instrument identifiers;
- exact label derivation and measurement units;
- calibration/white-reference files for HSI;
- permission to analyze, publish derived statistics, train models, and redistribute only what the licence permits; and
- citation and acknowledgement requirements.

### Priority 4 — methods-only sources

Use Davur et al., Pinto et al., and Bratu et al. as design and failure-mode references unless rights and raw data become available. Their current published validation designs or species/sample limitations prevent their headline performance from serving as a reliable target benchmark.

---

## C.3 Dataset quality rubric

Each candidate dataset should be scored against the following criteria before model development:

| Criterion | Acceptable evidence |
|---|---|
| Biological independence | Count of distinct fruits, trees, batches, orchards, seasons, and cultivars—not merely images or patches |
| Grouping keys | Stable fruit/sample ID and identifiers for repeated day, side, patch, instrument, and batch |
| Ground-truth traceability | Measurement protocol, unit, instrument, calibration, operator, and timing relative to imaging |
| Label validity | Clear distinction among firmness, eating ripeness, internal rot, days to threshold, dry matter, moisture, and subjective colour stage |
| Leakage control | All records derived from one fruit confined to one fold; no patch-, side-, or day-level random split across folds |
| External validity | Independent harvest batch, orchard, season, storage condition, phone/camera, or geographic source |
| Licensing | Explicit dataset licence and attribution terms; no inference from “public repository” or article licence |
| Completeness | File manifest reconciles with metadata; missing/corrupt records and exclusions documented |
| Calibration data | White/dark references for spectral instruments; colour references and fixed exposure for RGB where available |
| Reproducibility | Versioned annotations, checksums, documented preprocessing, and reproducible train/test assignment |

---

## C.4 Required split policy for every adopted dataset

Let \(g_i\) denote the biological fruit identifier for observation \(i\). Every image, spectral patch, side, wavelength file, phone capture, and day derived from fruit \(g_i\) must belong to exactly one of training, validation, or test:

\[
\mathcal{G}_{train} \cap \mathcal{G}_{val} =
\mathcal{G}_{train} \cap \mathcal{G}_{test} =
\mathcal{G}_{val} \cap \mathcal{G}_{test} = \varnothing.
\]

Where sufficient metadata exist, the project should add a higher-level external test split by harvest batch, orchard, season, storage treatment, or device. Image-level random splitting is prohibited for longitudinal fruit datasets because it estimates recognition of previously seen fruit and acquisition conditions rather than generalization to a new fruit. **[A]**

---

## C.5 Licensing and availability caveats

1. **Mendeley Hass RGB data:** CC BY 4.0 is verified at the dataset record. Attribution and version/DOI retention are required.
2. **RipeTrack:** public repository and Google Drive links are verified; explicit code/data licence is not. Do not redistribute or publish derived subsets until permission is documented.
3. **DeepHS Fruit:** public direct and torrent files are verified; explicit code/data licence is not. Its 72 GB avocado archive should not be acquired merely because it is reachable.
4. **Estrada figshare data:** the associated Scientific Reports article is CC BY-NC-ND 4.0, but the dataset is a separate repository object. The separate item licence must be checked; do not substitute the article licence.
5. **Request-only studies:** “available on reasonable request” is an access route, not a licence. Written terms should accompany the transfer.
6. **Unavailable/IP-restricted studies:** do not attempt to reconstruct or redistribute raw data from figures or supplementary screenshots. Use only reported aggregate findings within normal citation limits.
7. **Article images and equipment photographs:** article open-access terms may differ from dataset terms and third-party photo credits. Each proposed reused image needs its own rights check.

---

## C.6 Dataset-to-research-task mapping

| Research task | Best current source | Why | Required safeguard |
|---|---|---|---|
| RGB ripeness-stage baseline | Mendeley Hass photographic dataset | Largest verified, licensed longitudinal fruit dataset in this audit | Fruit-grouped split; report controlled-lightbox domain |
| RGB remaining-life baseline | Mendeley Hass photographic dataset | Day and endpoint metadata allow days-left derivation | Freeze endpoint definition before modeling; avoid post-outcome leakage |
| Smartphone external validation | Lee et al., if obtained | Smartphone captures plus firmness/internal quality | Request fruit IDs; leave-one-batch-out evaluation |
| VIS/NIR days-to-ripen regression | Han et al., if obtained | 476 independent fruits and one HSI per fruit | Whole-fruit split; separate cultivars and harvest dates |
| HSI representation learning | DeepHS Fruit, if licensed | Multiple cameras, fruit types, and destructive labels | Fruit/series/camera grouped folds; annotation audit |
| RGB–NIR phone reconstruction | RipeTrack, if licensed | Paired mobile data and reconstruction pipeline | Confirm fruit grouping and device/illumination metadata |
| Water-sensitive wavelength prototyping | Estrada leaf dataset, if licensed | Dense 350–2500 nm spectra with measured dehydration | Treat as leaf-only auxiliary evidence; validate on fruit tissue |
| Gas-chamber protocol | Bratu et al. paper | Detailed LPAS chamber and temporal gas workflow | New avocado calibration; selective sensors and environmental controls |
