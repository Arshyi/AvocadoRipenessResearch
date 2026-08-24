"""Fruit-grouped RGB baselines for ripening stage and days-to-stage-4.

The predictors are compact color and texture summaries extracted from each
image. Storage condition, day, side, filename, and fruit identity are excluded
from the predictor matrix. Every day and side of a biological fruit remains in
one fold.
"""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.base import clone
from sklearn.compose import TransformedTargetRegressor
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import (
    HistGradientBoostingClassifier,
    HistGradientBoostingRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import GroupKFold, StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]
FEATURES_PATH = ROOT / "data" / "processed" / "hass_avocado_rgb_features.csv"
TABLES = ROOT / "tables"
FIGURES = ROOT / "figures"
RESULTS = ROOT / "ml" / "results"
ARTIFACTS = ROOT / "ml" / "artifacts"
SEED = 20260730
CLASS_LABELS = np.array([1, 2, 3, 4, 5])


def classification_models() -> dict[str, object]:
    return {
        "Prior-only dummy": DummyClassifier(strategy="prior"),
        "Multinomial logistic": Pipeline(
            [
                ("impute", SimpleImputer(strategy="median")),
                ("scale", StandardScaler()),
                (
                    "model",
                    LogisticRegression(
                        max_iter=2500,
                        class_weight="balanced",
                        C=1.0,
                        random_state=SEED,
                    ),
                ),
            ]
        ),
        "Random forest": Pipeline(
            [
                ("impute", SimpleImputer(strategy="median")),
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=300,
                        min_samples_leaf=3,
                        max_features="sqrt",
                        class_weight="balanced_subsample",
                        random_state=SEED,
                        n_jobs=-1,
                    ),
                ),
            ]
        ),
        "Histogram gradient boosting": Pipeline(
            [
                ("impute", SimpleImputer(strategy="median")),
                (
                    "model",
                    HistGradientBoostingClassifier(
                        max_iter=220,
                        learning_rate=0.07,
                        max_leaf_nodes=31,
                        min_samples_leaf=25,
                        l2_regularization=1.0,
                        class_weight="balanced",
                        random_state=SEED,
                    ),
                ),
            ]
        ),
    }


def regression_models() -> dict[str, object]:
    return {
        "Median dummy": DummyRegressor(strategy="median"),
        "Ridge regression": Pipeline(
            [
                ("impute", SimpleImputer(strategy="median")),
                ("scale", StandardScaler()),
                ("model", Ridge(alpha=10.0)),
            ]
        ),
        "Random forest regressor": Pipeline(
            [
                ("impute", SimpleImputer(strategy="median")),
                (
                    "model",
                    RandomForestRegressor(
                        n_estimators=300,
                        min_samples_leaf=3,
                        max_features=0.7,
                        random_state=SEED,
                        n_jobs=-1,
                    ),
                ),
            ]
        ),
        "Histogram gradient boosting regressor": Pipeline(
            [
                ("impute", SimpleImputer(strategy="median")),
                (
                    "model",
                    HistGradientBoostingRegressor(
                        max_iter=220,
                        learning_rate=0.07,
                        max_leaf_nodes=31,
                        min_samples_leaf=25,
                        l2_regularization=1.0,
                        random_state=SEED,
                    ),
                ),
            ]
        ),
    }


def feature_columns(frame: pd.DataFrame) -> list[str]:
    prefixes = (
        "rgb_",
        "hsv_",
        "gray_",
        "edge_",
        "chromatic_",
        "red_green_",
        "green_blue_",
        "excess_green",
        "foreground_fraction",
    )
    return [
        column
        for column in frame.columns
        if column.startswith(prefixes)
        and column not in {"rgb_image", "image_file"}
    ]


def metrics_from_confusion(matrix: np.ndarray) -> dict[str, float]:
    matrix = matrix.astype(float)
    total = matrix.sum()
    true_support = matrix.sum(axis=1)
    predicted_support = matrix.sum(axis=0)
    diagonal = np.diag(matrix)
    recall = np.divide(
        diagonal,
        true_support,
        out=np.full(diagonal.shape, np.nan),
        where=true_support > 0,
    )
    precision = np.divide(
        diagonal,
        predicted_support,
        out=np.zeros(diagonal.shape),
        where=predicted_support > 0,
    )
    f1 = np.divide(
        2 * precision * recall,
        precision + recall,
        out=np.zeros(diagonal.shape),
        where=(precision + recall) > 0,
    )
    distance = np.abs(CLASS_LABELS[:, None] - CLASS_LABELS[None, :])
    return {
        "accuracy": float(diagonal.sum() / total),
        "balanced_accuracy": float(np.nanmean(recall)),
        "macro_f1": float(np.nanmean(f1)),
        "ordinal_mae": float((matrix * distance).sum() / total),
    }


