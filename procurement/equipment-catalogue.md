# Prototype Equipment Catalogue

**Project:** Multimodal non-destructive Hass avocado characterisation  
**Verification date:** 2026-07-30  
**Canonical item list:** [`bill-of-materials.csv`](./bill-of-materials.csv)

Prices are observed list prices, authorised-distributor prices, official MSRP, explicit planning allowances, or quote-only placeholders as labelled. They exclude tax, duty, UAE shipping, calibration certificates, and institutional purchasing fees unless the source explicitly includes them. Availability and exchange rates can change; obtain written quotations before commitment.

## 1. Budget summary

| Configuration | Included scope | Budget |
|---|---|---:|
| MVP priced core | Live-priced or current-MSRP rows in `MVP_priced_core` | **US$443.67** |
| MVP planning total | Priced core plus the explicitly labelled fabrication/consumable allowances | **US$723.62** |
| Research-grade with shared core instruments | MVP plus discrete SWIR feasibility, inert plumbing/chamber allowance, optical accessories/standard, PAL-1, FT327, and assay consumables | **US$6,591.51** |
| Research-grade buy-new baseline proxy | Shared-instrument configuration plus the 2023 NIRQuest+1.7 contract proxy, current F-900 price, and 2026 MB120 authorised MAP | **US$43,466.01** |
| Mid-tier Hamamatsu upgrade | C11708MA, not included above | **€650.53 ex VAT** |

Interpretation:

- **US$723.62** is the practical MVP purchase plan, not a guaranteed landed cost.
- **US$6,591.51** assumes the university supplies the actual research spectrometer, ethylene reference analyser, moisture analyser/oven, balance, chemistry facilities, and computer.
- **US$43,466.01 is not a quotation.** It uses a 2023 federal purchase of an NIRQuest+1.7 package as a transparent historical proxy because Ocean Insight currently quotes by configuration. It also omits any quote-only KNF pump and assumes the 900–1650 nm instrument is sufficient.
- A 900–2500 nm system is required if the 1720/2300 nm lipid bands are a primary objective. That configuration must be quoted and may make the buy-new total materially higher.
- Optional rows (`OPT-*`), quote-only rows, tax, freight, calibration gases, and destructive oil-analysis capital equipment are excluded unless expressly named above.

The budget arithmetic is:

```text
MVP priced core                                  $443.67
MVP planning allowances                         $279.95
MVP planning total                              $723.62

Research auxiliary purchases/allowances       $5,867.89
Research grade using shared core instruments  $6,591.51

Historical NIRQuest+1.7 package proxy         $19,979.00
F-900 current authorised-supplier price       $10,495.00
OHAUS MB120 2026 authorised MAP                $6,400.50
Buy-new baseline proxy                        $43,466.01
```

## 2. Required MVP purchases

### 2.1 Control, imaging, and data

#### Espressif ESP32-S3-DevKitC-1-N8R8 — MPN `ESP32-S3-DevKitC-1-N8R8`

- **Source/price:** DigiKey listing surfaced through Component Search Engine, US$15.00.
- **Verified configuration:** 8 MB QSPI flash and 8 MB octal PSRAM; Wi-Fi/BLE; dual-row breakout.
- **Use:** deterministic sensor sequencing, LED drive control, timestamping, and microSD records.
- **Why selected:** substantial I/O and memory headroom while keeping acquisition independent from the image computer.
- **Limitation:** its integrated ADC is not the primary precision optical ADC, and Wi-Fi time is not a substitute for logging explicit device clock/offset metadata.

#### Raspberry Pi Zero 2 W — ordering code `SC1176`

- **Source/price:** official US$15 MSRP; purchase from an approved reseller and verify local stock.
- **Verified configuration:** 1 GHz quad-core Cortex-A53, 512 MB RAM, Wi-Fi/Bluetooth, CSI camera connector.
- **Use:** Camera Module 3 capture and metadata control.
- **Limitation:** availability can drive reseller prices above MSRP. Use a lab-owned Raspberry Pi if fairly priced stock is unavailable.

#### Raspberry Pi Camera Module 3 standard — Adafruit PID `5657`

- **Source/price:** Adafruit, US$29.25.
- **Verified configuration:** 12 MP Sony IMX708, autofocus, standard approximately 75° view.
- **Use:** standardised peel images.
- **Protocol:** mechanically fix the camera; set and then lock focus, exposure, gain, white balance, crop, and processing. Retain exposure metadata.
- **Limitation:** camera RGB is device- and illumination-dependent. It is not spectrophotometry.

#### Calibrite ColorChecker Classic Mini — SKU `CCC-MINI`

