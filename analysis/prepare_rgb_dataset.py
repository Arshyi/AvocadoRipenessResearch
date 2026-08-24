"""Prepare the licensed longitudinal Hass RGB dataset for grouped analysis.

Raw files are never modified. The script reconciles the primary Mendeley
workbook against the extracted JPEGs, derives fruit-safe identifiers and
remaining-time labels, and computes compact foreground-aware color/texture
features for classical baselines.
"""

from __future__ import annotations

import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = (
    ROOT
    / "data"
    / "raw"
    / "hass_avocado_mendeley_v1"
    / "Hass Avocado Ripening Photographic Dataset"
)
IMAGE_ROOT = RAW_ROOT / "Avocado Ripening Dataset"
WORKBOOK_PATH = RAW_ROOT / "Avocado Ripening Dataset.xlsx"
PROCESSED = ROOT / "data" / "processed"
QUALITY_JSON = ROOT / "reports" / "data-quality-summary.json"
FILENAME_PATTERN = re.compile(
    r"^(?P<storage>T10|T20|Tam)_d(?P<day>\d{2})_(?P<sample>\d{3})_"
    r"(?P<side>[ab])_(?P<stage>[1-5])$"
)


def _summaries(prefix: str, values: np.ndarray) -> dict[str, float]:
    values = np.asarray(values, dtype=np.float32)
    quantiles = np.quantile(values, [0.10, 0.50, 0.90])
    return {
        f"{prefix}_mean": float(np.mean(values)),
        f"{prefix}_std": float(np.std(values)),
        f"{prefix}_q10": float(quantiles[0]),
        f"{prefix}_q50": float(quantiles[1]),
        f"{prefix}_q90": float(quantiles[2]),
    }


def extract_features(path: Path) -> dict[str, float | str]:
    with Image.open(path) as source:
        source = source.convert("RGB")
        width, height = source.size
        small = source.resize((96, 96), Image.Resampling.BILINEAR)
        rgb = np.asarray(small, dtype=np.float32) / 255.0
        hsv = np.asarray(small.convert("HSV"), dtype=np.float32) / 255.0

    gray = (
        0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    )
    foreground = np.mean(rgb, axis=2) < 0.88
    if int(foreground.sum()) < 256:
        foreground = np.ones(gray.shape, dtype=bool)

    result: dict[str, float | str] = {
        "file_name": path.stem,
        "image_file": path.name,
        "image_width_px": int(width),
        "image_height_px": int(height),
        "foreground_fraction": float(np.mean(foreground)),
    }

    for index, channel in enumerate(("r", "g", "b")):
        result.update(_summaries(f"rgb_{channel}_fg", rgb[..., index][foreground]))
        result.update(_summaries(f"rgb_{channel}_all", rgb[..., index]))
        histogram, _ = np.histogram(
            rgb[..., index][foreground], bins=8, range=(0.0, 1.0), density=False
        )
        histogram = histogram / max(histogram.sum(), 1)
        for bin_index, value in enumerate(histogram):
            result[f"rgb_{channel}_hist_{bin_index}"] = float(value)

    for index, channel in enumerate(("h", "s", "v")):
        result.update(_summaries(f"hsv_{channel}_fg", hsv[..., index][foreground]))

    result.update(_summaries("gray_fg", gray[foreground]))
    horizontal = np.abs(np.diff(gray, axis=1))
    vertical = np.abs(np.diff(gray, axis=0))
    result["edge_abs_mean"] = float(
        (float(horizontal.mean()) + float(vertical.mean())) / 2
    )
    result["edge_abs_q90"] = float(
        np.quantile(np.concatenate((horizontal.ravel(), vertical.ravel())), 0.90)
    )

    mean_rgb = np.array(
        [
            result["rgb_r_fg_mean"],
            result["rgb_g_fg_mean"],
            result["rgb_b_fg_mean"],
        ],
        dtype=float,
    )
    denominator = float(mean_rgb.sum()) + 1e-9
    result["chromatic_r"] = float(mean_rgb[0] / denominator)
    result["chromatic_g"] = float(mean_rgb[1] / denominator)
    result["chromatic_b"] = float(mean_rgb[2] / denominator)
    result["red_green_ratio"] = float(mean_rgb[0] / (mean_rgb[1] + 1e-9))
    result["green_blue_ratio"] = float(mean_rgb[1] / (mean_rgb[2] + 1e-9))
    result["excess_green"] = float(
        2 * mean_rgb[1] - mean_rgb[0] - mean_rgb[2]
    )

    center = rgb[24:72, 24:72, :]
    for index, channel in enumerate(("r", "g", "b")):
        result[f"rgb_{channel}_center_mean"] = float(center[..., index].mean())
    return result


