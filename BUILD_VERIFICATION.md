# Build verification

Verified on 14 November 2026 in Python 3.13.5.

- 19 unittest methods pass, including parameterized cases and subtests.
- Dijkstra matches Floyd–Warshall for every source on both assignment graphs.
- Prim matches Kruskal for every source on both assignment graphs.
- Nine deterministic additional connected graphs pass the independent checks.
- Exhaustive feasible five-symbol code lengths confirm Huffman optimum: 96 bits.
- Hanoi simulation validates all moves, counts and final states for n=0..8.
- Interactive CLI smoke tests pass for every menu option, invalid-input recovery,
  zero disks and invalid batch arguments.
- Python source files compile successfully.
- 13 diagrams and six real execution screenshots are included.
- Printable PDF: 39 A4 pages, with embedded Tahoma and Tahoma Bold.
- All 39 final PDF pages were rendered and visually reviewed. The final version
  removes a one-line overflow and keeps captions with figures.
- Full execution and test transcripts are in `outputs/`.

GitHub repository creation and project upload are complete:
https://github.com/Eager1337/dcomp320-final-project (private).

These are software/build and repository checks, not a claim of university
submission. Actual names/IDs, lecturer invitation, submitting the repository link,
printing and the presentation remain the group's responsibility.