 # DCOMP320 — Editable presentation outline

## Audience and purpose
Lecturer and classmates; an English, beginner-friendly explanation of the four assignment problems, with reproducible Python results and viva-ready speaker notes. Target 8–10 minutes. Exactly 14 slides.

## Narrative
One runnable program connects recursion, trees, greedy compression and graph optimization. Explain each idea visually, connect it to the implementation, then show independently verified results. Distinguish shortest paths from minimum spanning trees and explicitly acknowledge the missing L in Figure 2.

## Selected visual reference and locked theme
Use only the look of the five user-supplied E-learning references; none of their wording, branding or photographs. White 16:9 canvas, heavy black left-aligned headings, generous whitespace, asymmetric diagram-led layouts, rounded mint/yellow callout panels and a small coral-circle / purple-triangle / mint-square / yellow-circle motif. Top navigation becomes the actual four project sections. Relevant editable algorithm diagrams replace the stock-photo regions.

- Fonts: installed Google Slides-safe Poppins (bold titles) and DM Sans (body); Roboto Mono for code.
- Palette: black #111111; body gray #505050; mint #A6D8C8; yellow #F4CD59; purple #8B78CD; coral #F16F54; pale gray #F5F6F5.
- Hierarchy: titles 34–42 pt; body 18–22 pt; diagram labels 16–20 pt; captions/navigation 10–12 pt.
- Native text, shapes, connectors, tables and charts. No rasterized text or charts.
- Layout families: split-title/diagram, two-column code/result, comparative diagrams, full-width results/tests, editorial closing.
- Real student names/IDs remain unfilled. Do not invent contributions or personal reflections. Generated preparation material must be disclosed in notes.

## Slide sequence — exactly 14
1. **Data structures & algorithms, made visible.** Course/university, project overview; visual motif and four structures. Notes introduce scope and blank student identity fields.
2. **Four problems. One reproducible program.** Map Hanoi → stack, traversals → tree/queue, Huffman → heap, routes/MST → weighted graph. Show `main.py`, `src/algorithms.py`, tests and outputs.
3. **Three disks need seven legal moves.** Editable Hanoi states and seven-move sequence; `2^n − 1`. Explain legal moves, smallest disk = 1.
4. **Recursion solves a smaller version first.** Actual Hanoi implementation excerpt and call flow; zero-disk base case, validation, O(n) stack. Notes distinguish Θ(2^n) move generation from nested generator dispatch overhead.
5. **A perfect binary tree has five levels.** Editable 31-node tree, children `2i`/`2i+1`, 16 leaves and height four edges. Explain why it is not a BST.
6. **Traversal changes order—not the tree.** Four visit-order rules with actual traversal sequences; recursive append versus FIFO `deque`. Short implementation excerpt; full sequences and complexity in notes.
7. **Huffman makes frequent symbols cheaper.** Representative preview: native weighted tree, stable left=0/right=1 branches, frequencies and exact 96-bit result; fixed-width baseline 138 bits.
8. **A min-heap builds a prefix-free code.** Actual heap merge/code assignment excerpts; native codebook table; encode/decode demonstration. Notes show ties, merge sum, 12-byte payload caveat and unspecified message order.
9. **Figure 1: the shortest A-to-L route costs 20.** Editable full 12-vertex/19-edge graph with path A–D–H–E–J–L highlighted; sum 4+9+4+2+1. Notes include all-source-A distances.
10. **Figure 2 has no vertex L.** Editable full 10-vertex/19-edge graph; A-to-L is not applicable. Separately labeled A–I–J example costs 10; distances in notes.
11. **Shortest route ≠ cheapest spanning tree.** Native selected-edge MST diagrams for both graphs, weights 35 and 42. Figure 1 shortest-path-tree weight 43 vs MST 35; MST A-to-L path costs 24.
12. **Dijkstra and Prim use the heap differently.** Side-by-side real code excerpts and selection criteria. Graph representation: undirected edges, adjacency list/matrix, non-edge infinity. Core O((V+E) log V); traces add O(V²).
13. **19 test methods pass—with independent checks.** Native verification matrix: legal Hanoi simulation, traversal sequences, encode/decode/exhaustive Huffman, Floyd–Warshall vs Dijkstra, Kruskal vs Prim; deterministic random graphs and CLI checks. Show exact test command.
14. **Run it. Explain it. Verify it.** Three reproducible commands and key takeaways; GitHub link, report/source references, submission reminders. Notes include academic-integrity disclosure, Week 4 only and no invented collaborator invitation.

## Preview checkpoint
Build only slide 7 as `preview.pptx`. Run deterministic precheck, render with the provided converter, inspect, deliver, then wait for approval before building the full 14-slide deck or uploading it to GitHub.

## Evidence/source of truth
`src/algorithms.py`, `outputs/results.json`, `outputs/execution.txt`, `tests/test_algorithms.py`, `project.report/report-portable.md`, `PRESENTATION_NOTES.md` and the supplied assignment scan. External implementation references: Python heapq/deque documentation and Princeton shortest-path/MST material, already included in the project report.