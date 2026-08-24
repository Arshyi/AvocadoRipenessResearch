# Appendix A — Existing Papers Supplied for Review

**Evidence-audit date:** 30 July 2026

## Evidence labels

- **[V-P] Primary-source verified:** verified against a publisher, institutional, author-hosted, or repository primary source.
- **[V-L] Local-full-text verified:** verified directly in the supplied local PDF.
- **[A] Audit assessment:** an interpretation or methodological assessment based on the reported design; it is not a claim made verbatim by the authors.
- **[U] Unresolved:** the available source did not establish the point, or an external permission/metadata check remains necessary.

Reported model performance is reproduced as a claim of the cited paper, not independently replicated performance.

---

## A.1 RipeTrack: Assessing Fruit Ripeness and Remaining Lifetime Using Smartphones

### Full citation

Waseem, M. S., Sharma, N., & Hefeeda, M. (2026). RipeTrack: Assessing Fruit Ripeness and Remaining Lifetime Using Smartphones. *IEEE Transactions on Mobile Computing, 25*(1), 830–845. [https://doi.org/10.1109/TMC.2025.3599917](https://doi.org/10.1109/TMC.2025.3599917). **[V-P, V-L]**

Primary access:

- [Institutional publication record](https://elmi.hbku.edu.qa/en/publications/ripetrack-assessing-fruit-ripeness-and-remaining-lifetime-using-s/)
- [Author-hosted manuscript](https://www.cs.sfu.ca/~mhefeeda/Papers/tmc25_RipeTrack.pdf)
- [RipeTrack code and data-link repository](https://github.com/ShahzaibWaseem/RipeTrack)

The article appears in the 2026 volume; the `2025` embedded in the DOI is not the publication year. **[V-P]**

### Research objective

RipeTrack addresses two related tasks:

1. classification of fruit as unripe, ripe, or expired; and
2. estimation of the fruit’s remaining lifetime.

The proposed consumer-facing system uses smartphone sensing and machine-learning models to infer optical changes associated with ripening without cutting the fruit. Its intended value is scalable, non-invasive assessment for retailers and consumers rather than laboratory chemical analysis. **[V-P, V-L]**

### Experimental and technical approach

The authors first collected hyperspectral images and ethylene measurements across the observed postharvest lives of several fruit types. The laboratory hyperspectral system used a Specim IQ camera covering approximately 400–1000 nm with 204 bands and approximately 3 nm spectral sampling. Ethylene was measured using an FD-90A-C2H4 detector specified in the paper as covering 0–100 ppm with 1 ppm accuracy. Mobile experiments used Google Pixel 4XL and OnePlus 8 Pro phones. **[V-L]**

The full laboratory dataset reported in Table 1 of the paper is:

| Fruit/cultivar | Independent fruits | Hyperspectral images | Ethylene readings | Observed lifetime |
|---|---:|---:|---:|---:|
| Organic avocado | 10 | 460 | 230 | 11 days |
| Hass avocado | 3 | 234 | 117 | 19 days |
| Bartlett pear | 11 | 382 | 209 | 12 days |
| Bosc pear | 3 | 276 | 138 | 40 days |
| Banana | 12 | 279 | 168 | 7 days |
| Nectarine | 3 | 138 | 138 | 16 days |
| Mango | 6 | 144 | 144 | 16 days |
| **Total** | **48** | **1,913** | **1,144** | — |

**Evidence:** counts transcribed from the supplied paper. **[V-L]**

The mobile dataset contains 3,865 paired RGB and near-infrared captures: 2,695 from the Pixel 4XL and 1,170 from the OnePlus 8 Pro. The paper reconstructs a richer spectral representation from phone measurements and then uses learned models for ripeness and remaining-life prediction. The authors also examine transfer learning to additional fruits and measurements under varied illumination. **[V-L]**

### Main reported findings

- Avocado ripeness classification accuracy: **95%**.
- Pear ripeness classification accuracy: **98%**.
- Avocado remaining-lifetime prediction accuracy: **93%**.
- Pear remaining-lifetime prediction accuracy: **97%**.
- The paper reports that the mobile ripeness test set used fruits not observed during training.
- The paper reports extension to bananas, mangoes, and nectarines through transfer learning and tests in home and grocery-store illumination.

The 93% and 97% figures are accuracies for an 11-class remaining-life-percentage
target (0%, 10%, ..., 100%). The target is derived from days until the start of
RipeTrack's ethylene-defined *Expired* stage, with approximately one- to
two-day granularity depending on fruit lifetime. These percentages are not
continuous regression accuracy, MAE in days, or validation against a sensory
usable-life endpoint. **[V-L, A]**

These are the authors’ reported results and require independent replication before they are treated as expected prototype performance. **[V-P, V-L]**

### Contribution to the proposed research

RipeTrack supplies a strong systems precedent for:

- multimodal visible and near-infrared sensing;
- moving from laboratory hyperspectral evidence toward consumer hardware;
- reporting an intuitive ripeness state and remaining-life output;
- testing multiple phones and lighting conditions; and
- using transfer learning for additional fruit types.

The proposed avocado study extends this direction by adding explicit biological ground truth—firmness, mass loss, moisture/dry matter, soluble solids, starch, oil, pigment, and potentially gas measurements—and by fitting interpretable longitudinal state and rate models rather than treating each image as an independent black-box sample. **[A]**

### Limitations and cautions

1. **The biological sample size is much smaller than the image count.** The avocado results derive from 13 independent fruits in total, including only three Hass fruits. Repeated images increase temporal resolution but do not create new independent biological replicates. **[V-L, A]**
2. **Cultivar and supply-chain generalization remain uncertain.** Organic and Hass avocado groups are small and do not establish robustness across orchards, harvest maturity, season, cold-chain history, or country of origin. **[A]**
3. **The reconstruction split needs a grouping audit.** A 70/15/15 split is reported for hyperspectral reconstruction, but the manuscript does not clearly establish that all repeated views and days from a fruit were confined to one partition. Any re-analysis must split by fruit identity. **[V-L, A]**
4. **Accuracy is not a complete shelf-life metric.** Future evaluation should report class balance, confusion matrices, ordinal error, MAE/RMSE in days, calibration intervals, and performance on wholly independent harvest batches. **[A]**
5. **Optical features are not uniquely attributable to water.** Visible/NIR changes may combine water absorption, lipid- and carbohydrate-related absorption, pigment changes, geometry, and scattering from softening tissue. Wavelength interpretations require destructive calibration. **[A]**
6. **Dataset reuse rights are unresolved.** The public GitHub repository links datasets hosted on Google Drive, but no explicit dataset licence was located during this audit. Public downloadability alone does not grant reuse or redistribution rights. Written clarification is required before incorporating the data into a redistributed project. **[U]**

### Bottom-line interpretation

RipeTrack demonstrates the feasibility of a phone-oriented optical pipeline and provides a valuable reference architecture. It does **not** by itself establish a universally valid avocado ripeness model, nor does it identify a single causal chemical mechanism behind the measured spectra. The strongest extension is therefore a fruit-grouped, batch-independent, multimodal longitudinal experiment with destructive chemical and mechanical calibration. **[A]**

---

## A.2 Non-destructive Methods for Fruit Quality Evaluation

### Full citation

Bratu, A.-M., Popa, C., Bojan, M., Logofatu, P. C., & Petrus, M. (2021). Non-destructive methods for fruit quality evaluation. *Scientific Reports, 11*, 7782. [https://doi.org/10.1038/s41598-021-87530-2](https://doi.org/10.1038/s41598-021-87530-2). **[V-P, V-L]**

Primary access:

- [Scientific Reports article](https://www.nature.com/articles/s41598-021-87530-2)
- [Article PDF](https://www.nature.com/articles/s41598-021-87530-2.pdf)

The article is open access under CC BY 4.0. This licence covers the article and included material unless a credit line says otherwise; it does not establish the existence or reuse licence of a separate raw dataset. **[V-P]**

### Research objective

This study evaluates the deterioration of stored apples by combining:

1. laser photoacoustic spectroscopy (LPAS) for ethylene and ethanol in the fruit’s emitted gases; and
2. multispectral imaging using visible spectral filters for external reflectance and defect-related changes.

The work concerns apples, not avocados, and its quantitative gas trajectories should not be transferred directly to avocado. **[V-P, V-L, A]**

### Experimental approach

Twenty apples—five Golden Delicious, five Gala, five Granny Smith, and five Starkrimson—were monitored at room temperature over 35 days. Measurements were taken on days 1, 7, 14, 21, 28, and 35. For gas analysis, each fruit was placed in a 150 cm³ glass cuvette, flushed with synthetic air, and connected to a CO₂-laser photoacoustic system. The study selected a laser line for ethylene and another for ethanol. External measurements used an imaging system with eight visible-region spectral filters and tracked histograms from selected surface regions. **[V-P, V-L]**

### Main supported findings

- Ethylene emission decreased over storage for all four cultivars, with a pronounced decline around the second and third weeks.
- Ethanol was initially low and increased during storage, becoming especially elevated once fruit showed advanced deterioration and fermentation.
- Cultivar-specific trajectories were evident: Golden and Gala began with higher ethylene, while Starkrimson showed comparatively high ethanol.
- Visible defects, wrinkling, brown patches, and mass loss became apparent over time.

These findings support gas sensing as a potentially informative longitudinal modality, but the study’s five fruits per cultivar provide limited statistical power and do not establish an avocado-specific gas law. **[V-P, V-L, A]**

### Required correction to an overstrong reading of the imaging results

The multispectral imaging results were **not** a strong demonstration that image changes tracked gas deterioration. The authors explicitly report that practical impediments prevented uniform experimental conditions and that they were mostly unsuccessful in finding clear temporal patterns. In the discussion, they state that the histogram and global-plot changes generally could not be separated from statistical or systematic error. A slight overall shift toward darker tones was found for the more extensively observed Granny Smith case. **[V-P, V-L]**

Accordingly, the defensible interpretation is:

> The paper demonstrates a precise gas-measurement approach and an exploratory attempt to combine it with multispectral imaging; the imaging evidence was mostly inconclusive rather than a validated external deterioration model.

**[A]**

### Contribution to the proposed research

The paper remains relevant as a methodological precedent for:

- pairing an external optical signal with an internal/volatile signal;
- measuring ethylene and ethanol longitudinally;
- accounting for cultivar-dependent gas behavior; and
- recognizing the calibration and repeatability demands of spectral imaging.

For the avocado proposal, gas sensing should be treated as an experimentally calibrated complementary modality. Low-cost VOC sensors are not automatically selective for ethylene or ethanol, and any chamber measurement must control fruit mass, chamber volume, accumulation time, flow, temperature, humidity, background gas, sensor cross-sensitivity, and sensor drift. **[A]**

### Limitations and cautions

1. **Species mismatch:** apple physiology and peel gas diffusion cannot supply avocado-specific parameters without new experiments. **[A]**
2. **Small biological sample:** five apples per cultivar with repeated measurements; repeated time points are not independent replicates. **[V-P, A]**
3. **Limited imaging evidence:** most spectral-histogram changes were not distinguishable from experimental variability. **[V-P, V-L]**
4. **Descriptive analysis:** the paper does not provide a validated remaining-life model, independent test cohort, or modern grouped machine-learning evaluation. **[A]**
5. **No public raw-data repository located:** the article is open access, but this audit found no linked machine-readable release of the gas time series and multispectral images. **[U]**

### Bottom-line interpretation

The paper supports the concept of multimodal gas-plus-optical monitoring but does not validate a deployable imaging predictor. Its most useful lesson for the proposed avocado work is experimental: controlled chambers, selective/calibrated gas measurements, biological replication, and synchronized optical measurements are necessary before coupled kinetic or machine-learning models can be trusted. **[A]**

---

## A.3 How the two supplied papers jointly frame the proposal

| Dimension | RipeTrack | Bratu et al. | Proposed avocado extension |
|---|---|---|---|
| Target setting | Smartphone/consumer and retail | Laboratory/storage research | Calibrated prototype progressing toward deployable hardware |
| Fruit scope | Avocado, pear, banana, mango, nectarine | Four apple cultivars | Hass avocado with documented harvest and storage batches |
| Primary modalities | RGB, near-infrared, reconstructed hyperspectral signatures, ethylene | LPAS ethylene/ethanol and exploratory multispectral imaging | RGB/colour, NIR, firmness, fruit mass, environment, selective gases, destructive chemistry |
| Primary outputs | Ripeness class and remaining lifetime | Longitudinal gas and image changes | Ripeness state, firmness, moisture/dry matter, days to edible/overripe thresholds, uncertainty |
| Key strength | Practical sensing architecture | Precise trace-gas methodology | Multimodal biological calibration and interpretable dynamics |
| Key limitation | Very small independent avocado sample, especially Hass | Apple-only, five fruits/cultivar, weak imaging result | Must be addressed through fruit-grouped, batch-independent design |

**Synthesis [A]:** RipeTrack shows how optical sensing can become an accessible prediction system; Bratu et al. shows how internal volatile measurements can be collected alongside imaging. The proposed work should combine the practical orientation of the former with the controlled multimodal measurement discipline of the latter, while avoiding image-level leakage, unsupported chemical attribution, and overstatement of exploratory results.
