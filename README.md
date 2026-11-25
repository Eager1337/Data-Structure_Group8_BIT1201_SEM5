# DCOMP320 — Data Structures and Algorithm Final Project

**New to the project? Read [START_HERE.md](START_HERE.md) first.** It explains each
exercise in plain language and shows how to run the program.

## Quick links

- [Beginner walkthrough](START_HERE.md)
- [Read the full report with diagrams](project.report/report-portable.md)
- [Printable report PDF](project.report/report.pdf)
- [Download the complete submission ZIP](https://github.com/Eager1337/Data-Structure/blob/main/submission/DCOMP320_Complete_Project.zip)


Repository: https://github.com/Eager1337/Data-Structure (private).
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



