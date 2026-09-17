# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

"""
Read the file in data/, make one picture, save it to out/.

    uv run plot.py

This draws the 2026 daily rainfall at the Hong Kong Observatory.
"""

import csv
import datetime as dt
from pathlib import Path

import matplotlib.pyplot as plt

FILE = "rainfall-daily.csv"                    # the same name as in fetch.py
PICTURE = "rainfall-2026.png"                  # what goes into out/, and into the README
YEAR = 2026                                    # only this year, for now

HERE = Path(__file__).parent
DATA = HERE / "data" / FILE
OUT = HERE / "out"


def rows(path):
    """The file as a list of lists, one per line. The Observatory puts two lines
    of titles above the table and a legend below it, so keep only the lines that
    start with a year."""
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
    for year, month, day, value, quality in table:   # the loop over the numbers
        if int(year) != YEAR:                        # keep only 2026
            continue
        if value.strip() == "***":                   # the Observatory's word for "missing"
            continue
        if value.strip() == "Trace":                 # less than 0.05 mm
            value = "0.0"
        dates.append(dt.date(int(year), int(month), int(day)))
        values.append(float(value))                  # it arrived as text; make it a number
    print(f"{len(values)} values, from {min(values)} to {max(values)} mm")
    print(f"first day: {dates[0]}, last day: {dates[-1]}")

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.bar(dates, values, color="#1f6fb4", width=1.0)
    ax.set_xlabel("date in 2026")
    ax.set_ylabel("daily total rainfall, mm")
    ax.set_title(f"Hong Kong Observatory daily rainfall, {YEAR} (Jan–Jul)")
    fig.tight_layout()

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / PICTURE, dpi=150)
    print(f"saved out/{PICTURE}")
    plt.show()


if __name__ == "__main__":
    main()