# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

"""
Hong Kong Observatory daily rainfall, 2026 wet season (June–August).

    uv run plot.py
"""

import csv
import datetime as dt
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

FILE = "rainfall-daily.csv"
PICTURE = "rainfall-2026.png"
YEAR = 2026
MONTHS = (6, 7, 8)        # 只保留 6、7、8 月
LABEL_ABOVE = 100         # 只标 >= 100 mm 的日子

HERE = Path(__file__).parent
DATA = HERE / "data" / FILE
OUT = HERE / "out"

# ---------- the look ----------
BG = "#faf3e0"            # pale yellow background
GRID = "#d9cfae"          # slightly darker than the background
INK = "#3a3226"           # text colour, warm dark brown


def rows(path):
    kept = []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for line in csv.reader(handle):
            if line and line[0].strip().isdigit():
                kept.append(line)
    return kept


def main():
    table = rows(DATA)
    print(f"{DATA.name}: {len(table)} rows. The first one: {table[0]}")

    dates, values = [], []
    for year, month, day, value, quality in table:
        if int(year) != YEAR:
            continue
        if int(month) not in MONTHS:
            continue
        if value.strip() == "***":
            continue
        if value.strip() == "Trace":
            value = "0.0"
        dates.append(dt.date(int(year), int(month), int(day)))
        values.append(float(value))
    print(f"{len(values)} values, from {min(values)} to {max(values)} mm")

    colours = []
    for v in values:
        if v >= 100:
            colours.append("#c0392b")
        elif v >= 50:
            colours.append("#2c6e9b")
        else:
            colours.append("#a8c8e0")

    fig, ax = plt.subplots(figsize=(13, 5.5))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    ax.bar(dates, values, color=colours, width=0.8, edgecolor="none", zorder=3)

    # 每 20 mm 一条横向灰线
    ax.yaxis.grid(True, linestyle="-", linewidth=0.6, color=GRID, alpha=0.9, zorder=0)
    ax.set_axisbelow(True)

    # 50 mm 虚线
    ax.axhline(50, linestyle="--", linewidth=0.8, color="#b58b4c", alpha=0.8, zorder=1)

    # ---- 标注：放在柱子顶端，左右错开 ----
    big_days = [(d, v) for d, v in zip(dates, values) if v >= LABEL_ABOVE]
    big_days.sort(key=lambda p: p[0])
    # 左右偏移（天）：-3, 0, +3 轮流用，避免相邻重叠
    offsets = [-3, 0, 3]
    for k, (d, v) in enumerate(big_days):
        dx = offsets[k % 3]
        ax.annotate(
            f"{d.strftime('%d %b')}",
            xy=(d, v),                                    # 箭头指到柱子顶端
            xytext=(d + dt.timedelta(days=dx), v + 8),    # 文字放上方，左右错开
            ha="center", va="bottom", fontsize=9, color="#8a4b1f",
            arrowprops=dict(arrowstyle="-", color="#b58b4c", lw=0.6, alpha=0.8),
            bbox=dict(boxstyle="round,pad=0.18", fc=BG, ec="none", alpha=0.9),
        )
    print(f"labelled {len(big_days)} days above {LABEL_ABOVE} mm")

    # 横轴：每 10 天一个刻度
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    ax.set_xlim(dates[0] - dt.timedelta(days=2), dates[-1] + dt.timedelta(days=2))

    # 给标注留出上方空间
    ax.set_ylim(0, max(values) * 1.18)

    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    for side in ["left", "bottom"]:
        ax.spines[side].set_color(INK)
        ax.spines[side].set_linewidth(0.9)

    ax.tick_params(colors=INK, labelsize=9)
    ax.set_xlabel("day, June to August 2026", fontsize=11, color=INK)
    ax.set_ylabel("daily total rainfall, mm", fontsize=11, color=INK)

    days100 = sum(1 for v in values if v >= 100)
    days50 = sum(1 for v in values if v >= 50)
    ax.set_title(
        "Hong Kong Observatory — the 2026 wet season",
        fontsize=15, color=INK, pad=32, loc="left",
    )
    ax.text(
        0.0, 1.015,
        f"June to August 2026 · "
        f"{days100} days above 100 mm · {days50} days above 50 mm",
        transform=ax.transAxes, fontsize=10, color="#8a4b1f", va="bottom",
    )

    fig.tight_layout()

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / PICTURE, dpi=150, facecolor=BG)
    print(f"saved out/{PICTURE}")
    plt.show()


if __name__ == "__main__":
    main()