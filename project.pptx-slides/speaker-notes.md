# DCOMP320 — slide-by-slide speaker notes

## 1. Data structures & algorithms, made visible.

Introduce the four assignment problems and explain that the program is a runnable Python implementation. Target total duration 8–10 minutes. Student names and IDs are intentionally not fabricated; add the real group details before submission. The printed brief gives the deadline as Week 4 only.
Sources: Supplied DCOMP320 assignment; README.md
Preparation material includes generated assistance. Verify understanding and disclose assistance as course policy requires. No personal contribution, student identity or university submission is claimed.

## 2. Four problems. One reproducible program.

Point to main.py as the entry point. Algorithms return data instead of printing directly, which allows tests to verify them independently of the CLI. The JSON output keeps complete results and traces. No third-party dependencies are needed for the algorithms or their tests.
Sources: src/algorithms.py; outputs/results.json; tests/test_algorithms.py
Preparation material includes generated assistance. Verify understanding and disclose assistance as course policy requires. No personal contribution, student identity or university submission is claimed.

## 3. Three disks need seven legal moves.

Explain the rules: move one top disk at a time and never place a larger disk on a smaller disk. Lists store pegs bottom-to-top and disk 1 is the smallest. Read the seven displayed moves. The CLI simulates and validates the moves. The test suite checks legal simulation, count and final state for n=0 through n=8. The algorithm also accepts n=0 and distinct custom peg names.
Sources: src/algorithms.py; outputs/results.json; tests/test_algorithms.py
Preparation material includes generated assistance. Verify understanding and disclose assistance as course policy requires. No personal contribution, student identity or university submission is claimed.

## 4. Recursion solves a smaller version first.

Read the exact nested solve function in hanoi. A zero-disk problem yields no moves. yield from delegates to smaller generators; yield emits the move of disk k. Core recursive move-generation work is Θ(2^n), with O(n) call stack. The nested Python yield-from dispatch can add a factor up to n, so do not describe measured traced Python runtime as only move count. The wrapper rejects negative/noninteger/bool n and repeated peg names. CLI limits disks to 0..15 to control output.
Sources: src/algorithms.py; outputs/results.json; tests/test_algorithms.py
Preparation material includes generated assistance. Verify understanding and disclose assistance as course policy requires. No personal contribution, student identity or university submission is claimed.

## 5. A perfect binary tree has five levels.

This is the exact assignment tree: node labels 1 to 31 in level order. Internal nodes 1 to 15 have children 2i and 2i+1. All leaves are at depth four: five levels, height four edges, 16 leaves and 15 internal nodes. It is perfect, full and complete, but not a binary search tree. A left child can have a larger numeric label than its parent; inorder is therefore not sorted. assignment_tree constructs one object per node and links them.
Sources: src/algorithms.py; outputs/results.json; tests/test_algorithms.py
Preparation material includes generated assistance. Verify understanding and disclose assistance as course policy requires. No personal contribution, student identity or university submission is claimed.

## 6. Traversal changes order—not the tree.

Compare where root is visited relative to its subtrees. Each recursive traversal appends into one shared result list, avoiding costly repeated list concatenation. Level order uses collections.deque, a FIFO queue, with approximately O(1) append and popleft. All traversals take O(n) work and O(n) returned-list storage. Recursive auxiliary stack is O(h); the queue can store O(width) nodes. Complete actual sequences:
Preorder: 1, 2, 4, 8, 16, 17, 9, 18, 19, 5, 10, 20, 21, 11, 22, 23, 3, 6, 12, 24, 25, 13, 26, 27, 7, 14, 28, 29, 15, 30, 31
Inorder: 16, 8, 17, 4, 18, 9, 19, 2, 20, 10, 21, 5, 22, 11, 23, 1, 24, 12, 25, 6, 26, 13, 27, 3, 28, 14, 29, 7, 30, 15, 31
Postorder: 16, 17, 8, 18, 19, 9, 4, 20, 21, 10, 22, 23, 11, 5, 2, 24, 25, 12, 26, 27, 13, 6, 28, 29, 14, 30, 31, 15, 7, 3, 1
Level order: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31
Sources: src/algorithms.py; outputs/results.json; tests/test_algorithms.py
Preparation material includes generated assistance. Verify understanding and disclose assistance as course policy requires. No personal contribution, student identity or university submission is claimed.

