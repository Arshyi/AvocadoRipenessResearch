"""Validate the reproducible avocado analysis package."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_HASHES = {
    "data/raw/Hass-Avocado-Ripening-Photographic-Dataset-v1.zip":
        "FB14C3D8C6FB59A20BFFB579A5FE97C7EBA7030F4420882E8A75B575FF0C5BB6",
    "data/raw/Avocado-Strawberry-Ripening-Stages-v1.zip":
        "48B8E6B84DD3C58643F624C12689AF6E81A73E2A4CA8D7EB5BBFA7C507BE4224",
    "data/raw/DeepHS-Fruit-annotations-upd-2024-01-09.zip":
        "14275450E362684BC379A5AAF6C845CF82B0F9D5912036B9401D59A4B964A3F3",
    "data/raw/DeepHS-Fruit-readme.txt":
        "F4CDD2EFC40FF49740EE7CAD118CB019E227BF119F24506194919E15380513CA",
}
EXPECTED_TABLES = {
    "data/dataset_inventory.csv": 9,
    "data/processed/hass_avocado_rgb_metadata.csv": 14722,
    "data/processed/hass_avocado_rgb_features.csv": 14710,
    "tables/eda-summary.csv": 3,
    "tables/model-comparison.csv": 8,
    "tables/storage-holdout-results.csv": 3,
    "tables/feature-importance.csv": 86,
    "ml/results/fold-metrics.csv": 40,
    "ml/results/split-audit.csv": 10,
    "ml/results/oof-predictions.csv": 94176,
    "procurement/bill-of-materials.csv": 44,
}
REQUIRED_FILES = [
    "reports/data-quality-summary.json",
    "analysis/eda-summary.json",
    "ml/results/summary.json",
    "ml/artifacts/final_color_stage_model.joblib",
    "proposal/avocado-research-proposal.md",
    "output/pdf/avocado-research-proposal.pdf",
    "communications/collaborator-outreach-draft.md",
    "models/kinetic/candidate_models.py",
    "reproducibility/run_all.ps1",
    *[
        f"appendices/appendix-{letter}-{slug}.md"
        for letter, slug in [
            ("a", "existing-papers"),
            ("b", "bibliography"),
            ("c", "public-datasets"),
            ("d", "hardware-catalogue"),
            ("e", "mathematical-models"),
            ("f", "software-stack"),
            ("g", "repository-structure"),
            ("h", "data-quality"),
            ("i", "ml-results"),
            ("j", "statistical-plan"),
            ("k", "reproducibility"),
            ("l", "risk-evidence"),
        ]
    ],
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def validate(skip_large_hashes: bool) -> dict:
    checks: list[dict] = []

    for relative, expected_rows in EXPECTED_TABLES.items():
        path = ROOT / relative
        frame = pd.read_csv(path)
        ok = len(frame) == expected_rows and not frame.columns.duplicated().any()
        checks.append(
            {
                "check": f"table:{relative}",
                "status": "PASS" if ok else "FAIL",
                "observed_rows": len(frame),
                "expected_rows": expected_rows,
                "columns": len(frame.columns),
            }
        )

    split = pd.read_csv(ROOT / "ml/results/split-audit.csv")
    overlap = int(split["fruit_overlap"].max())
    checks.append(
        {
            "check": "fruit_split_overlap",
            "status": "PASS" if overlap == 0 else "FAIL",
            "observed_max_overlap": overlap,
        }
    )

    quality = json.loads(
        (ROOT / "reports/data-quality-summary.json").read_text(encoding="utf-8")
    )
    expected_quality = {
        "workbook_rows": (quality.get("workbook_rows"), 14722),
        "jpeg_files": (quality.get("jpeg_files"), 14710),
        "matched_rows": (quality.get("matched_rows"), 14710),
        "missing_image_rows": (len(quality.get("missing_image_rows", [])), 12),
    }
    for key, (observed, expected) in expected_quality.items():
        checks.append(
            {
                "check": f"quality:{key}",
                "status": "PASS" if observed == expected else "FAIL",
                "observed": observed,
                "expected": expected,
            }
        )

    summary = json.loads(
        (ROOT / "ml/results/summary.json").read_text(encoding="utf-8")
    )
    point = summary["classification"]["models"]["Histogram gradient boosting"][
        "point"
    ]["balanced_accuracy"]
    regression = summary["days_to_stage4"]["models"][
        "Histogram gradient boosting regressor"
    ]["point"]["mae"]
    checks.extend(
        [
            {
                "check": "ml:best_balanced_accuracy",
                "status": "PASS" if abs(point - 0.7307329032777372) < 1e-12 else "FAIL",
                "observed": point,
            },
            {
                "check": "ml:best_days_to_stage4_mae",
                "status": "PASS" if abs(regression - 1.8531579960773636) < 1e-12 else "FAIL",
                "observed": regression,
            },
        ]
    )

    for relative in REQUIRED_FILES:
        exists = (ROOT / relative).is_file()
        checks.append(
            {
                "check": f"required_file:{relative}",
                "status": "PASS" if exists else "FAIL",
            }
        )

    for relative, expected in EXPECTED_HASHES.items():
        path = ROOT / relative
        if skip_large_hashes and path.stat().st_size > 500_000_000:
            status, observed = "SKIP", None
        else:
            observed = sha256(path)
            status = "PASS" if observed == expected else "FAIL"
        checks.append(
            {
                "check": f"sha256:{relative}",
                "status": status,
                "observed": observed,
                "expected": expected,
            }
        )

    failures = [check for check in checks if check["status"] == "FAIL"]
    return {
        "status": "PASS" if not failures else "FAIL",
        "checks": checks,
        "failure_count": len(failures),
        "note": "Scientific claim boundaries still require human review; this validates files, rows, selected metrics, grouping, and checksums.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-large-hashes", action="store_true")
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    result = validate(args.skip_large_hashes)
    rendered = json.dumps(result, indent=2)
    print(rendered)
    if args.write_report:
        (ROOT / "reproducibility/validation-report.json").write_text(
            rendered + "\n", encoding="utf-8"
        )
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
