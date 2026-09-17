# Process

## Tools

- **DeepSeek** — to adapt the template's `plot.py` from daily temperature to
  daily rainfall: rename the data file, keep only 2026, handle `Trace`, switch
  from a line chart to a bar chart, and then iterate on the look (background
  colour, colour-coding by intensity, where to put the labels).
- **uv** — to run both scripts without installing anything globally.

## Kept

The template's `rows()` function. It reads the CSV, keeps only the lines that
start with a year, and throws away the two title lines at the top and the legend
at the bottom. It worked on my file exactly as it was written, so I did not
touch it. That is the one part of the template I would have written the same way
myself.

## Rejected

Two things, at different stages.

First, a **line chart**, the same shape as the template. Daily rainfall is zero
on most days and spikes on a few — a line draws a continuous curve through those
spikes and makes them look like a slow rise and fall, when what actually happened
is that no rain fell for a week and then 120 mm fell in one day. A bar chart
shows that. A line chart would have hidden it.

Second, **the whole year**. The first bar chart showed January to August and the
rainy months were buried in a long stretch of empty ones. Restricting the picture
to June–August made the wet season the whole point of the image instead of a
detail in the middle of it.

## What I had to correct

- The first version of the code did not handle `Trace`, the Observatory's word
  for "less than 0.05 mm". It would have crashed with `ValueError: could not
  convert string to float` the first time it hit one. I added a line to treat
  `Trace` as 0.0 before converting.
- The x-axis originally counted days from 1 to 243. I changed it to real dates
  so the chart shows month and day names.
- The first labelled version put the date *and* the rainfall value next to every
  big bar. With four big bars in June alone, the labels overlapped and it was
  impossible to tell which bar each label belonged to. I cut the labels down to
  the date only, moved them to the top of each bar, and staggered them left and
  right so neighbouring labels never touch.