- **Source/price:** Calibrite direct, US$74.00.
- **Verified configuration:** 24 patches; 63.5 × 109.0 mm.
- **Use:** place in each controlled-light image or acquire an immediately adjacent calibration frame.
- **Limitation:** it calibrates visible colour. It is not an NIR white reference and is vulnerable to surface wear, dirt, fading, gloss, and illumination non-uniformity.

#### Adafruit microSD breakout — PID `254`

- **Source/price:** Adafruit, US$7.50; card excluded.
- **Use:** local, append-only raw records on the ESP32.
- **Procurement note:** use genuine high-endurance media from an authorised channel. The US$15 card row is an allowance until a local authorised item and capacity are selected.

### 2.2 Environment and gases

#### Sensirion SHT45 breakout with PTFE membrane — chip `SHT45-AD1B-R2`, Adafruit PID `5665`

- **Source/price:** Adafruit, US$13.50 for the protected version.
- **Verified central-range typical accuracy:** ±1.0 %RH and ±0.1 °C under the manufacturer’s stated conditions.
- **Use:** chamber-air temperature and humidity, compensation covariates, and environmental exposure history.
- **Limitation:** does not measure tissue moisture. Condensation, self-heating, placement, and equilibration must be controlled.

#### Sensirion SCD30 NDIR CO₂ breakout — Adafruit PID `4867`

- **Source/price:** Adafruit, US$58.95.
- **Verified manufacturer range/accuracy:** specified 400–10,000 ppm; ±(30 ppm + 3% of reading); 20 s time constant stated by Sensirion.
- **Use:** CO₂ accumulation slope during a fixed sealed interval.
- **Why SCD30 rather than a generic eCO₂ sensor:** it measures CO₂ by NDIR, while many cheap “CO₂” boards infer an equivalent value from a non-specific MOX sensor.
- **Limitation:** the result is still chamber concentration, not respiration rate until free volume, pressure/temperature, leak, blank, and dynamic response are addressed. Never extrapolate above 10,000 ppm.

#### Bosch BME688 breakout — Adafruit PID `5046`

- **Source/price:** Adafruit, US$19.95.
- **Use:** a conditioned gas-resistance trajectory and supporting T/RH/pressure channels.
- **Strength:** inexpensive broad headspace feature that may help a multivariate model.
- **Scientific limit:** a MOX response is a mixture of gas chemistry, humidity, temperature, heater history, baseline, ageing, and flow. It cannot report “ethanol ppm,” “ethylene ppm,” or total VOC concentration without a matrix-specific analytical calibration.

### 2.3 Mass

#### SparkFun TAL220 10 kg straight-bar load cell — `SEN-13329`

- **Source/price:** SparkFun, US$12.95.
- **Use:** fruit mass at each session with a fixed cradle.
- **Why 10 kg:** robust mounting and ample overload margin; resolution is supplied by the mechanical/ADC system rather than nominal full-scale capacity alone.
- **Limitation:** creep, temperature, wiring, off-axis loading, mounting torque, vibration, and cradle contact can dominate. Calibrate the assembled mechanism, not the bare cell.

#### SparkFun HX711 board — `SEN-13879`

- **Source/price:** SparkFun, US$4.95.
- **Verified function:** 24-bit delta-sigma load-cell ADC, 10/80 samples/s, programmable gain.
- **Use:** bridge excitation/readout.
- **Limitation:** “24-bit” is converter word length, not 24-bit effective accuracy. Use stable windows, daily tare, check masses, and drift flags.

### 2.4 MVP optical head

#### Vishay BPW34 PIN photodiode — `BPW34`

- **Source/price:** DigiKey, US$1.37 observed for a single device.
- **Verified band:** approximately 430–1100 nm; 7.5 mm² active area; response peaks near 900 nm.
- **Use:** one baffled detector for sequential 660/740/850/970 nm illumination.
- **Limitation:** it has zero useful coverage of 1200, 1450, and 1700 nm avocado-relevant SWIR bands.

#### Roithner four-LED set

Exact proposed parts:

| Function | MPN | Nominal peak |
|---|---|---:|
| chlorophyll-sensitive | `LED660N-03` | 660 nm |
| red-edge/reference | `LED740-03AU` | 740 nm |
| scattering reference | `LED850-03UP` | 850 nm |
| weak water-sensitive | `LED970D-03` | 970 nm |

- **Budget:** US$50 planning allowance; Roithner’s 2026-06-18 price list verifies the part designations, but a written quote is required because package/bin price mapping was not reliably extractable.
- **Use:** illuminate one controlled peel spot sequentially; acquire dark, fruit, and diffuse-reference counts.
- **Limitation:** individual LEDs have spectral width, temperature shift, ageing, radiant-output variation, and bin variation. Record exact bins and characterise spectrum/output. A ratio from four broad LEDs is a predictive feature, not a reconstructed chemical spectrum.

