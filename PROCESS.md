# Process

<!-- Same as assignment 1, same honesty. Which tools you used and for what; one
thing you kept and why it was good; one thing you rejected and why it was wrong.
"I did not use any" is fine if it is true.

If a model wrote most of plot.py, which is likely and allowed, the interesting part
is what you had to correct: did it invent a column name, use pandas where a list
would do, silently drop the rows it could not parse? -->

## Tools

- **Deepseek** — to adapt the template's `plot.py` from daily temperature to daily
  rainfall: rename the data file, keep only 2026, handle `Trace`, and switch
  from a line chart to a bar chart.
- **uv** — to run both scripts without installing anything globally.

## Kept

The template's `rows()` function. It reads the CSV, keeps only the lines that
start with a year, and throws away the two title lines at the top and the legend
at the bottom. It worked on my file exactly as it was written, so I did not
touch it.

The first version of the code did not handle `Trace`, the Observatory's word for
"less than 0.05 mm". It would have crashed with `ValueError: could not convert
string to float` the first time it hit one. I added a line to treat `Trace` as
0.0 before converting. I also changed the x-axis from "day number" to a real
date, so the chart shows month names rather than counting from 1 to 243.

## Rejected

An early version of the picture was a line chart, the same shape as the template.
I rejected it because daily rainfall is zero on most days and spikes on a few —
a line draws a continuous curve through those spikes and makes them look like a
slow rise and fall, when what actually happened is that no rain fell for a week
and then 120 mm fell in one day. A bar chart shows that. A line chart would have
hidden it.
I first tried a line chart for the whole year. It buried the wet season in a flat line. Restricting to June–August and using bars made the heavy days visible.