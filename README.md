# DCOMP320 — Data Structures and Algorithm Final Project

**New to the project? Read [START_HERE.md](START_HERE.md) first.** It explains each
exercise in plain language and shows how to run the program.

## Quick links

- [Beginner walkthrough](START_HERE.md)
- [Read the full report with diagrams](project.report/report-portable.md)
- [Printable report PDF](project.report/report.pdf)
- [Editable 14-slide PowerPoint](project.pptx-slides/presentation.pptx)
- [Slide-by-slide speaker notes](project.pptx-slides/speaker-notes.md)
- [Download the complete submission ZIP](https://github.com/Eager1337/dcomp320-final-project/blob/main/submission/DCOMP320_Complete_Project.zip)
- [Presentation preparation](PRESENTATION_NOTES.md)

Repository: https://github.com/Eager1337/dcomp320-final-project (private).
The Python source, report, tests, diagrams, screenshots and submission ZIP have
been uploaded. Your real names/IDs, lecturer collaborator invitation, printing
and individual presentation still need to be completed.

Limkokwing University of Creative Technology, Sierra Leone.
Semester shown in brief: September 2026–February 2027.
Lecturer: Amandus Benjamin Coker.

## Run (Python 3.10 or newer)

No third-party libraries are required for the solutions or tests.

```bash
python main.py                         # interactive menu
python main.py --all --disks 3          # reproducible full demonstration
python main.py --all --disks 4 --json outputs/results-n4.json
python -m unittest discover -s tests -v
```

Use `python3` instead of `python` if that is the name on your computer.
Hanoi supports 0..15 disks in the CLI to avoid accidentally printing huge output.
The algorithm accepts non-negative integers; extremely deep recursion is limited
by Python's recursion limit and exponentially large output.

## Verified results

- Hanoi, n=3: seven legal moves; in general 2^n−1.
- All four traversals match the provided 31-node tree.
- Huffman: a=1000, b=1001, c=101, d=11, e=0; 96 payload bits.
- Figure 1: A–D–H–E–J–L has cost 20; Prim MST total is 35.
- Figure 2: no L exists. A–I–J has cost 10; Prim MST total is 42.
- 19 test methods pass; subtests cover multiple sources, sizes and invalid inputs.
- Independent checks: Floyd–Warshall, Kruskal and exhaustive Huffman code lengths.

## Contents

- `src/algorithms.py`: recursive Hanoi, binary tree traversals, Huffman, graph data,
  Dijkstra, Prim, path reconstruction and matrix generation.
- `main.py`: interactive and batch CLI.
- `tests/test_algorithms.py`: regression, edge-case and independent-oracle tests.
- `outputs/`: complete execution transcript, JSON data and passing test log.
- `project.report/content.md`: editable report source.
- `project.report/report-portable.md`: the same report with relative image links,
  for reading from the extracted ZIP on your own computer.
- `project.report/report.pdf`: printable report; Tahoma 10 pt body, 1.15 spacing,
  justified paragraphs, diagrams, execution screenshots and full code appendices.
- `project.report/diagrams/`: 13 exact, data-driven PNG diagrams.
- `project.report/screenshots/`: six real terminal screenshots.
- `PRESENTATION_NOTES.md`: demo plan, speaking notes and likely viva questions.
- `project.pptx-slides/presentation.pptx`: 14 editable English slides; native
  diagrams, tables, code explanations and speaker notes on every slide.
- `project.pptx-slides/speaker-notes.md`: the same notes as readable Markdown.
- `project.pptx-slides/generate_deck.py`: reproducible PowerPoint builder.
- `SUBMISSION_CHECKLIST.md`: GitHub and hard-copy submission steps.

## Honest handling of the brief

The figures are treated as undirected because no arrowheads are shown.
Figure 2 has vertices A..J, not L; no missing vertex is invented.
Prim solves a minimum spanning tree problem, not the shortest-path problem.
The Huffman input supplies frequencies, not an ordered message: the example
message groups each symbol by its frequency only to demonstrate encoding.
The 96-bit result excludes codebook/header costs; it is not a full compressed
file-format size. At 96 bits, payload occupies 12 packed bytes with no padding.

Names and IDs must be filled in by the real group members before submission.
Use this as a worked implementation and study resource; disclose assistance as
your university requires and ensure every member can explain their own work.
GitHub publication is complete. The lecturer has not been invited and the report
has not been printed; those actions require the group's follow-through.

## Optional report regeneration

The optional scripts need `matplotlib`, `Pillow` and `reportlab` (see
`requirements-report.txt`). Fonts are NOT redistributed in this ZIP.
For the required Tahoma PDF formatting, install your licensed Tahoma fonts and
set `TAHOMA_REGULAR` and `TAHOMA_BOLD` to their paths if the defaults do not exist.

```bash
python project.report/charts.py
python project.report/build_report.py
```

`capture_execution.py` additionally requires Linux, Xvfb, xterm and ImageMagick:

```bash
xvfb-run -a -s '-screen 0 1700x1100x24' python project.report/capture_execution.py
```

The included PDF/PNGs do not require regeneration to view or print.

## Optional PowerPoint regeneration

The included PPTX opens directly in PowerPoint or Google Slides. Its text, shapes,
connectors and tables are editable—not screenshots of slides. Open the Notes pane
for beginner-friendly explanations and complete traversal/distance results.

To rebuild, install `python-pptx` and the Google Slides-safe fonts Poppins, DM Sans
and Roboto Mono. The approved preview is used as slide 7, so keep `preview.pptx`
beside the builder. Fonts are not bundled.

```bash
python -m pip install python-pptx
python project.pptx-slides/generate_deck.py
```

Edit the builder and regenerate, or edit the PPTX directly for your presentation.
Add the real group names and IDs before submission.