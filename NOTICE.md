# Third-party data: attribution and rights status

## Dataset used for modelling (CC BY 4.0)

The exploratory analysis and every baseline model in this repository are
computed from:

> Xavier, R., et al. (2024). *'Hass' Avocado Ripening Photographic Dataset*,
> version 1. Mendeley Data. https://doi.org/10.17632/3xd9n945v8.1
> Licensed CC BY 4.0.

14,710 reconciled photographs of 478 individual fruits. The derived
colour/texture feature table and metadata table in `data/processed/` are
adaptations of that dataset and therefore also carry CC BY 4.0 obligations:
credit the dataset authors as well as this repository. The raw images are not
redistributed here; download them from the DOI above.

## Datasets deliberately not used

These rights decisions are documented in `data/dataset_inventory.csv` and are
part of the project's method, not gaps in acquisition:

| Dataset | Status | Reason |
| --- | --- | --- |
| Avocado and Strawberry Ripening Stages (10.17632/zysvgmxcyz.1, CC BY 4.0) | Acquired, excluded from modelling | Archive structure, image counts and augmentation lineage could not be reconciled with the landing page. |
| DeepHS Fruit v2 | Annotations and repository metadata only | No explicit dataset reuse terms; the ~77 GB avocado hyperspectral payload was never downloaded. |
| RipeTrack (10.1109/TMC.2025.3599917) | Literature comparison only | Code is licensed, the dataset is not; data payload was never downloaded. |

## Results boundary

Model results in this repository are internal, fruit-grouped validation on a
single public dataset. Storage-condition holdouts degrade substantially
(balanced accuracy 0.497 on the coldest condition), so nothing here supports a
deployment, device or harvest-season generalisation claim.