def _python_scalar(value):
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    return value


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    QUALITY_JSON.parent.mkdir(parents=True, exist_ok=True)

    metadata = pd.read_excel(WORKBOOK_PATH, sheet_name="DATABASE")
    metadata = metadata.rename(
        columns={
            "File Name": "file_name",
            "Time Stamp": "timestamp",
            "Storage Group": "storage_group",
            "Sample": "sample_id",
            "Day of Experiment": "day",
            "Ripening Index Classification": "ripening_stage",
        }
    )
    metadata["timestamp"] = pd.to_datetime(metadata["timestamp"], errors="coerce")
    metadata["sample_id"] = metadata["sample_id"].astype(int)
    metadata["day"] = metadata["day"].astype(int)
    metadata["ripening_stage"] = metadata["ripening_stage"].astype(int)
    metadata["fruit_id"] = metadata.apply(
        lambda row: f"{row['storage_group']}-{int(row['sample_id']):03d}", axis=1
    )
    metadata["side"] = metadata["file_name"].str.extract(
        FILENAME_PATTERN, expand=True
    )["side"]

    image_paths = sorted(IMAGE_ROOT.glob("*.jpg"))
    image_map = {path.stem: path for path in image_paths}
    metadata["image_present"] = metadata["file_name"].isin(image_map)
    metadata["relative_image_path"] = metadata["file_name"].map(
        lambda stem: image_map[stem].relative_to(ROOT).as_posix()
        if stem in image_map
        else ""
    )

    first_stage4 = (
        metadata.loc[metadata["ripening_stage"] >= 4]
        .groupby("fruit_id")["day"]
        .min()
    )
    first_stage5 = (
        metadata.loc[metadata["ripening_stage"] >= 5]
        .groupby("fruit_id")["day"]
        .min()
    )
    metadata["first_stage4_day"] = metadata["fruit_id"].map(first_stage4)
    metadata["first_stage5_day"] = metadata["fruit_id"].map(first_stage5)
    metadata["days_to_stage4_signed"] = metadata["first_stage4_day"] - metadata["day"]
    metadata["eligible_days_to_stage4"] = (
        metadata["first_stage4_day"].notna()
        & (metadata["day"] <= metadata["first_stage4_day"])
    )

    existing_stems = set(image_map)
    metadata_stems = set(metadata["file_name"])
    missing_image_rows = sorted(metadata_stems - existing_stems)
    unlisted_images = sorted(existing_stems - metadata_stems)

    encoded_mismatches: list[dict[str, object]] = []
    for row in metadata.itertuples(index=False):
        match = FILENAME_PATTERN.match(row.file_name)
        if not match:
            encoded_mismatches.append(
                {"file_name": row.file_name, "reason": "filename_pattern"}
            )
            continue
        encoded = match.groupdict()
        if (
            encoded["storage"] != row.storage_group
            or int(encoded["day"]) != row.day
            or int(encoded["sample"]) != row.sample_id
            or int(encoded["stage"]) != row.ripening_stage
        ):
            encoded_mismatches.append(
                {"file_name": row.file_name, "reason": "metadata_disagreement"}
            )

    sequence_violations = []
    ordered = metadata.sort_values(["fruit_id", "side", "day"])
    for (fruit_id, side), group in ordered.groupby(["fruit_id", "side"]):
        stages = group["ripening_stage"].to_numpy()
        if np.any(np.diff(stages) < 0):
            sequence_violations.append({"fruit_id": fruit_id, "side": side})

    print(f"Extracting features from {len(image_paths):,} JPEGs...")
    with ThreadPoolExecutor(max_workers=12) as pool:
        features = list(pool.map(extract_features, image_paths, chunksize=32))
    feature_frame = pd.DataFrame(features)
    available_metadata = metadata.loc[metadata["image_present"]].copy()
    analysis_frame = available_metadata.merge(
        feature_frame, how="inner", on="file_name", validate="one_to_one"
    )

    metadata_out = PROCESSED / "hass_avocado_rgb_metadata.csv"
    features_out = PROCESSED / "hass_avocado_rgb_features.csv"
    metadata.to_csv(metadata_out, index=False, date_format="%Y-%m-%dT%H:%M:%S")
    analysis_frame.to_csv(features_out, index=False, date_format="%Y-%m-%dT%H:%M:%S")

    quality = {
        "source": {
            "doi": "10.17632/3xd9n945v8.1",
            "license": "CC BY 4.0",
            "landing_url": "https://data.mendeley.com/datasets/3xd9n945v8/1",
        },
        "workbook_rows": int(len(metadata)),
        "jpeg_files": int(len(image_paths)),
        "matched_rows": int(metadata["image_present"].sum()),
        "missing_image_rows": missing_image_rows,
        "unlisted_images": unlisted_images,
        "duplicate_file_names": int(metadata["file_name"].duplicated().sum()),
        "missing_values_by_column": {
            key: int(value) for key, value in metadata.isna().sum().items()
        },
        "fruit_count": int(metadata["fruit_id"].nunique()),
        "fruit_count_by_storage": {
            key: int(value)
            for key, value in metadata.groupby("storage_group")["fruit_id"]
            .nunique()
            .items()
        },
        "record_count_by_storage": {
            key: int(value)
            for key, value in metadata["storage_group"].value_counts().items()
        },
        "record_count_by_stage": {
            str(key): int(value)
            for key, value in metadata["ripening_stage"].value_counts().sort_index().items()
        },
        "fruits_reaching_stage4_or_later": int(first_stage4.size),
        "fruits_reaching_stage5": int(first_stage5.size),
        "filename_metadata_mismatch_count": int(len(encoded_mismatches)),
        "filename_metadata_mismatches": encoded_mismatches[:100],
        "stage_sequence_violation_count": int(len(sequence_violations)),
        "stage_sequence_violations": sequence_violations[:100],
        "processed_feature_rows": int(len(analysis_frame)),
        "feature_columns": [
            column
            for column in analysis_frame.columns
            if column not in available_metadata.columns
        ],
    }
    QUALITY_JSON.write_text(
        json.dumps(quality, indent=2, default=_python_scalar), encoding="utf-8"
    )
    print(json.dumps(quality, indent=2, default=_python_scalar))


if __name__ == "__main__":
    main()