## 7. Huffman makes frequent symbols cheaper.

Slide 7 of the planned 14-slide DCOMP320 presentation. Suggested speaking time: 45 seconds.
Huffman assigns shorter codes to more frequent symbols. Begin with a=2, b=4, c=8, d=16, e=16. A min-heap repeatedly removes the two smallest weights: 2+4=6, 6+8=14, 14+16=30, 16+30=46. The implementation uses sorted symbols and an insertion serial to resolve ties. Left branches are 0; right branches are 1. Read each leaf path: e=0, d=11, c=101, a=1000, b=1001. The weighted length is 2×4 + 4×4 + 8×3 + 16×2 + 16×1 = 96 bits. The merge sum is also 6+14+30+46=96. Five symbols need three bits in a fixed-width code: 46×3=138. Savings: 42 bits, about 30.4%. These are payload bits only, not a complete compressed file. Frequencies do not specify message order. Alternative tie decisions may give different but equally optimal codes.
Source: src/algorithms.py huffman; outputs/results.json; project report. This deck and preparation notes are generated assistance; students must verify, understand and disclose use as required by course policy. No student contribution or personal reflection is being claimed.

## 8. A min-heap builds a prefix-free code.

Symbols are leaves, so no symbol code can be a prefix of another. Read the heap code: pop two minima, form a parent, push it back. Code walking appends 0 to the left and 1 to the right; single-symbol input gets code 0. The project implements encode and decode with validation. Sorted leaf symbols and a serial insertion key produce stable equal-frequency ties. The two symbols a and b encode as 1000 + 1001 and round-trip to ab. This short message is an illustration, not the 46-symbol frequency input. The full grouped demonstration has 96 payload bits (12 packed bytes, no padding), excluding headers. Huffman construction uses O(k log k) heap work for k distinct symbols; message encoding and decoding are proportional to processed symbols/bits.
Sources: src/algorithms.py; outputs/results.json; tests/test_algorithms.py
Preparation material includes generated assistance. Verify understanding and disclose assistance as course policy requires. No personal contribution, student identity or university submission is claimed.

## 9. Figure 1: the shortest A-to-L route costs 20.

Figure 1: each drawn edge is undirected because the handout shows no arrowheads. The graph contains exactly 12 vertices and 19 edges. Dijkstra yields A-D-H-E-J-L with cost 20. Purple edges mark that route, not an MST. Distances from A: A=0, B=12, C=14, D=4, E=17, F=8, G=7, H=13, I=16, J=19, K=10, L=20. Dijkstra maintains tentative distances and predecessor pointers. Nonnegative weights justify finalizing the smallest unsettled distance. Complete settlement/update traces are in outputs/results.json.
Sources: src/algorithms.py; outputs/results.json; tests/test_algorithms.py
Preparation material includes generated assistance. Verify understanding and disclose assistance as course policy requires. No personal contribution, student identity or university submission is claimed.

## 10. Figure 2 has no vertex L.

Figure 2: each drawn edge is undirected because the handout shows no arrowheads. The graph contains exactly 10 vertices and 19 edges. There is no L in the input. A-to-L is not applicable, not a merely unreachable target. Do not invent L or silently replace it. A-I-J with cost 10 is a separately labelled demonstration. Distances from A: A=0, B=2, C=5, D=7, E=11, F=23, G=11, H=18, I=9, J=10. Dijkstra maintains tentative distances and predecessor pointers. Nonnegative weights justify finalizing the smallest unsettled distance. Complete settlement/update traces are in outputs/results.json.
Sources: src/algorithms.py; outputs/results.json; tests/test_algorithms.py
Preparation material includes generated assistance. Verify understanding and disclose assistance as course policy requires. No personal contribution, student identity or university submission is claimed.

## 11. Shortest route ≠ cheapest spanning tree.

