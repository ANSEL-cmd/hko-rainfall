# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "matplotlib",
# ]
# ///

import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt


DATA_FILE = Path("data/rainfall-daily.csv")
OUTPUT_FILE = Path("out/rain-curtain.png")

YEAR = 2026
MONTHS = [6, 7, 8]


def read_rainfall(path):
    """Read daily rainfall data from the Hong Kong Observatory CSV."""

    data = []

    with open(path, "r", encoding="utf-8-sig") as file:
        # The CSV has two title lines before the actual column headers.
        next(file)
        next(file)

        reader = csv.DictReader(file)

        for row in reader:
            try:
                year = int(row["年/Year"])
                month = int(row["月/Month"])
                day = int(row["日/Day"])
                value = row["數值/Value"]

                if year != YEAR or month not in MONTHS:
                    continue

                if value in ("***", ""):
                    rainfall = 0.0
                else:
                    rainfall = float(value)

                data.append((month, day, rainfall))

            except (ValueError, KeyError):
                continue

    return data


def draw_rain_curtain(data):

    values = [value for _, _, value in data]

    maximum = max(values)
    total = sum(values)
    average = total / len(values)

    fig, ax = plt.subplots(figsize=(15, 10))

    background = "#F3F0E8"
    ink = "#234B68"
    dark = "#183C55"
    light = "#6D8494"

    fig.patch.set_facecolor(background)
    ax.set_facecolor(background)

    ax.set_xlim(-1, len(data))
    ax.set_ylim(-18, 108)

    # --------------------------------------------------
    # Continuous rain field
    # --------------------------------------------------

    for day_index, (_, _, rainfall) in enumerate(data):

        if rainfall <= 0:
            continue

        # Convert rainfall to visual density.
        strength = math.sqrt(rainfall / maximum)

        # More rainfall = denser rain.
        density = int(2 + strength * 18)

        spacing = 0.8 / max(density, 1)

        start_x = day_index - 0.4

        for j in range(density):

            x = start_x + (j + 0.5) * spacing

            # Slight diagonal direction.
            tilt = -0.08

            # More rainfall = darker rain.
            alpha = 0.12 + strength * 0.55

            # More rainfall = slightly thicker rain.
            linewidth = 0.35 + strength * 0.65

            ax.plot(
                [x, x + tilt],
                [2, 98],
                color=ink,
                linewidth=linewidth,
                alpha=alpha,
                solid_capstyle="round",
            )

    # --------------------------------------------------
    # Month boundaries
    # --------------------------------------------------

    month_names = {
        6: "JUNE",
        7: "JULY",
        8: "AUGUST",
    }

    current_month = None
    month_start = 0
    month_ranges = []

    for i, (month, _, _) in enumerate(data):

        if month != current_month:

            if current_month is not None:
                month_ranges.append(
                    (current_month, month_start, i)
                )

            current_month = month
            month_start = i

    month_ranges.append(
        (current_month, month_start, len(data))
    )

    for index, (month, start, end) in enumerate(month_ranges):

        if index > 0:

            ax.plot(
                [start - 0.5, start - 0.5],
                [0, 100],
                color=ink,
                linewidth=0.5,
                alpha=0.10,
            )

        center = (start + end) / 2

        ax.text(
            center,
            -4.0,
            month_names[month],
            ha="center",
            va="top",
            fontsize=8,
            fontweight="bold",
            color=ink,
            alpha=0.55,
        )

    # --------------------------------------------------
    # Small date markers
    # --------------------------------------------------

    for i, (month, day, _) in enumerate(data):

        # Show every fifth day.
        if day % 5 == 0:

            ax.plot(
                [i, i],
                [-1.4, -0.4],
                color=light,
                linewidth=0.45,
                alpha=0.35,
            )

            ax.text(
                i,
                -2.0,
                f"{day:02d}",
                ha="center",
                va="top",
                fontsize=6.5,
                color=light,
                alpha=0.55,
            )

    # --------------------------------------------------
    # Title
    # --------------------------------------------------

    ax.text(
        -0.5,
        107,
        "RAIN CURTAIN",
        ha="left",
        va="top",
        fontsize=24,
        fontweight="bold",
        color=dark,
    )

    ax.text(
        -0.5,
        102.5,
        "Hong Kong · Daily rainfall · June — August 2026",
        ha="left",
        va="top",
        fontsize=9,
        color=ink,
        alpha=0.55,
    )

    # --------------------------------------------------
    # Top 3 rainfall events
    # --------------------------------------------------

    ranked = sorted(
        enumerate(data),
        key=lambda item: item[1][2],
        reverse=True,
    )

    top_events = ranked[:3]

    # Different colors for the three highlighted rainfall events.
    event_colors = [
        "#183C55",
        "#4F7185",
        "#8A9DA8",
    ]

    for rank, (index, (month, day, rainfall)) in enumerate(top_events):

        if rainfall <= 0:
            continue

        marker_color = event_colors[rank]

        # Small colored dot above the corresponding rain column.
        ax.scatter(
            index,
            99.5,
            s=18,
            color=marker_color,
            zorder=5,
        )

        # Data label in the upper-right.
        # The dot and text use the same color as the marker.
        label_x = len(data) - 2
        label_y = 104.5 - rank * 2.3

        ax.text(
            label_x,
            label_y,
            f"●  {day:02d}.{month:02d}   {rainfall:.1f} mm",
            ha="right",
            va="center",
            fontsize=7,
            color=marker_color,
            alpha=0.85,
        )

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    # Maximum
    ax.text(
        -0.5,
        -8.0,
        f"{maximum:.1f}",
        ha="left",
        va="top",
        fontsize=15,
        fontweight="bold",
        color=dark,
    )

    ax.text(
        -0.5,
        -11.0,
        "MAX mm",
        ha="left",
        va="top",
        fontsize=6.5,
        color=light,
        alpha=0.8,
    )

    # Average
    ax.text(
        len(data) / 2,
        -8.0,
        f"{average:.1f}",
        ha="center",
        va="top",
        fontsize=15,
        fontweight="bold",
        color=dark,
    )

    ax.text(
        len(data) / 2,
        -11.0,
        "AVERAGE mm / DAY",
        ha="center",
        va="top",
        fontsize=6.5,
        color=light,
        alpha=0.8,
    )

    # Total
    ax.text(
        len(data),
        -8.0,
        f"{total:,.1f}",
        ha="right",
        va="top",
        fontsize=15,
        fontweight="bold",
        color=dark,
    )

    ax.text(
        len(data),
        -11.0,
        "TOTAL mm",
        ha="right",
        va="top",
        fontsize=6.5,
        color=light,
        alpha=0.8,
    )

    # --------------------------------------------------
    # Small data note
    # --------------------------------------------------

    ax.text(
        len(data),
        -14.5,
        "HONG KONG OBSERVATORY · 92 DAILY RECORDS",
        ha="right",
        va="top",
        fontsize=6.5,
        color=light,
        alpha=0.55,
    )

    # --------------------------------------------------
    # Clean frame
    # --------------------------------------------------

    ax.axis("off")

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    plt.savefig(
        OUTPUT_FILE,
        dpi=300,
        bbox_inches="tight",
        facecolor=background,
    )

    plt.close()


def main():

    data = read_rainfall(DATA_FILE)

    if not data:
        raise ValueError("No rainfall data found.")

    draw_rain_curtain(data)

    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()