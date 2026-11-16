"""Checks behind reports/independent-review-2026-11-16.md.

Re-reads this repository's own retained outputs and asks questions the baseline
report does not ask. Nothing is retrained and no new data is used.

Inputs (already in the repository):
  ml/results/oof-predictions.csv                 out-of-fold predictions for every model
  data/processed/hass_avocado_rgb_metadata.csv   one row per workbook record

Standard library only, so it runs without the pinned scientific stack:

  python analysis/review_checks.py

Sections
  1  Storage shift: in-distribution versus held-out performance, per storage group
  2  Image-weighted versus fruit-weighted accuracy
  3  Agreement between the two photographed sides of a fruit on the same day
  4  Predictions that move backwards in time
  5  Where the classification errors are
  6  Days to first stage 4: the image model against baselines that use no image
  7  Does the image say anything the calendar does not?
  8  Follow-up, removals and batch structure of the source dataset
"""

from __future__ import annotations

import csv
import math
import random
import statistics as st
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OOF = ROOT / "ml" / "results" / "oof-predictions.csv"
META = ROOT / "data" / "processed" / "hass_avocado_rgb_metadata.csv"

CLASSES = [1, 2, 3, 4, 5]
GROUPS = ["T10", "T20", "Tam"]
CLASSIFIER = "Histogram gradient boosting"
REGRESSOR = "Histogram gradient boosting regressor"
SEED = 20261116


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def class_metrics(pairs) -> tuple[float, float, float, int]:
    """(accuracy, balanced accuracy, ordinal MAE, n) for (truth, prediction) pairs."""
    by_class = defaultdict(lambda: [0, 0])
    n = hits = distance = 0
    for truth, prediction in pairs:
        by_class[truth][1] += 1
        if truth == prediction:
            by_class[truth][0] += 1
            hits += 1
        distance += abs(truth - prediction)
        n += 1
    recalls = [by_class[c][0] / by_class[c][1] for c in CLASSES if by_class[c][1]]
    return hits / n, sum(recalls) / len(recalls), distance / n, n


def mae(pairs) -> float:
    pairs = list(pairs)
    return sum(abs(a - b) for a, b in pairs) / len(pairs)