#### ADS1115 — Adafruit PID `1085`

- **Source/price:** Adafruit, US$14.95.
- **Verified function:** 16-bit ADC, four single-ended/two differential channels, PGA, 8–860 samples/s.
- **Use:** digitise slow TIA channels.
- **Limitation:** it does not supply the pixel clock, correlated acquisition, buffer chain, or optical coupling for a Hamamatsu line-array spectrometer.

#### Analogue-board allowance

The US$40 allowance covers a low-input-bias op amp, gain-select resistors, feedback capacitors, LED current drivers, MOSFETs, decoupling, connectorisation, and a prototype PCB. Select final TIA gain only after measuring the white-reference and darkest-fruit currents. Include saturation and dark-current checks.

### 2.5 Chamber, mixing, and power

#### Integra clear enclosure — `H12106HCF-6P-P10`

- **Source/price:** AutomationDirect authorised catalogue, US$150.
- **Verified envelope:** approximately 12.54 × 10.54 × 6.71 in; clear polycarbonate; original enclosure ratings NEMA 6P/IP68.
- **Use:** mechanically robust MVP shell for one fruit, sensors, and feedthroughs.
- **Limitation:** drilling voids the as-supplied environmental rating; polycarbonate, gasket, adhesives, and coatings can outgas or adsorb volatiles. Perform empty-chamber blank and dose/recovery tests. Use a glass/stainless vessel for quantitative volatile work.

#### Noctua NF-A4x10 5V — `NF-A4x10 5V`

- **Budget:** US$14.95 planning allowance; verify an authorised local reseller.
- **Verified manufacturer specifications:** 40 × 40 × 10 mm; up to 4500 rpm; 8.2 m³/h; 17.9 dBA; 0.22 W.
- **Use:** low-flow headspace mixing.
- **Limitation:** fan heat and airflow change transport. Fix duty cycle and turn it off during mass acquisition.

#### Mean Well `GST60A12-P1J`

- **Source/price:** DigiKey, US$18.60.
- **Verified output:** 12 V, 5 A, 60 W; universal AC input; IEC C14; 5.5/2.1 mm DC plug.
- **Use:** external certified low-voltage supply feeding a fused/switchable prototype.
- **Limitation:** the IEC input cord is separate. Enclose mains only in the commercial brick; do not bring exposed mains into the chamber electronics.

#### SparkFun AP63357 5 V buck — `COM-21255`

- **Source/price:** SparkFun, US$7.70.
- **Verified headline specification:** 3.8–32 V input, fixed 5 V, up to 3.5 A subject to thermal conditions.
- **Use:** digital, camera auxiliary, and fan rail where current budget permits.

## 3. Optional MVP items

### ams OSRAM AS7341 breakout — Adafruit PID `4698`

- **Observed price/status:** US$18.95, out of stock at verification.
- **Bands:** visible channels centred near 415, 445, 480, 515, 555, 590, 630, and 680 nm, plus broad NIR/clear/flicker channels.
- **Use:** compact surface-pigment descriptor.
- **Limit:** neither a continuous spectrometer nor a water/oil NIR analyser. Do not delay the MVP for an out-of-stock optional board.

### SPEC Sensors DGS2-C2H4 — `970-650`

- **Source/price:** DigiKey, US$120, active listing.
- **Use:** only as an exploratory bridge sensor calibrated against a reference analyser in avocado headspace.
- **Critical caveat:** the manufacturer’s cross-sensitivity table includes responses to ethanol, hydrogen sulfide, sulfur dioxide, nitric oxide, and formaldehyde. One published table entry gives 0.6 ppm indicated response to 200 ppm ethanol; other interferents can produce responses comparable with or larger than the nominal range. Fruit volatiles therefore create a credible confounding pathway.
- **Decision:** optional, not required. Do not use it to generate the primary ethylene ground truth.

### SparkFun 12 V vacuum pump

- **Source/price:** SparkFun, US$25.50.
- **Use:** flushing or proof-of-concept circulation.
- **Limit:** wetted materials/recovery are not characterised for analytical volatiles. Keep it out of the quantitative reference path unless blank, adsorption, and recovery performance are validated.

## 4. Mid-tier spectral options

### Hamamatsu C11708MA

