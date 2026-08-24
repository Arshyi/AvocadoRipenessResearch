"""Draw a publication-ready overview of the proposed avocado sensor system."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "figures" / "prototype-system-overview.png"


def box(ax, x, y, w, h, text, color, text_color="#102A43", size=9.5):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.015,rounding_size=0.025",
        linewidth=1.2,
        edgecolor="#334E68",
        facecolor=color,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=size,
        color=text_color,
        linespacing=1.25,
        weight="semibold",
    )
    return patch


def arrow(ax, start, end, label=None, curve=0.0):
    a = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=13,
        linewidth=1.25,
        color="#486581",
        connectionstyle=f"arc3,rad={curve}",
    )
    ax.add_patch(a)
    if label:
        ax.text(
            (start[0] + end[0]) / 2,
            (start[1] + end[1]) / 2 + 0.015,
            label,
            ha="center",
            va="center",
            fontsize=7.5,
            color="#486581",
            backgroundcolor="white",
        )


def main():
    plt.rcParams.update({"font.family": "DejaVu Sans"})
    fig, ax = plt.subplots(figsize=(14, 8.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(
        0.5,
        0.96,
        "Proposed multimodal avocado characterization system",
        ha="center",
        va="center",
        fontsize=20,
        weight="bold",
        color="#102A43",
    )
    ax.text(
        0.5,
        0.915,
        "Repeated non-destructive measurements linked to matched destructive ground truth",
        ha="center",
        va="center",
        fontsize=11,
        color="#486581",
    )

    box(
        ax,
        0.04,
        0.59,
        0.20,
        0.22,
        "Indexed Hass avocado\nfruit ID, zone, side,\ntime, batch, storage",
        "#D9EAF7",
        size=11,
    )

    box(
        ax,
        0.31,
        0.70,
        0.20,
        0.13,
        "Optical bay\nlocked RGB + reference\n660 / 740 / 850 / 970 nm",
        "#DCEFE2",
    )
    box(
        ax,
        0.31,
        0.53,
        0.20,
        0.13,
        "Transient headspace\nT / RH + NDIR CO2\nconditioned MOX trend",
        "#FCE8D5",
    )
    box(
        ax,
        0.31,
        0.36,
        0.20,
        0.13,
        "Mass and handling\nload cell + calibration\nstorage exposure log",
        "#ECE2F4",
    )

    box(
        ax,
        0.58,
        0.62,
        0.17,
        0.16,
        "Immutable raw layer\nimages, counts, spectra,\ncalibration and QC",
        "#EAF0F6",
    )
    box(
        ax,
        0.58,
        0.39,
        0.17,
        0.16,
        "Derived trajectories\ncolour, reflectance,\nmass loss, CO2 slope",
        "#EAF0F6",
    )

    box(
        ax,
        0.80,
        0.66,
        0.17,
        0.15,
        "Grouped empirical ML\nfruit and batch holdout\nablation + uncertainty",
        "#D8EEF1",
    )
    box(
        ax,
        0.80,
        0.45,
        0.17,
        0.15,
        "Dynamic models\nmixed-effects ODEs\nBayesian state space",
        "#D8EEF1",
    )
    box(
        ax,
        0.80,
        0.24,
        0.17,
        0.15,
        "Outputs\nfirmness + time window\ncalibrated uncertainty",
        "#D8EEF1",
    )

    box(
        ax,
        0.31,
        0.11,
        0.44,
        0.14,
        "Matched sacrifice cohort\nfirmness | moisture / dry matter | Brix | starch | oil\npeel pigments | internal condition | reference ethylene subset",
        "#F6E3E3",
        size=9.5,
    )

    arrow(ax, (0.24, 0.72), (0.31, 0.765))
    arrow(ax, (0.24, 0.68), (0.31, 0.595))
    arrow(ax, (0.24, 0.64), (0.31, 0.425))
    arrow(ax, (0.51, 0.765), (0.58, 0.70))
    arrow(ax, (0.51, 0.595), (0.58, 0.67))
    arrow(ax, (0.51, 0.425), (0.58, 0.65))
    arrow(ax, (0.665, 0.62), (0.665, 0.55))
    arrow(ax, (0.75, 0.49), (0.80, 0.525))
    arrow(ax, (0.75, 0.49), (0.80, 0.735))
    arrow(ax, (0.885, 0.66), (0.885, 0.60))
    arrow(ax, (0.885, 0.45), (0.885, 0.39))
    arrow(ax, (0.53, 0.25), (0.63, 0.39), "calibration labels", curve=-0.12)
    arrow(ax, (0.31, 0.18), (0.22, 0.59), "scheduled fruit", curve=-0.20)

    ax.text(
        0.04,
        0.045,
        "Claims boundary: RGB, NIR, mass, CO2, and MOX are observations. "
        "Internal chemistry is a calibrated prediction only when matched reference assays support it.",
        fontsize=9,
        color="#486581",
    )
    fig.savefig(OUTPUT, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(OUTPUT)


if __name__ == "__main__":
    main()