def pearson(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return sxy / math.sqrt(sxx * syy) if sxx > 0 and syy > 0 else float("nan")


def main() -> None:
    rows = read_csv(OOF)
    meta = {row["file_name"]: row for row in read_csv(META)}

    cls = [row for row in rows if row["model"] == CLASSIFIER]
    for row in cls:
        row["t"] = int(float(row["truth"]))
        row["p"] = int(float(row["prediction"]))
    reg = [row for row in rows if row["model"] == REGRESSOR]
    for row in reg:
        row["y"] = float(row["truth"])
        row["yhat"] = float(row["prediction"])
        row["d"] = int(row["day"])
        row["stage"] = int(meta[row["file_name"]]["ripening_stage"])

    print("Independent review checks, AvocadoRipenessResearch")
    print(f"classifier rows: {len(cls)}   regression rows: {len(reg)}")

    # ------------------------------------------------------------------ 1
    print("\n== 1. Storage shift: in-distribution (5-fold fruit-grouped OOF) versus held-out")
    held_out = {}
    with (ROOT / "tables" / "storage-holdout-results.csv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            held_out[row["held_out_storage"]] = row
    print(f"   {'group':5s} {'fruits':>6s} {'images':>7s} {'img/fruit':>9s} {'bal.acc in-distribution':>24s}"
          f" {'bal.acc held out':>17s} {'drop':>6s} {'training images when held out':>30s}")
    for group in GROUPS:
        sub = [row for row in cls if row["storage_group"] == group]
        fruits = len({row["fruit_id"] for row in sub})
        _, balanced, _, n = class_metrics((row["t"], row["p"]) for row in sub)
        out = float(held_out[group]["balanced_accuracy"])
        print(f"   {group:5s} {fruits:6d} {n:7d} {n / fruits:9.1f} {balanced:24.3f} {out:17.3f} {balanced - out:6.3f}"
              f" {int(held_out[group]['train_images']):30d}")
    _, balanced, _, n = class_metrics((row["t"], row["p"]) for row in cls)
    print(f"   pooled in-distribution balanced accuracy: {balanced:.3f} on {n} images")

    # ------------------------------------------------------------------ 2
    print("\n== 2. Image-weighted versus fruit-weighted accuracy")
    per_fruit = defaultdict(list)
    for row in cls:
        per_fruit[row["fruit_id"]].append(row["t"] == row["p"])
    fruit_acc = sorted(sum(v) / len(v) for v in per_fruit.values())
    image_acc = sum(row["t"] == row["p"] for row in cls) / len(cls)
    print(f"   image-weighted {image_acc:.3f}   fruit-weighted {sum(fruit_acc) / len(fruit_acc):.3f}"
          f"   worst-decile fruit {fruit_acc[len(fruit_acc) // 10]:.3f}"
          f"   fruits below 0.5: {sum(a < 0.5 for a in fruit_acc)} of {len(fruit_acc)}")

    # ------------------------------------------------------------------ 3
    print("\n== 3. The two sides of one fruit on one day carry the same label. Do the predictions agree?")
    by_fruit_day = defaultdict(list)
    for row in cls:
        by_fruit_day[(row["fruit_id"], row["day"])].append(row)
    pairs = [v for v in by_fruit_day.values() if len(v) == 2]
    agree = sum(v[0]["p"] == v[1]["p"] for v in pairs)
    both = sum(v[0]["p"] == v[0]["t"] and v[1]["p"] == v[1]["t"] for v in pairs)
    none = sum(v[0]["p"] != v[0]["t"] and v[1]["p"] != v[1]["t"] for v in pairs)
    mixed_truth = sum(v[0]["t"] != v[1]["t"] for v in pairs)
    print(f"   fruit-days with two images: {len(pairs)} of {len(by_fruit_day)};"
          f" pairs whose TRUE stages differ: {mixed_truth}")
    print(f"   predictions agree: {agree / len(pairs):.3f}   both right: {both / len(pairs):.3f}"
          f"   one right: {(len(pairs) - both - none) / len(pairs):.3f}   both wrong: {none / len(pairs):.3f}")

    # ------------------------------------------------------------------ 4
    print("\n== 4. True stages never go backwards within a fruit and side. Do predictions?")
    sequences = defaultdict(list)
    for row in cls:
        sequences[(row["fruit_id"], meta[row["file_name"]]["side"])].append((int(row["day"]), row["p"], row["t"]))
    steps = back = true_back = 0
    reversed_fruits = set()
    for (fruit, _side), seq in sequences.items():
        seq.sort()
        for (_, p0, t0), (_, p1, t1) in zip(seq, seq[1:]):
            steps += 1
            true_back += t1 < t0
            if p1 < p0:
                back += 1
                reversed_fruits.add(fruit)
    print(f"   consecutive steps: {steps}   true-stage decreases: {true_back}"
          f"   predicted-stage decreases: {back} ({back / steps:.1%})"
          f"   fruits with at least one: {len(reversed_fruits)} of {len(per_fruit)}")

    # ------------------------------------------------------------------ 5
    print("\n== 5. Row-normalised confusion of the selected classifier")
    confusion = Counter((row["t"], row["p"]) for row in cls)
    print("   true\\pred " + " ".join(f"{c:>6d}" for c in CLASSES))
    for truth in CLASSES:
        total = sum(confusion[(truth, p)] for p in CLASSES)
        print(f"   {truth:9d} " + " ".join(f"{confusion[(truth, p)] / total:6.2f}" for p in CLASSES) + f"   n={total}")
    adjacent = sum(v for (t, p), v in confusion.items() if abs(t - p) == 1)
    far = sum(v for (t, p), v in confusion.items() if abs(t - p) >= 2)
    print(f"   adjacent-stage errors: {adjacent / len(cls):.1%}   two or more stages off: {far / len(cls):.1%}")

    # ------------------------------------------------------------------ 6
    print("\n== 6. Days to first stage 4: mean absolute error in days")
    fruits = sorted({row["fruit_id"] for row in reg})
    random.Random(SEED).shuffle(fruits)
    fold_of = {fruit: index % 5 for index, fruit in enumerate(fruits)}

    def in_sample(key) -> float:
        cells = defaultdict(list)
        for row in reg:
            cells[key(row)].append(row["y"])
        medians = {k: st.median(v) for k, v in cells.items()}
        return mae((row["y"], medians[key(row)]) for row in reg)

    def grouped_cv(key, fallback) -> float:
        """Five folds by fruit: cell medians come from the other four folds only."""
        errors = []
        for fold in range(5):
            cells, coarse, everything = defaultdict(list), defaultdict(list), []
            for row in reg:
                if fold_of[row["fruit_id"]] != fold:
                    cells[key(row)].append(row["y"])
                    coarse[fallback(row)].append(row["y"])
                    everything.append(row["y"])
            medians = {k: st.median(v) for k, v in cells.items()}
            coarse_medians = {k: st.median(v) for k, v in coarse.items()}
            overall = st.median(everything)
            for row in reg:
                if fold_of[row["fruit_id"]] == fold:
                    guess = medians.get(key(row), coarse_medians.get(fallback(row), overall))
                    errors.append(abs(row["y"] - guess))
        return sum(errors) / len(errors)

    print(f"   rows {len(reg)}, fruits {len(fruits)}; baselines are medians of the target within a cell")
    print(f"   {'predictor':58s} {'in-sample':>10s} {'5-fold by fruit':>16s}")
    print(f"   {'image model as published (colour features only)':58s} {'':>10s} {mae((r['y'], r['yhat']) for r in reg):16.3f}")
    specs = [
        ("global median (the published dummy)", lambda r: 0, lambda r: 0),
        ("true current stage", lambda r: r["stage"], lambda r: 0),
        ("storage group", lambda r: r["storage_group"], lambda r: 0),
        ("storage group + true current stage", lambda r: (r["storage_group"], r["stage"]), lambda r: r["storage_group"]),
        ("storage group + days elapsed (no image at all)", lambda r: (r["storage_group"], r["d"]), lambda r: r["storage_group"]),
    ]
    for label, key, fallback in specs:
        print(f"   {label:58s} {in_sample(key):10.3f} {grouped_cv(key, fallback):16.3f}")
    print("   by storage group (5-fold by fruit for the calendar baseline):")
    for group in GROUPS:
        sub = [row for row in reg if row["storage_group"] == group]
        errors = []
        for fold in range(5):
            cells = defaultdict(list)
            for row in sub:
                if fold_of[row["fruit_id"]] != fold:
                    cells[row["d"]].append(row["y"])
            medians = {k: st.median(v) for k, v in cells.items()}
            overall = st.median([v for values in cells.values() for v in values])
            errors += [abs(row["y"] - medians.get(row["d"], overall)) for row in sub if fold_of[row["fruit_id"]] == fold]
        print(f"     {group}: n={len(sub):5d}  image model {mae((r['y'], r['yhat']) for r in sub):.3f}"
              f"   storage group + days elapsed {sum(errors) / len(errors):.3f}"
              f"   mean target {sum(r['y'] for r in sub) / len(sub):.2f} d")

    # ------------------------------------------------------------------ 7
    print("\n== 7. Within one storage group on one day, does the image model rank fruits correctly?")
    print("   residual = value minus the median over all fruits in the same group on the same day")
    cells = defaultdict(list)
    for row in reg:
        cells[(row["storage_group"], row["d"])].append(row)
    for members in cells.values():
        my, mp = st.median(r["y"] for r in members), st.median(r["yhat"] for r in members)
        for row in members:
            row["ry"], row["rp"] = row["y"] - my, row["yhat"] - mp
    for group in GROUPS + ["all"]:
        sub = [row for row in reg if group == "all" or row["storage_group"] == group]
        rho = pearson([r["rp"] for r in sub], [r["ry"] for r in sub])
        print(f"   {group:4s} n={len(sub):5d}  SD of true residual {st.pstdev(r['ry'] for r in sub):.2f} d"
              f"   correlation(model residual, true residual) {rho:+.3f}   share of residual variance {rho * rho:.1%}")

    # ------------------------------------------------------------------ 8
    print("\n== 8. Source dataset: follow-up, removals and batch structure")
    by_fruit = defaultdict(list)
    for row in meta.values():
        by_fruit[row["fruit_id"]].append(row)
    for group in GROUPS:
        members = {f: sorted(v, key=lambda r: int(r["day"])) for f, v in by_fruit.items() if v[0]["storage_group"] == group}
        last_days = Counter(int(v[-1]["day"]) for v in members.values())
        first4 = sorted(float(v[0]["first_stage4_day"]) for v in members.values() if v[0]["first_stage4_day"])
        never = [v for v in members.values() if not v[0]["first_stage4_day"]]
        start_dates = Counter(v[0]["timestamp"][:10] for v in members.values())
        start_stage = Counter(int(v[0]["ripening_stage"]) for v in members.values())
        print(f"   {group}: {len(members)} fruits; first-day dates {dict(sorted(start_dates.items()))};"
              f" first-day stage {dict(sorted(start_stage.items()))}")
        print(f"       last observed day -> fruits: {dict(sorted(last_days.items()))}")
        print(f"       reached stage 4: {len(first4)} (first stage-4 day median {st.median(first4):.0f},"
              f" SD {st.pstdev(first4):.2f}, range {first4[0]:.0f}-{first4[-1]:.0f});"
              f" never reached: {len(never)}, of which removed before the group's last day:"
              f" {sum(int(v[-1]['day']) < max(last_days) for v in never)}")


if __name__ == "__main__":
    main()