- **Source/price:** RS Components Portugal, €650.53 ex VAT, observed stock 2 at verification.
- **Official specifications:** 640–1050 nm, 256 pixels, typical 15 nm and maximum 20 nm spectral resolution, 5 V, 30 mW, 27.6 × 16.8 × 13 mm, approximately 9 g.
- **Use:** compact pigment/weak-water spectral proof of concept.
- **Integration reality:** this is a bare analogue microspectrometer head. It requires incident optics, a wavelength-stable geometry, pixel timing, analogue buffering, ADC acquisition, dark/white calibration, shielding, and firmware.
- **Limit:** silicon cutoff excludes 1200/1450/1700/2300 nm. It should not be described as an internal oil/moisture analyser without empirical calibration.

### Hamamatsu C14384MA-01

- **Official specifications:** 640–1050 nm, 256 pixels, typical 17/max 20 nm, 11.7 × 4 × 3.1 mm, approximately 0.3 g; Hamamatsu reports substantially higher sensitivity near 1000 nm than C11708MA.
- **Status:** quote only; no current authorised-distributor price was verified.
- **Decision:** request a quote only if miniaturisation and 1000 nm sensitivity justify custom electronics.

## 5. Research-grade optical system

### Ocean Insight NIRQuest+1.7 — family `NIRQUEST+1.7-XX`

- **Official specifications:** 900–1650 nm cooled InGaAs, 512 pixels, 1 ms–120 s integration; SMA 905 input; resolution depends on slit/grating and is listed as 2.8 nm for a 25 µm example configuration.
- **Use:** moisture/dry-matter calibration, spectroscopy of 1200 and 1450 nm features, and multivariate model development.
- **Procurement:** obtain a matched quote for slit, grating, fibre, light source, probe geometry, and software.
- **Price evidence:** a 2023 U.S. federal purchase of a NIRQuest+1.7 package, software, shipping, and surcharge was US$19,979. This is deliberately labelled a historical proxy, not a 2026 vendor quote.
- **Limit:** ends before the approximately 1720 and 2300 nm lipid bands. If oil chemistry is central, specify the +2.5 family or another extended-range instrument.

### Ocean Insight NIRQuest+2.5

- **Use:** extended SWIR coverage suitable for the avocado lipid-related 1720/2300 nm regions.
- **Status:** quote only. Exact detector, slit/grating, signal-to-noise, cooling, accessories, and price must be confirmed.
- **Decision:** university shared core is strongly preferred until pilot data show that extended SWIR materially improves the scientific endpoint.

### Marktech InGaAs photodiode — `MTPD1346D-100`

- **Source/price:** DigiKey, US$16.63 each; three budgeted, US$49.89.
- **Verified band:** 800–1750 nm; 1 mm active area; TO-46.
- **Use:** 1200 and 1450 nm feasibility channels with dark/temperature correction.
- **Limit:** discrete channels can test signal feasibility, but broad absorption and scattering make them much less identifiable than a calibrated spectrum.

### Roithner SWIR LEDs — `LED1200S-03`, `LED1450S-03`

- **Budget:** US$60 allowance, quotation required.
- **Use:** pair with InGaAs detector for controlled 1200/1450 nm measurements.
- **Interpretation:** 1450 nm is a strong water band but more surface-weighted due to high absorption; 970 nm is weaker but typically penetrates more deeply. Neither channel alone yields internal moisture percentage.

### Source, probe, and white standard

US$2,300 is reserved for a stabilised tungsten-halogen source, fibres, and a repeatable interactance/reflectance probe; US$700 is reserved for a certified diffuse reflectance standard. These are configuration allowances pending the chosen spectrometer.

Do not substitute printer paper or the visible ColorChecker for the NIR radiometric standard. Retain certification data, monitor contamination, and record reference identity with every scan.

## 6. Research-grade headspace system

### Felix Instruments F-900

- **Source/price:** QA Supplies, SKU `2002995`, US$10,495.
- **Manufacturer PPB-channel specification:** 0–10 ppm; 0.001 ppm resolution; stated 25 ppb detection limit; stated accuracy \(5\% \pm 0.025\) ppm.
- **Use:** reference ethylene for validating a low-cost bridge sensor and for selected biological endpoints.
- **Protocol:** use the applicable PolarCept/interference-removal procedure, calibration gas, blanks, controlled flow, and recovery checks.
- **Limit:** the cost and maintenance make it shared-core equipment. Even reference analysers require method validation in humid mixed fruit headspace.

### KNF NMP 830

- **Official family capability:** up to approximately 3.1 L/min depending configuration; oil-free diaphragm designs and PTFE-coated diaphragm option.
- **Status:** quote only.
- **Use:** controlled research gas loop.
- **Procurement dependency:** select head material, diaphragm, motor voltage, flow, vacuum/pressure, and fittings only after the analyser and chamber pressure-drop requirements are frozen.

