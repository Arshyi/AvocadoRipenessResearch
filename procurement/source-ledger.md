# Procurement and Specification Source Ledger

**Checked:** 2026-07-30  
**Rule:** manufacturer/datasheet sources establish specifications; manufacturer stores or authorised distributors establish current prices. Aggregators and historical contracts are explicitly labelled.

| ID | Item / claim | Specification source | Price / availability source | Evidence used and caveat |
|---|---|---|---|---|
| S01 | ESP32-S3-DevKitC-1-N8R8 | [Espressif DevKitC-1 documentation](https://documentation.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/index.html) | [Component Search Engine distributor snapshot](https://componentsearchengine.com/prices/ESP32-S3-DevKitC-1-N8R8?manufacturer=Espressif+Systems) | Exact N8R8 configuration; DigiKey US$15 listing. Aggregator should be reconfirmed at order. |
| S02 | Raspberry Pi Zero 2 W | [Official product portal](https://pip.raspberrypi.com/categories/584-raspberry-pi-zero-2-w) | [Official buy page](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/?variant=raspberry-pi-zero-2-w) | Ordering code SC1176; official US$15 class MSRP retained, but reseller stock/price varies. |
| S03 | Raspberry Pi Camera Module 3 | [Official product brief](https://cdn-shop.adafruit.com/product-files/5660/camera-module-3-product-brief.pdf) | [Adafruit PID 5657](https://www.adafruit.com/product/5657) | US$29.25; 12 MP IMX708, autofocus, standard field of view. |
| S04 | ColorChecker Classic Mini | [Calibrite product page](https://calibrite.com/us/product/colorchecker-classic-mini/?noredirect=en-US) | [Calibrite shop](https://shop.calibrite.com/colorchecker-classic-mini-ccc-mini/) | SKU CCC-MINI; US$74; 24 patches, 63.5 × 109.0 mm. |
| S05 | SHT45 | [Sensirion SHT45 catalogue](https://sensirion.com/products/catalog/SHT45) | [Adafruit PID 5665](https://www.adafruit.com/product/5665) | US$13.50 with PTFE membrane; typical accuracy quoted only in manufacturer-stated conditions. |
| S06 | SCD30 | [Sensirion SCD30 catalogue](https://sensirion.com/products/catalog/SCD30) | [Adafruit PID 4867](https://www.adafruit.com/product/4867) | US$58.95; specified 400–10,000 ppm; NDIR. |
| S07 | BME688 | [Bosch BME688 page](https://www.bosch-sensortec.com/products/environmental-sensors/gas-sensors/bme688/) | [Adafruit PID 5046](https://www.adafruit.com/product/5046) | US$19.95. MOX gas resistance is non-specific; catalogue wording intentionally avoids compound ppm. |
| S08 | TAL220 load cell | [SparkFun SEN-13329](https://www.sparkfun.com/sparkfun-load-cell-10kg-straight-bar-tal220.html) | Same | US$12.95 observed. |
| S09 | HX711 board | [HX711 datasheet](https://cdn.sparkfun.com/assets/learn_tutorials/5/4/6/hx711F_EN.pdf) | [SparkFun SEN-13879](https://www.sparkfun.com/sparkfun-load-cell-amplifier-hx711.html) | US$4.95; 24-bit output is not treated as system accuracy. |
| S10 | ADS1115 | [Texas Instruments datasheet](https://www.ti.com/lit/ds/symlink/ads1115.pdf) | [Adafruit PID 1085](https://www.adafruit.com/product/1085) | US$14.95; 8–860 samples/s. |
| S11 | microSD breakout | [Adafruit guide](https://learn.adafruit.com/adafruit-micro-sd-breakout-board-card-tutorial) | [Adafruit PID 254](https://www.adafruit.com/product/254) | US$7.50; card excluded. |
| S12 | Mean Well GST60A12-P1J | [Manufacturer datasheet](https://www.meanwell-web.com/content/files/pdfs/productPdfs/MW/GST60A/GST60A-spec.pdf) | [DigiKey](https://www.digikey.com/en/products/detail/mean-well-usa-inc/GST60A12-P1J/7703712) | US$18.60; 12 V/5 A; IEC cord separate. |
| S13 | SparkFun AP63357 buck | [SparkFun COM-21255](https://www.sparkfun.com/sparkfun-buck-regulator-breakout-5v-ap63357.html) | Same | US$7.70; thermal derating remains application dependent. |
| S14 | Integra chamber shell | [Integra/AutomationDirect catalogue PDF](https://cdn.automationdirect.com/static/catalog/images/product-pdf/ENI-Integra-Enclosures.pdf) | [AutomationDirect exact product](https://www.automationdirect.com/adc/shopping/catalog/enclosures_-z-_subpanels_-z-_thermal_management_-z-_lighting/enclosures/polycarbonate_enclosures/h12106hcf-6p) | Exact MPN H12106HCF-6P-P10; US$150. Environmental rating is as supplied, before drilled ports. |
| S15 | Noctua NF-A4x10 5V | [Manufacturer specifications](https://www.noctua.at/en/products/nf-a4x10-5v/specifications) | [Manufacturer product page](https://www.noctua.at/en/products/nf-a4x10-5v) | US$14.95 is an allowance pending authorised local-reseller confirmation. |
| S16 | BPW34 | [Vishay datasheet mirror](https://www.digikey.com/htmldatasheets/production/1279013/0/0/1/bpw34.pdf) | [DigiKey exact part](https://www.digikey.com/en/products/detail/vishay-semiconductor-opto-division/BPW34/1681149) | US$1.37 observed; 430–1100 nm. Reconfirm tape/tube variant and tariff at order. |
| S17 | Roithner LED set | [Roithner current price/part list](https://www.roithner-laser.com/pricelist.pdf) | Same / request quotation | Exact part designations verified; US$50 and US$60 set values are allowances because columns/bin pricing were not unambiguously attributable. |
| S18 | AS7341 | [ams OSRAM official page](https://ams-osram.com/products/sensor-solutions/ambient-light-color-spectral-proximity-sensors/ams-as7341-11-channel-spectral-color-sensor) | [Adafruit PID 4698](https://www.adafruit.com/product/4698) | US$18.95 but out of stock. Broad NIR channel is not water/oil spectroscopy. |
| S19 | SPEC DGS2-C2H4 | [SPEC DGS2 datasheet](https://www.spec-sensors.com/wp-content/uploads/2024/06/DGS2-970-Series-Datasheet-24a.pdf) | [DigiKey 970-650](https://www.digikey.com/en/products/detail/spec-sensors-a-division-of-interlink-electronics/970-650/25269602) | US$120; range shown by distributor. Cross-sensitivity evidence drives optional-only classification. |
| S20 | Hamamatsu C11708MA | [Official product page](https://www.hamamatsu.com/eu/en/product/optical-sensors/spectrometers/mini-spectrometer/C11708MA.html), [datasheet](https://www.hamamatsu.com/content/dam/hamamatsu-photonics/sites/documents/99_SALES_LIBRARY/ssd/c10988ma-01_etc_kacc1169e.pdf) | [RS Portugal](https://pt.rs-online.com/web/p/kits-de-desarrollo-de-sensores/2616229) | €650.53 ex VAT; stock 2 observed. Bare head needs a complete optical/electrical readout. |
| S21 | Hamamatsu C14384MA-01 | [Official release/specifications](https://www.hamamatsu.com/eu/en/news/featured-products_and_technologies/2018/20181023000000.html) | Quote only | No current authorised price verified. |
| S22 | NIRQuest+1.7 | [Official product page](https://www.oceanoptics.com/spectrometer/nirquest1-7/), [2025 product sheet](https://www.oceanoptics.com/wp-content/uploads/2025/04/Ocean_NIRQuestPlus_Product_Sheet.pdf) | [2023 federal contract record](https://govtribe.com/award/federal-contract-award/purchase-order-n0017323p2034) | US$19,979 is a historical package proxy, not current price. Obtain a configuration-specific Ocean Insight quote. |
| S23 | Marktech MTPD1346D-100 | [Manufacturer datasheet mirror](https://www.mouser.com/datasheet/2/1094/MTPD1346D_100-1900758.pdf) | [DigiKey](https://www.digikey.com/en/products/detail/marktech-optoelectronics/MTPD1346D-100/5866635) | US$16.63; 800–1750 nm, 1 mm active area. |
| S24 | PTFE tubing | [Cole-Parmer exact product](https://www.coleparmer.com/i/cole-parmer-ptfe-tubing-1-8-id-x-1-4-od-50-ft/5011948) | Same | US$367.50 for 50 ft, exact size/MPN. |
| S25 | F-900 | [Felix support/specifications](https://felixinstruments.com/food-science-instruments/gas-analysis/food-science-instruments-handheld-ethylene-co2-o2-analysis-f-900-portable-ethylene-analyzer/support/) | [QA Supplies](https://qasupplies.com/f-900-portable-ethylene-analyzer/) | US$10,495; interference-removal protocol remains essential. |
| S26 | KNF NMP 830 | [Official family page](https://knf.com/en/uk/solutions/pumps/series/diaphragm-gas-pump-nmp-830) | Quote only | Flow is configuration dependent; no price asserted. |
| S27 | ATAGO PAL-1 | [ATAGO USA](https://atago-usa.com/PAL-1-p176.html) | [ATAGO Direct](https://atago.net/en/atagodirect-index.php?key=ABS42888) | US$330 direct; Cat. No. 3810; 0–53% Brix. |
| S28 | FT327 | [QA Supplies exact product](https://qasupplies.com/ft327-penetrometer/) | Same | US$285; page explicitly flags FT444 for very firm harvest-stage avocado. |
| S29 | OHAUS MB120 | [OHAUS product page](https://us.ohaus.com/products/balances-scales/moisture-analyzers/mb120) | [2026 authorised distributor price list](https://store.clarksonlab.com/Vendors/vOha.pdf) | Material 30241165; US$6,400.50 MAP. |
| S30 | SparkFun pump | [Exact product](https://www.sparkfun.com/vacuum-pump-12v.html) | Same | US$25.50. No analytical wetted-material claim is inferred. |
| S31 | SparkFun image reuse | [SparkFun image-licence notice](https://news.sparkfun.com/735) | N/A | Product images used locally under CC BY-NC-SA 3.0 for this non-commercial research document. |
| S32 | Noctua asset reuse policy | [Noctua legal information](https://www.noctua.at/en/legal-information) | N/A | Official photos may be used under stated royalty-free non-exclusive terms, but no local copy was included because an exact stable asset URL was not verified. |

## Scientific sources behind wavelength and geometry decisions

| ID | Source | Design implication |
|---|---|---|
| L01 | [Hass avocado NIR study, PMC10490472](https://pmc.ncbi.nlm.nih.gov/articles/PMC10490472/) | Visible chlorophyll information near 680 nm; water features around 930–1030/970, 1200, 1450, 1918 nm; lipid-related bands around 900–920, 1200, 1700, and 2200–2400 nm; scan-zone variability matters. |
| L02 | [Clark et al. 2003](https://www.sciencedirect.com/science/article/pii/S0925521403000462), DOI 10.1016/S0925-5214(03)00046-2 | Interactance outperformed reflectance in the cited avocado dry-matter experiment; reinforces controlled optical geometry and fruit-level calibration. |
| L03 | [SWIR tissue spectroscopy review](https://pmc.ncbi.nlm.nih.gov/articles/PMC4370890/) | Water bands near 970/1180/1450/1930 nm and lipid bands near 930/1040/1200/1400/1700 nm; stronger water absorption trades against penetration depth. |
| L04 | [Hass colour/pigment study](https://hortsci.agriculturejournals.cz/pdfs/hor/2024/02/07.pdf) | Peel pigment and colour change are useful longitudinal channels but are affected by temperature and are not guaranteed to remain synchronised with internal softening. |

## Audit notes

- A blank price means **no verified current price**; it is not zero cost.
- “Planning allowance” means engineering reserve, not vendor evidence.
- Historical contract values are included only to make the buy-new order of magnitude transparent.
- Currency conversion was intentionally avoided. The €650.53 C11708MA option is reported separately.
- Product-page screenshots or copied photos were not treated as freely reusable. Only exact images with a clear reuse basis were downloaded.