def classification_cluster_bootstrap(
    truth: np.ndarray,
    prediction: np.ndarray,
    groups: np.ndarray,
    iterations: int = 1000,
) -> tuple[dict[str, float], dict[str, tuple[float, float]]]:
    group_values = np.unique(groups)
    matrices = []
    for group in group_values:
        use = groups == group
        matrices.append(
            confusion_matrix(
                truth[use], prediction[use], labels=CLASS_LABELS
            ).astype(float)
        )
    matrices = np.stack(matrices)
    point = metrics_from_confusion(matrices.sum(axis=0))
    rng = np.random.default_rng(SEED)
    draws = {metric: [] for metric in point}
    for _ in range(iterations):
        indices = rng.integers(0, len(group_values), len(group_values))
        result = metrics_from_confusion(matrices[indices].sum(axis=0))
        for metric, value in result.items():
            draws[metric].append(value)
    intervals = {
        metric: (
            float(np.quantile(values, 0.025)),
            float(np.quantile(values, 0.975)),
        )
        for metric, values in draws.items()
    }
    return point, intervals


def regression_cluster_bootstrap(
    truth: np.ndarray,
    prediction: np.ndarray,
    groups: np.ndarray,
    iterations: int = 1000,
) -> tuple[dict[str, float], dict[str, tuple[float, float]]]:
    group_values = np.unique(groups)
    indices_by_group = [np.flatnonzero(groups == group) for group in group_values]

    def calculate(indices: np.ndarray) -> dict[str, float]:
        y_true = truth[indices]
        y_pred = prediction[indices]
        return {
            "mae": float(mean_absolute_error(y_true, y_pred)),
            "rmse": float(mean_squared_error(y_true, y_pred) ** 0.5),
            "r2": float(r2_score(y_true, y_pred)),
        }

    point = calculate(np.arange(len(truth)))
    rng = np.random.default_rng(SEED + 1)
    draws = {metric: [] for metric in point}
    for _ in range(iterations):
        selected = rng.integers(0, len(group_values), len(group_values))
        indices = np.concatenate([indices_by_group[index] for index in selected])
        result = calculate(indices)
        for metric, value in result.items():
            draws[metric].append(value)
    intervals = {
        metric: (
            float(np.quantile(values, 0.025)),
            float(np.quantile(values, 0.975)),
        )
        for metric, values in draws.items()
    }
    return point, intervals


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    frame = pd.read_csv(FEATURES_PATH)
    features = feature_columns(frame)
    x = frame[features].to_numpy(dtype=float)
    y_class = frame["ripening_stage"].to_numpy(dtype=int)
    groups = frame["fruit_id"].to_numpy()

    class_splitter = StratifiedGroupKFold(
        n_splits=5, shuffle=True, random_state=SEED
    )
    class_models = classification_models()
    class_predictions: dict[str, np.ndarray] = {
        name: np.full(len(frame), -1, dtype=int) for name in class_models
    }
    fold_rows = []
    split_rows = []
    for fold, (train, test) in enumerate(
        class_splitter.split(x, y_class, groups), start=1
    ):
        train_groups = set(groups[train])
        test_groups = set(groups[test])
        if train_groups.intersection(test_groups):
            raise RuntimeError("Fruit leakage detected in classification folds")
        split_rows.append(
            {
                "task": "ripening_stage_classification",
                "fold": fold,
                "train_images": len(train),
                "test_images": len(test),
                "train_fruits": len(train_groups),
                "test_fruits": len(test_groups),
                "fruit_overlap": 0,
            }
        )
        for name, estimator in class_models.items():
            model = clone(estimator)
            model.fit(x[train], y_class[train])
            prediction = model.predict(x[test]).astype(int)
            class_predictions[name][test] = prediction
            fold_rows.append(
                {
                    "task": "ripening_stage_classification",
                    "model": name,
                    "fold": fold,
                    "accuracy": accuracy_score(y_class[test], prediction),
                    "balanced_accuracy": balanced_accuracy_score(
                        y_class[test], prediction
                    ),
                    "macro_f1": f1_score(
                        y_class[test], prediction, average="macro"
                    ),
                    "ordinal_mae": mean_absolute_error(y_class[test], prediction),
                    "mae": np.nan,
                    "rmse": np.nan,
                    "r2": np.nan,
                }
            )

    comparison_rows = []
    prediction_frames = []
    class_summaries = {}
    for name, prediction in class_predictions.items():
        if np.any(prediction < 0):
            raise RuntimeError(f"Incomplete OOF predictions for {name}")
        point, intervals = classification_cluster_bootstrap(
            y_class, prediction, groups
        )
        class_summaries[name] = {"point": point, "ci95": intervals}
        comparison_rows.append(
            {
                "task": "ripening_stage_classification",
                "model": name,
                "validation": "5-fold stratified grouped CV; group=biological fruit",
                "n_observations": len(frame),
                "n_fruits": frame["fruit_id"].nunique(),
                "accuracy": point["accuracy"],
                "accuracy_ci_low": intervals["accuracy"][0],
                "accuracy_ci_high": intervals["accuracy"][1],
                "balanced_accuracy": point["balanced_accuracy"],
                "balanced_accuracy_ci_low": intervals["balanced_accuracy"][0],
                "balanced_accuracy_ci_high": intervals["balanced_accuracy"][1],
                "macro_f1": point["macro_f1"],
                "macro_f1_ci_low": intervals["macro_f1"][0],
                "macro_f1_ci_high": intervals["macro_f1"][1],
                "ordinal_mae": point["ordinal_mae"],
                "ordinal_mae_ci_low": intervals["ordinal_mae"][0],
                "ordinal_mae_ci_high": intervals["ordinal_mae"][1],
                "mae": np.nan,
                "mae_ci_low": np.nan,
                "mae_ci_high": np.nan,
                "rmse": np.nan,
                "rmse_ci_low": np.nan,
                "rmse_ci_high": np.nan,
                "r2": np.nan,
                "r2_ci_low": np.nan,
                "r2_ci_high": np.nan,
            }
        )
        prediction_frames.append(
            pd.DataFrame(
                {
                    "file_name": frame["file_name"],
                    "fruit_id": frame["fruit_id"],
                    "storage_group": frame["storage_group"],
                    "day": frame["day"],
                    "truth": y_class,
                    "prediction": prediction,
                    "model": name,
                }
            )
        )

    substantive = {
        name: values
        for name, values in class_summaries.items()
        if "dummy" not in name.lower()
    }
    best_class_model_name = max(
        substantive,
        key=lambda name: substantive[name]["point"]["balanced_accuracy"],
    )
    best_class_prediction = class_predictions[best_class_model_name]

    confusion = confusion_matrix(
        y_class, best_class_prediction, labels=CLASS_LABELS, normalize="true"
    )
    sns.set_theme(style="white", context="talk")
    fig, ax = plt.subplots(figsize=(8, 7))
    sns.heatmap(
        confusion,
        annot=True,
        fmt=".2f",
        cmap="Blues",
        vmin=0,
        vmax=1,
        xticklabels=CLASS_LABELS,
        yticklabels=CLASS_LABELS,
        ax=ax,
    )
    ax.set(
        title=f"Fruit-grouped OOF confusion: {best_class_model_name}",
        xlabel="Predicted stage",
        ylabel="True stage",
    )
    fig.savefig(
        FIGURES / "grouped-classification-confusion.png",
        dpi=200,
        bbox_inches="tight",
        facecolor="white",
    )
    plt.close(fig)

    metric_plot = pd.DataFrame(
        [
            {
                "model": name,
                "balanced_accuracy": values["point"]["balanced_accuracy"],
                "low": values["ci95"]["balanced_accuracy"][0],
                "high": values["ci95"]["balanced_accuracy"][1],
            }
            for name, values in class_summaries.items()
        ]
    ).sort_values("balanced_accuracy")
    fig, ax = plt.subplots(figsize=(10, 6))
    positions = np.arange(len(metric_plot))
    ax.barh(
        positions,
        metric_plot["balanced_accuracy"],
        color="#2A6F97",
        alpha=0.9,
    )
    ax.errorbar(
        metric_plot["balanced_accuracy"],
        positions,
        xerr=np.vstack(
            [
                metric_plot["balanced_accuracy"] - metric_plot["low"],
                metric_plot["high"] - metric_plot["balanced_accuracy"],
            ]
        ),
        fmt="none",
        ecolor="#1A1A1A",
        capsize=4,
    )
    ax.set_yticks(positions, metric_plot["model"])
    ax.set(
        title="Fruit-grouped ripening-stage performance",
        xlabel="Balanced accuracy (fruit-cluster bootstrap 95% CI)",
        xlim=(0, 1),
    )
    fig.savefig(
        FIGURES / "grouped-classification-performance.png",
        dpi=200,
        bbox_inches="tight",
        facecolor="white",
    )
    plt.close(fig)

    storage_rows = []
    best_estimator = classification_models()[best_class_model_name]
    for held_out in ["T10", "T20", "Tam"]:
        train = frame["storage_group"].to_numpy() != held_out
        test = ~train
        model = clone(best_estimator)
        model.fit(x[train], y_class[train])
        prediction = model.predict(x[test]).astype(int)
        storage_rows.append(
            {
                "model": best_class_model_name,
                "held_out_storage": held_out,
                "train_images": int(train.sum()),
                "test_images": int(test.sum()),
                "train_fruits": int(frame.loc[train, "fruit_id"].nunique()),
                "test_fruits": int(frame.loc[test, "fruit_id"].nunique()),
                "accuracy": accuracy_score(y_class[test], prediction),
                "balanced_accuracy": balanced_accuracy_score(
                    y_class[test], prediction
                ),
                "macro_f1": f1_score(
                    y_class[test], prediction, average="macro"
                ),
                "ordinal_mae": mean_absolute_error(y_class[test], prediction),
            }
        )
    pd.DataFrame(storage_rows).to_csv(
        TABLES / "storage-holdout-results.csv", index=False
    )

    regression_frame = frame.loc[
        frame["eligible_days_to_stage4"].astype(str).str.lower().isin(["true", "1"])
        & frame["days_to_stage4_signed"].notna()
    ].copy()
    x_reg = regression_frame[features].to_numpy(dtype=float)
    y_reg = regression_frame["days_to_stage4_signed"].to_numpy(dtype=float)
    groups_reg = regression_frame["fruit_id"].to_numpy()
    reg_models = regression_models()
    reg_predictions: dict[str, np.ndarray] = {
        name: np.full(len(regression_frame), np.nan) for name in reg_models
    }
    reg_splitter = GroupKFold(n_splits=5, shuffle=True, random_state=SEED)
    for fold, (train, test) in enumerate(
        reg_splitter.split(x_reg, y_reg, groups_reg), start=1
    ):
        train_groups = set(groups_reg[train])
        test_groups = set(groups_reg[test])
        if train_groups.intersection(test_groups):
            raise RuntimeError("Fruit leakage detected in regression folds")
        split_rows.append(
            {
                "task": "days_to_stage4_regression",
                "fold": fold,
                "train_images": len(train),
                "test_images": len(test),
                "train_fruits": len(train_groups),
                "test_fruits": len(test_groups),
                "fruit_overlap": 0,
            }
        )
        for name, estimator in reg_models.items():
            model = clone(estimator)
            model.fit(x_reg[train], y_reg[train])
            prediction = model.predict(x_reg[test]).astype(float)
            reg_predictions[name][test] = prediction
            fold_rows.append(
                {
                    "task": "days_to_stage4_regression",
                    "model": name,
                    "fold": fold,
                    "accuracy": np.nan,
                    "balanced_accuracy": np.nan,
                    "macro_f1": np.nan,
                    "ordinal_mae": np.nan,
                    "mae": mean_absolute_error(y_reg[test], prediction),
                    "rmse": mean_squared_error(y_reg[test], prediction) ** 0.5,
                    "r2": r2_score(y_reg[test], prediction),
                }
            )

    reg_summaries = {}
    for name, prediction in reg_predictions.items():
        if np.isnan(prediction).any():
            raise RuntimeError(f"Incomplete OOF regression predictions for {name}")
        point, intervals = regression_cluster_bootstrap(
            y_reg, prediction, groups_reg
        )
        reg_summaries[name] = {"point": point, "ci95": intervals}
        comparison_rows.append(
            {
                "task": "days_to_stage4_regression",
                "model": name,
                "validation": "5-fold grouped CV; group=biological fruit",
                "n_observations": len(regression_frame),
                "n_fruits": regression_frame["fruit_id"].nunique(),
                "accuracy": np.nan,
                "accuracy_ci_low": np.nan,
                "accuracy_ci_high": np.nan,
                "balanced_accuracy": np.nan,
                "balanced_accuracy_ci_low": np.nan,
                "balanced_accuracy_ci_high": np.nan,
                "macro_f1": np.nan,
                "macro_f1_ci_low": np.nan,
                "macro_f1_ci_high": np.nan,
                "ordinal_mae": np.nan,
                "ordinal_mae_ci_low": np.nan,
                "ordinal_mae_ci_high": np.nan,
                "mae": point["mae"],
                "mae_ci_low": intervals["mae"][0],
                "mae_ci_high": intervals["mae"][1],
                "rmse": point["rmse"],
                "rmse_ci_low": intervals["rmse"][0],
                "rmse_ci_high": intervals["rmse"][1],
                "r2": point["r2"],
                "r2_ci_low": intervals["r2"][0],
                "r2_ci_high": intervals["r2"][1],
            }
        )
        prediction_frames.append(
            pd.DataFrame(
                {
                    "file_name": regression_frame["file_name"],
                    "fruit_id": regression_frame["fruit_id"],
                    "storage_group": regression_frame["storage_group"],
                    "day": regression_frame["day"],
                    "truth": y_reg,
                    "prediction": prediction,
                    "model": name,
                }
            )
        )

    substantive_reg = {
        name: values
        for name, values in reg_summaries.items()
        if "dummy" not in name.lower()
    }
    best_reg_model_name = min(
        substantive_reg, key=lambda name: substantive_reg[name]["point"]["mae"]
    )

    final_class_model = clone(best_estimator).fit(x, y_class)
    joblib.dump(
        {
            "estimator": final_class_model,
            "feature_columns": features,
            "target": "ripening_stage",
            "training_scope": "all 14,710 available images after grouped CV",
            "source_doi": "10.17632/3xd9n945v8.1",
        },
        ARTIFACTS / "final_color_stage_model.joblib",
    )

    rf_pipeline = clone(classification_models()["Random forest"]).fit(x, y_class)
    rf_model = rf_pipeline.named_steps["model"]
    importance = pd.DataFrame(
        {
            "feature": features,
            "importance": rf_model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)
    importance.to_csv(TABLES / "feature-importance.csv", index=False)
    top = importance.head(20).sort_values("importance")
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(top["feature"], top["importance"], color="#4E9F3D")
    ax.set(
        title="Random-forest impurity importance (descriptive)",
        xlabel="Mean decrease in impurity",
    )
    fig.savefig(
        FIGURES / "color-feature-importance.png",
        dpi=200,
        bbox_inches="tight",
        facecolor="white",
    )
    plt.close(fig)

    comparison = pd.DataFrame(comparison_rows)
    comparison.to_csv(TABLES / "model-comparison.csv", index=False)
    pd.DataFrame(fold_rows).to_csv(RESULTS / "fold-metrics.csv", index=False)
    pd.DataFrame(split_rows).to_csv(RESULTS / "split-audit.csv", index=False)
    pd.concat(prediction_frames, ignore_index=True).to_csv(
        RESULTS / "oof-predictions.csv", index=False
    )

    summary = {
        "source_doi": "10.17632/3xd9n945v8.1",
        "predictor_scope": (
            "foreground-aware RGB/HSV/texture summaries only; no filename, "
            "fruit ID, day, side, stage, or storage variable is a predictor"
        ),
        "classification": {
            "n_images": int(len(frame)),
            "n_fruits": int(frame["fruit_id"].nunique()),
            "best_non_dummy_model": best_class_model_name,
            "models": class_summaries,
            "storage_holdout": storage_rows,
        },
        "days_to_stage4": {
            "definition": (
                "Dataset-derived days until first observation at ripening index "
                "stage 4; only observations on or before that endpoint"
            ),
            "n_images": int(len(regression_frame)),
            "n_fruits": int(regression_frame["fruit_id"].nunique()),
            "best_non_dummy_model": best_reg_model_name,
            "models": reg_summaries,
        },
        "validation_boundary": (
            "DATA-DEMONSTRATED only for internal fruit-grouped validation in "
            "this single study. Storage-condition holdout is a stress test, not "
            "independent harvest-season or external-device validation."
        ),
    }
    (RESULTS / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
