# Process

## Tools

- **DeepSeek** — to adapt the template's `plot.py` from daily temperature to
  daily rainfall, read the Hong Kong Observatory CSV, filter the data to
  June–August 2026, and help me experiment with different ways of turning
  rainfall values into visual forms.
- **Matplotlib** — to generate the final image from the rainfall data.
- **uv** — to run the Python script without installing packages globally.

## Kept

The template's basic CSV-reading structure. It gave me a starting point for
reading the Hong Kong Observatory data and selecting the period I wanted to
visualise. I kept the general idea of reading the data with Python, but
changed the visualisation process substantially.

I also kept the idea of treating each day as an individual unit. Instead of
turning each day into a conventional bar, I used each day as part of a
continuous field of rain.

## Rejected

My first version followed the template and used a **bar chart** to show daily
rainfall. It represented the data clearly, but the result still felt too much
like a conventional data visualisation.

After seeing the other works presented in the lecture this morning, I started
to rethink the visual direction of my project. I realised that the data did
not necessarily have to be presented as a conventional chart. I wanted to
treat the numbers more like visual material and make the image feel closer to
an artwork.

I experimented with several different visual forms, including separate rain
lines, layered rainfall shapes, and more irregular rain patterns. Some
versions became too similar to a normal chart, while others became too dense
or visually unclear.

I eventually chose a **continuous rain field**. Instead of showing rainfall
as separate bars, I translated the amount of rain into the density, thickness,
and opacity of vertical rain strokes. This allowed the data to become part of
the visual structure while still preserving the relationship between rainfall
and the image.

## What I had to correct

- The original CSV contains two title lines before the actual column headers.
  I had to skip these lines before using `csv.DictReader`.
- The rainfall data contains values such as `***`, which cannot be converted
  directly into a number. I handled these values before converting the
  rainfall measurements to `float`.
- The original visualisation used a conventional chart structure. I changed
  the visual mapping so that higher rainfall produces a denser and slightly
  heavier rain field.
- I experimented with several versions of the rain field. Some were too
  blurry, some were too random, and some were too similar to a conventional
  chart. I gradually simplified the visual language and kept the continuous
  rain curtain as the main structure.
- I added a small amount of supporting information, including the three
  highest rainfall events and summary statistics, while keeping these
  elements secondary to the rain field.