Prim minimizes total edge weight while connecting every vertex without cycles. Only the chosen MST edges are drawn here. Figure 1 selected edges: [('A', 'D', 4), ('D', 'G', 3), ('G', 'F', 1), ('G', 'K', 4), ('K', 'H', 6), ('H', 'I', 3), ('H', 'E', 4), ('E', 'J', 2), ('J', 'L', 1), ('E', 'C', 5), ('C', 'B', 2)]. Figure 2 selected edges: [('A', 'B', 2), ('B', 'C', 3), ('B', 'D', 5), ('D', 'E', 4), ('D', 'G', 6), ('G', 'J', 1), ('J', 'I', 1), ('E', 'H', 7), ('E', 'F', 13)]. Totals are 35 and 42. A shortest-path tree rooted at A has total edge weight 43 in Figure 1, not 35. The MST path A-D-G-K-H-E-J-L costs 4+3+4+6+4+2+1=24, while the shortest route costs 20. This is why Prim must not be reported as a shortest-path algorithm. Independent Kruskal tests confirm both MST totals from all starts.
Sources: src/algorithms.py; outputs/results.json; tests/test_algorithms.py
Preparation material includes generated assistance. Verify understanding and disclose assistance as course policy requires. No personal contribution, student identity or university submission is claimed.

## 12. Dijkstra and Prim use the heap differently.

The Dijkstra display reproduces the core relaxation logic with a line-wrapped condition; old-distance trace logging is omitted. distance is an accumulated source-to-u cost. Relaxation tries distance + weight and pushes an improved candidate. In Prim the heap key is one edge weight; edges leading to already-visited vertices are skipped. The graph is a dict of neighbor dicts; make_graph adds both directions and validates symmetry, finite nonnegative weights and no duplicates/self-loops. An adjacency matrix uses zero on the diagonal and infinity for absent edges; exported JSON uses null for infinity. Core heap work is O((V+E) log V) for these simple graphs; heap/list storage depends on edges and vertices. Copying distances and recording visited snapshots adds O(V²) time/storage. Negative weights are rejected for this project; disconnected Prim raises an error.
Sources: src/algorithms.py; outputs/results.json; tests/test_algorithms.py
Preparation material includes generated assistance. Verify understanding and disclose assistance as course policy requires. No personal contribution, student identity or university submission is claimed.

## 13. 19 test methods pass—with independent checks.

19 unittest methods pass, with additional parameterized subtests. The builder does not fabricate a terminal screenshot; the actual output logs are in outputs/test-results.txt and execution screenshots in project.report/screenshots. Graph tests compare against independent Floyd–Warshall and Kruskal implementations, not only hard-coded expectations. Random connected graphs cover sizes 2 through 10 with seed 320. Huffman exhaustive feasible five-symbol code-length combinations confirm minimum 96 bits. Invalid input, empty/single/skew trees, disconnected/zero-weight/single-vertex graphs and malformed Huffman streams are checked. CLI smoke checks include all menu choices, invalid-input recovery, zero disks and --disks -1 returning exit code 2. Run the displayed command live if time permits.
Sources: src/algorithms.py; outputs/results.json; tests/test_algorithms.py
Preparation material includes generated assistance. Verify understanding and disclose assistance as course policy requires. No personal contribution, student identity or university submission is claimed.

## 14. Run it. Explain it. Verify it.

Close with the key results and invite questions. The repository is private, so lecturer access needs an invitation to a verified GitHub username. The report is 39 A4 pages with the required Tahoma body formatting; print and submit as instructed. Deadline is Week 4 in the brief—no exact date is specified. Add real student names/IDs, disclose assistance as required, and do not claim invented group contributions. The beginner walkthrough explains every concept and command; the final editable deck, builder and complete ZIP are included. Reference URLs: https://docs.python.org/3/library/heapq.html ; https://docs.python.org/3/library/collections.html ; https://algs4.cs.princeton.edu/44sp/ ; https://algs4.cs.princeton.edu/43mst/ .
Sources: README.md; START_HERE.md; SUBMISSION_CHECKLIST.md; supplied assignment; project.report/report-portable.md
Preparation material includes generated assistance. Verify understanding and disclose assistance as course policy requires. No personal contribution, student identity or university submission is claimed.