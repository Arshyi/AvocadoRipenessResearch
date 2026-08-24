# Processed data policy

Processed tables and features must be reproducible from `data/raw/` by scripts under `analysis/` or `ml/`.

The preferred metadata fields are:

```text
dataset_id
fruit_id
cultivar
batch_id
device_id
observation_time
days_since_start
days_until_ripe
firmness_N
moisture_percent_wb
dry_matter_percent
oil_content_percent
mass_g
temperature_C
relative_humidity_percent
colour_feature_reference
spectrum_reference
destructive_sample
```

Fields must not be populated by assuming equivalence between incompatible labels or units.
