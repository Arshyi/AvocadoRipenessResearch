"""Generate reproducible exploratory summaries for the processed Hass dataset."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
METADATA_PATH = ROOT / "data" / "processed" / "hass_avocado_rgb_metadata.csv"
FEATURES_PATH = ROOT / "data" / "processed" / "hass_avocado_rgb_features.csv"
FIGURES = ROOT / "figures"
TABLES = ROOT / "tables"
SUMMARY_PATH = ROOT / "analysis" / "eda-summary.json"
STORAGE_LABELS = {
    "T10": "10 C, 85% RH",
    "T20": "20 C, 85% RH",
    "Tam": "Ambient",
}
PALETTE = {"T10": "#2A6F97", "T20": "#F28E2B", "Tam": "#4E9F3D"}


def _save(fig: plt.Figure, name: str) -> None:
    fig.savefig(FIGURES / name, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    metadata = pd.read_csv(METADATA_PATH, parse_dates=["timestamp"])
    features = pd.read_csv(FEATURES_PATH, parse_dates=["timestamp"])

    sns.set_theme(style="whitegrid", context="talk")
    plt.rcParams.update({"figure.dpi": 120, "axes.titleweight": "bold"})

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    stage_counts = metadata["ripening_stage"].value_counts().sort_index()
    sns.barplot(
        x=stage_counts.index,
        y=stage_counts.values,
        color="#2A6F97",
        ax=axes[0],
    )
    axes[0].set(
        title="Workbook records by ripening stage",
        xlabel="Ripening index stage",
        ylabel="Image records",
    )
    storage_counts = (
        metadata.groupby("storage_group")["fruit_id"]
        .nunique()
        .reindex(["T10", "T20", "Tam"])
    )
    sns.barplot(
        x=[STORAGE_LABELS[index] for index in storage_counts.index],
        y=storage_counts.values,
        hue=storage_counts.index,
        palette=PALETTE,
        legend=False,
        ax=axes[1],
    )
    axes[1].set(
        title="Independent fruits by storage condition",
        xlabel="Storage condition",
        ylabel="Unique fruits",
    )
    axes[1].tick_params(axis="x", rotation=15)
    _save(fig, "dataset-distribution.png")

    fruit_day = (
        metadata.groupby(["fruit_id", "storage_group", "day"], as_index=False)
        .agg(ripening_stage=("ripening_stage", "median"))
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(
        data=fruit_day,
        x="day",
        y="ripening_stage",
        hue="storage_group",
        hue_order=["T10", "T20", "Tam"],
        palette=PALETTE,
        estimator="median",
        errorbar=("pi", 50),
        marker="o",
        ax=ax,
    )
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles,
        [STORAGE_LABELS.get(label, label) for label in labels],
        title="Storage",
    )
    ax.set(
        title="Observed ripening-index trajectory",
        xlabel="Day of experiment",
        ylabel="Median stage (band: interquartile range)",
        ylim=(0.8, 5.2),
    )
    _save(fig, "ripening-stage-by-day.png")

    fruit_endpoints = (
        metadata[["fruit_id", "storage_group", "first_stage4_day", "first_stage5_day"]]
        .drop_duplicates("fruit_id")
        .copy()
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(
        data=fruit_endpoints,
        x="storage_group",
        y="first_stage4_day",
        order=["T10", "T20", "Tam"],
        hue="storage_group",
        palette=PALETTE,
        legend=False,
        showfliers=False,
        ax=ax,
    )
    sns.stripplot(
        data=fruit_endpoints.sample(
            min(len(fruit_endpoints), 478), random_state=20260730
        ),
        x="storage_group",
        y="first_stage4_day",
        order=["T10", "T20", "Tam"],
        color="#1A1A1A",
        alpha=0.25,
        size=3,
        ax=ax,
    )
    ax.set_xticks(
        ax.get_xticks(), [STORAGE_LABELS[key] for key in ["T10", "T20", "Tam"]]
    )
    ax.set(
        title="First day reaching stage 4 (dataset-defined shelf-life endpoint)",
        xlabel="Storage condition",
        ylabel="First stage-4 day",
    )
    _save(fig, "time-to-stage4-by-storage.png")

    sampled = (
        features.groupby(["fruit_id", "day", "side"], group_keys=False)
        .head(1)
        .sample(min(6000, len(features)), random_state=20260730)
    )
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    sns.boxplot(
        data=sampled,
        x="ripening_stage",
        y="hsv_v_fg_mean",
        color="#7FB3D5",
        showfliers=False,
        ax=axes[0],
    )
    axes[0].set(
        title="Foreground value (brightness) by stage",
        xlabel="Ripening stage",
        ylabel="Mean HSV value",
    )
    sns.boxplot(
        data=sampled,
        x="ripening_stage",
        y="excess_green",
        color="#82C785",
        showfliers=False,
        ax=axes[1],
    )
    axes[1].set(
        title="Foreground excess-green index by stage",
        xlabel="Ripening stage",
        ylabel="2G - R - B",
    )
    _save(fig, "color-features-by-stage.png")

    missing = metadata.loc[~metadata["image_present"]]
    summary_rows = []
    for storage, group in metadata.groupby("storage_group"):
        fruit_group = fruit_endpoints[fruit_endpoints["storage_group"] == storage]
        summary_rows.append(
            {
                "storage_group": storage,
                "storage_description": STORAGE_LABELS[storage],
                "independent_fruits": int(group["fruit_id"].nunique()),
                "workbook_records": int(len(group)),
                "available_jpegs": int(group["image_present"].sum()),
                "median_first_stage4_day": float(
                    fruit_group["first_stage4_day"].median()
                ),
                "iqr_first_stage4_day": float(
                    fruit_group["first_stage4_day"].quantile(0.75)
                    - fruit_group["first_stage4_day"].quantile(0.25)
                ),
            }
        )
    summary_table = pd.DataFrame(summary_rows)
    summary_table.to_csv(TABLES / "eda-summary.csv", index=False)

    summary = {
        "workbook_records": int(len(metadata)),
        "available_images": int(features["file_name"].nunique()),
        "independent_fruits": int(metadata["fruit_id"].nunique()),
        "missing_image_records": int(len(missing)),
        "stage_counts": {
            str(key): int(value) for key, value in stage_counts.items()
        },
        "storage_summary": summary_rows,
        "median_first_stage4_day_overall": float(
            fruit_endpoints["first_stage4_day"].median()
        ),
        "fruits_without_stage4": int(
            fruit_endpoints["first_stage4_day"].isna().sum()
        ),
        "fruits_without_stage5": int(
            fruit_endpoints["first_stage5_day"].isna().sum()
        ),
        "interpretation_boundary": (
            "Descriptive associations are DATA-DEMONSTRATED for this dataset; "
            "causal temperature effects are not identified because storage "
            "assignment, harvest batch, and ambient conditions are not jointly "
            "randomized and fully recorded."
        ),
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
