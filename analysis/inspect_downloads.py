"""Inspect acquired avocado datasets without modifying raw source files."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq


ROOT = Path(__file__).resolve().parents[1]
PARQUET_PATH = (
    ROOT
    / "data"
    / "raw"
    / "hass_avocado_mendeley_hf_mirror"
    / "hass_avocado_9899rows.parquet"
)
WORKBOOK_PATH = (
    ROOT
    / "data"
    / "raw"
    / "hass_avocado_mendeley_hf_mirror"
    / "Avocado Ripening Dataset.xlsx"
)
OUTPUT_PATH = ROOT / "tmp" / "downloads" / "inspection_summary.json"


def main() -> None:
    parquet = pq.ParquetFile(PARQUET_PATH)
    first = parquet.read_row_group(0).slice(0, 3)
    workbook = pd.read_excel(WORKBOOK_PATH, sheet_name="DATABASE")

    first_rows = first.to_pylist()
    for row in first_rows:
        image = row.get("image")
        if isinstance(image, dict) and image.get("bytes") is not None:
            image["bytes_length"] = len(image["bytes"])
            image["bytes"] = None

    summary = {
        "parquet_path": str(PARQUET_PATH),
        "parquet_rows": parquet.metadata.num_rows,
        "parquet_row_groups": parquet.metadata.num_row_groups,
        "parquet_schema": str(parquet.schema_arrow),
        "parquet_first_rows": first_rows,
        "workbook_path": str(WORKBOOK_PATH),
        "workbook_rows": len(workbook),
        "workbook_columns": workbook.columns.tolist(),
        "workbook_storage_counts": workbook["Storage Group"]
        .value_counts(dropna=False)
        .to_dict(),
        "workbook_stage_counts": workbook["Ripening Index Classification"]
        .value_counts(dropna=False)
        .sort_index()
        .to_dict(),
        "workbook_unique_samples": int(workbook["Sample"].nunique()),
        "workbook_unique_storage_sample_pairs": int(
            workbook[["Storage Group", "Sample"]].drop_duplicates().shape[0]
        ),
        "workbook_duplicate_file_names": int(workbook["File Name"].duplicated().sum()),
        "workbook_missing_values": workbook.isna().sum().to_dict(),
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()