### PTFE tubing — Cole-Parmer `UX-50119-48`

- **Source/price:** Cole-Parmer, US$367.50 for 50 ft, 1/8 in ID × 1/4 in OD.
- **Use:** replaceable low-adsorption headspace path.
- **Limit:** PTFE improves chemical inertness but does not eliminate wall memory, fittings dead volume, leaks, or condensation. Verify dose recovery with relevant gases.

### Analytical chamber

The US$1,000 custom-vessel allowance is for a known-volume borosilicate or stainless chamber with PTFE-faced seals and serviceable ports. Final procurement requires an engineering drawing, safe pressure/vacuum envelope, cleaning protocol, fruit loading access, leak criterion, and wetted-material list.

## 7. Destructive ground truth and laboratory equipment

### ATAGO PAL-1 — model `PAL-1`, Cat. No. `3810`

- **Source/price:** ATAGO Direct, US$330.
- **Specification:** Brix 0.0–53.0%; 0.1% resolution; ±0.2% stated accuracy; 2–3 drop sample.
- **Use:** soluble-solids concentration on a destructive homogenate/extract.
- **Limit:** °Brix is refractive concentration, affected by water loss and non-sugar solutes. It cannot by itself prove how much starch converted to sugar.

### QA Supplies FT327 — SKU `2006060`

- **Source/price:** QA Supplies, US$285.
- **Use:** controlled destructive firmness.
- **Vendor caveat:** QA Supplies notes that freshly harvested avocados may require the higher-range FT444.
- **Protocol requirements:** specify probe, peel removal, penetration depth, loading speed, location, temperature, and replicate aggregation.

### OHAUS MB120 AM — material `30241165`

- **Price evidence:** 2026 authorised-distributor list gives US$7,530 list / US$6,400.50 MAP.
- **Specification:** 120 g capacity, 0.001 g readability, programmable drying.
- **Use:** rapid moisture/dry-matter reference once the method is validated.
- **Limit:** halogen moisture methods can differ from a reference convection-vacuum oven depending on temperature, endpoint, volatile loss, grind, and sample thickness. Validate against the adopted standard method.
- **Decision:** use an existing laboratory moisture analyser/oven where possible.

### Other shared laboratory capabilities

The following are not assigned fabricated product numbers or prices because the correct method depends on the study protocol:

- calibrated analytical balance and reference weights;
- drying oven/vacuum oven and desiccator if used as the primary gravimetric reference;
- validated starch assay reagents/spectrophotometer;
- oil extraction (for example, Soxhlet or validated solvent method), fume hood, solvent handling, and hazardous-waste route;
- gas calibration standards, regulator, bags/manifold, and institutional gas safety;
- optional GC-FID/GC-MS for ethylene/VOC confirmation.

These must be captured in the institution-specific method and safety plan before data collection.

## 8. Procurement groups

### Order first

`MVP-001` through `MVP-017`, plus local fabrication/consumable rows `MVP-019`–`MVP-023`.

### Order after LED quotation

`MVP-018`, confirming exact wavelengths, bins, packages, forward voltages, drive limits, and availability.

### Do not block MVP on

AS7341 availability, electrochemical ethylene, pump circulation, Hamamatsu microspectrometers, or any SWIR system.

### University-lab availability check before purchase

NIRQuest-equivalent spectrometer and accessories, F-900 or GC reference, MB120/oven, analytical balance, oil/starch facilities, gas calibration equipment, and safe chemical workspace.

## 9. Product images

Local catalogue images are intentionally limited to products whose reuse terms were verified:

- [`images/sparkfun-hx711-sen-13879.jpg`](./images/sparkfun-hx711-sen-13879.jpg)
- [`images/sparkfun-tal220-sen-13329.jpg`](./images/sparkfun-tal220-sen-13329.jpg)

Licensing, attribution, source URLs, and hashes are recorded in [`images/README.md`](./images/README.md). For all other exact models, the BOM and source ledger link to the official product page/image rather than copying an image without a clear reuse grant.

## 10. Purchase acceptance checklist

For every ordered line:

1. match manufacturer and exact MPN, not only reseller description;
2. archive vendor quote, date, currency, tax/freight, lead time, and calibration option;
3. download the manufacturer datasheet/manual and record revision;
4. photograph received label/serial/lot and inspect for substitutions;
5. run incoming functional checks;
6. add device ID, firmware, calibration, and warranty details to the equipment register;
7. reject unsupported claims such as “24-bit accuracy,” “VOC ppm,” or “NIR moisture” that exceed the verified method.
