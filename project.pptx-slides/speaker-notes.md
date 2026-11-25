# DCOMP320 — Slide-by-Slide Speaker Notes & Viva Defense Guide

**Course**: DCOMP320 Data Structures and Algorithms
**Institution**: Limkokwing University of Creative Technology, Sierra Leone
**Lecturer**: Amandus Benjamin Coker
**Deck**: 26 Slides with Native Morph Transitions, Presenter Roles, and Examiner Viva Q&A

---

## Slide 01: Data Structures & Algorithms, Made Visible.

**Presenter Role**: Presenter 1


--- SPEAKER NOTES ---
PRESENTER ROLE: Presenter 1 (Opening)
ESTIMATED DURATION: 60 seconds

VERBATIM TALKING SCRIPT:
"Good morning/afternoon, Lecturer Coker and members of the panel. Today, our team presents our comprehensive implementation, mathematical analysis, and empirical verification for the DCOMP320 Data Structures and Algorithms final project. We have implemented all four core problem domains into a clean, reproducible Python system backed by 19 automated tests. Each member of our team will walk through their specialized domain, followed by our live defense where we address all examiner questions."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- Formal introduction of DCOMP320 project scope and university context.
- Highlight that all 4 assignment domains are implemented natively without third-party libraries.
- Present team structure and readiness for examiner viva questions.

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: What was the guiding software engineering philosophy behind this implementation?
A: We decoupled algorithmic computation from I/O. Every algorithm in src/algorithms.py returns pure data structures (generators, dataclasses, tuples), enabling complete unit testing and automated validation independent of the CLI.

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---

## Slide 02: Team Roles & Defense Strategy.

**Presenter Role**: Presenter 1


--- SPEAKER NOTES ---
PRESENTER ROLE: Presenter 1
ESTIMATED DURATION: 45 seconds

VERBATIM TALKING SCRIPT:
"To ensure an orderly and professional defense, we have divided the four assignment problems across our presenters. I will cover the architecture and Tower of Hanoi. Presenter 2 will discuss Binary Trees and traversal mechanics. Presenter 3 will explain Huffman coding and bit compression. Presenter 4 will present Graph optimization, including shortest paths, minimum spanning trees, and our critical analysis of the Figure 2 anomaly. Finally, all team members will participate in defending the implementation during the viva."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- Explicitly shows examiner that every team member has mastery over their assigned section.
- Displays clear time management (10-12 mins total presentation).
- Clarifies fallback mapping for 2, 3, or 4 member teams.

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: How did you ensure consistency across different team members code?
A: We enforced strict type annotations, shared data contracts in algorithms.py, unified error handling, and automated unittest suites that everyone ran before committing.

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---

## Slide 03: Four Problems. One Reproducible Architecture.

**Presenter Role**: Presenter 1


--- SPEAKER NOTES ---
PRESENTER ROLE: Presenter 1
ESTIMATED DURATION: 45 seconds

VERBATIM TALKING SCRIPT:
"Our repository is organized around a clean modular architecture. The core algorithms reside in src/algorithms.py with zero third-party dependencies—relying exclusively on standard library modules such as heapq and collections. The main.py entry point provides both an interactive console menu and non-interactive scriptable CLI flags. All outputs are recorded deterministically in JSON format, and every algorithm is verified by 19 automated unit tests."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- Functional separation: src/algorithms.py contains zero print statements.
- CLI options: interactive menu + batch mode (--all, --disks).
- Deterministic JSON output enables automated regression testing.

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: Why did you avoid using popular third-party graph libraries like NetworkX?
A: To demonstrate authentic academic understanding of data structures. Building our own adjacency lists, min-heaps, and tree structures proves foundational competence without relying on black-box abstractions.

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---

## Slide 04: Problem 1: Tower of Hanoi — Recursive Divide & Conquer.

**Presenter Role**: Presenter 1


--- SPEAKER NOTES ---
PRESENTER ROLE: Presenter 1
ESTIMATED DURATION: 60 seconds

VERBATIM TALKING SCRIPT:
"Moving to Problem 1: The Tower of Hanoi is a textbook demonstration of divide-and-conquer recursion. To move n disks from peg A to peg C using peg B as auxiliary, the algorithm breaks the task into three atomic steps: First, recursively move n minus 1 disks from A to B. Second, move the single largest disk directly from A to C. Third, recursively move the n minus 1 disks from B to C. This yields the classical recurrence T(n) equals 2 T(n minus 1) plus 1, resulting in exactly 2 to the n minus 1 moves. For n equals 3, exactly 7 moves are required."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- Mathematical recurrence: T(n) = 2T(n-1) + 1, expanding to 2^n - 1.
- Invariance: Larger disk is never placed on a smaller disk at any point in the call stack.
- Call stack auxiliary memory is O(n), while time complexity is Theta(2^n).

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: How does your Python implementation avoid high recursion overhead?
A: We use Python generators with yield from, allowing each move to be lazily emitted as a tuple without storing the entire sequence of 2^n moves in memory upfront.

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---

## Slide 05: Hanoi State Animation: Move 1 (A → C).

**Presenter Role**: Presenter 1


--- SPEAKER NOTES ---
PRESENTER ROLE: Presenter 1
ESTIMATED DURATION: 45 seconds

VERBATIM TALKING SCRIPT:
"Notice the PowerPoint Morph transition on screen. In Move 1, the smallest disk, Disk 1 in coral, glides seamlessly from Peg A to Peg C. This leaves Disk 2 accessible on Peg A and satisfies all rules. Peg B remains completely free as an auxiliary buffer."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- Morph transition demonstrates the first physical move.
- Disk 1 on Peg C, Disks 2 & 3 remain on Peg A.
- Table shows Step 1 active.

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: Why does disk 1 move to C first instead of B for n=3?
A: Because n=3 is odd. For odd n, the smallest disk must always make its first move directly to the target peg (C) to ensure the largest disk eventually reaches C on move 2^(n-1). For even n, disk 1 starts on the auxiliary peg (B).

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---

## Slide 06: Hanoi State Animation: Moves 2 & 3 (Subproblem n=2 on B).

**Presenter Role**: Presenter 1


--- SPEAKER NOTES ---
PRESENTER ROLE: Presenter 1
ESTIMATED DURATION: 45 seconds

VERBATIM TALKING SCRIPT:
"In Step 2, Disk 2 moves from A to B. Then in Step 3, Disk 1 moves from C onto Disk 2 on Peg B. As you can see, the subproblem of size n minus 1 equals 2 is now completely solved on auxiliary Peg B. This clears Peg A completely except for the largest disk, and leaves target Peg C completely empty and ready."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- Subproblem reduction: Moving n-1=2 disks to Peg B took 2^2 - 1 = 3 moves.
- Largest disk (Disk 3) is now exposed and ready to move to Peg C.
- Peg C is empty.

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: What is the maximum number of recursive calls on the stack at this point?
A: At n=3, the maximum stack depth is exactly 3 frames (proportional to O(n)), corresponding to the depth of the recursive calls for disk 3, disk 2, and disk 1.

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---

## Slide 07: Hanoi State Animation: Move 4 to 7 (Solved State).

**Presenter Role**: Presenter 1


--- SPEAKER NOTES ---
PRESENTER ROLE: Presenter 1
ESTIMATED DURATION: 45 seconds

VERBATIM TALKING SCRIPT:
"In Move 4, Disk 3 moves to Peg C. Then in Moves 5, 6, and 7, the two disks on Peg B are transferred onto Peg C. The entire puzzle is solved in exactly 7 legal moves. Our automated test suite simulates and verifies this sequence for n equals 0 through n equals 8, confirming exact move counts and legal disk ordering at every step. I will now hand over to Presenter 2 for Binary Trees."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- Move 4 places base disk; Moves 5-7 transfer remaining disks.
- Final state verified: C = [3, 2, 1], A = [], B = [].
- Smooth transition to Presenter 2 for Problem 2.

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: What would happen if n=0 or negative disks were passed?
A: n=0 gracefully yields 0 moves without errors. Negative or non-integer inputs trigger strict validation in algorithms.py and raise ValueError/TypeError.

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---

## Slide 08: Problem 2: Perfect Binary Tree Architecture.

**Presenter Role**: Presenter 2


--- SPEAKER NOTES ---
PRESENTER ROLE: Presenter 2
ESTIMATED DURATION: 60 seconds

VERBATIM TALKING SCRIPT:
"Thank you, Presenter 1. Moving to Problem 2: We analyze the complete binary tree specified in the assignment. The tree contains exactly 31 nodes labeled 1 through 31 in level order. Node i has left child 2i and right child 2i plus 1. This forms a perfect binary tree with 5 levels and height 4. Nodes 1 through 15 are internal nodes, while nodes 16 through 31 are all leaves at depth 4. Crucially, as examiners often ask, this tree is full, complete, and perfect—but it is NOT a Binary Search Tree because left children are often larger than their parents."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- Mathematical definition: Node i children = 2i and 2i+1.
- 31 nodes = 2^(h+1) - 1 where height h = 4.
- 16 leaves (51.6% of nodes) at bottom depth.
- NOT a BST: Inorder traversal is not sorted.

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: Why is this tree not a Binary Search Tree (BST)?
A: In a BST, every left descendant must be strictly less than the node, and right descendant greater. Here, node 4 has left child 8 (greater), while node 2 has right child 5 (greater than 4). Numeric labels represent level-order positions, not BST search keys.

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---

## Slide 09: Tree Traversals: Pre, In, Post, and Level-Order.

**Presenter Role**: Presenter 2


--- SPEAKER NOTES ---
PRESENTER ROLE: Presenter 2
ESTIMATED DURATION: 60 seconds

VERBATIM TALKING SCRIPT:
"Here we compare the four canonical tree traversals. In Preorder, we visit the root before subtrees, beginning with 1, 2, 4, 8, 16. In Inorder, we explore the left subtree, then root, then right, starting at leaf 16. In Postorder, both subtrees are processed before the parent, making it ideal for bottom-up tasks like deleting trees or evaluating expression trees. Finally, Level-Order traverses horizontally across each depth level, producing the natural sequence 1 through 31. All four algorithms run in O(n) time, but their spatial memory footprints differ substantially."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- Preorder (Root-L-R), Inorder (L-Root-R), Postorder (L-R-Root), Level-Order (BFS).
- Inorder on a BST produces sorted output; here it proves the tree is not a BST.
- Linear time complexity Theta(n) across all four methods.

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: Why did you avoid using recursive list concatenation (e.g., return left + [root] + right)?
A: Recursive list concatenation copies lists at each frame, leading to O(n^2) worst-case time complexity. We passed a single accumulator list that nodes append to in O(1), preserving strict O(n) linear performance.

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---

## Slide 10: Traversal Memory: FIFO Queue vs DFS Call Stack.

**Presenter Role**: Presenter 2


--- SPEAKER NOTES ---
PRESENTER ROLE: Presenter 2
ESTIMATED DURATION: 60 seconds

VERBATIM TALKING SCRIPT:
"A favorite viva defense question is the memory comparison between DFS and BFS. DFS traversals use the call stack with auxiliary memory proportional to tree height O(h). In our tree of 31 nodes, the maximum stack depth is only 5 frames. Conversely, Level-Order BFS uses a FIFO queue whose size is proportional to maximum tree width O(w). At level 4, our queue must hold up to 16 leaf nodes simultaneously—more than half the tree! Furthermore, we utilized Python collections.deque, which guarantees O(1) popleft, avoiding the O(n) overhead of list.pop(0). I now pass the presentation to Presenter 3 for Huffman Coding."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- DFS auxiliary space = O(h) = O(log n) for balanced trees.
- BFS auxiliary space = O(w) = O(n/2) = O(n) for balanced trees.
- collections.deque is an O(1) double-ended queue implemented in C.

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: What would happen if you used Python built-in list as a queue?
A: Using a Python list with pop(0) causes an O(n) memory shift for every pop, degrading overall BFS traversal from O(n) to O(n^2). collections.deque provides O(1) pointer shifts.

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---

## Slide 11: Problem 3: Huffman Coding & Greedy Optimization.

**Presenter Role**: Presenter 3


--- SPEAKER NOTES ---
PRESENTER ROLE: Presenter 3
ESTIMATED DURATION: 60 seconds

VERBATIM TALKING SCRIPT:
"Thank you, Presenter 2. Moving to Problem 3: Huffman Coding is a greedy algorithm designed for lossless data compression. The input consists of 5 symbols: a with frequency 2, b with 4, c with 8, and d and e each with 16, totaling 46 symbols. Huffman’s key insight is that frequently occurring symbols should be assigned shorter bit codes, while rarer symbols receive longer codes. By maintaining candidate subtrees in a min-heap priority queue, we repeatedly extract the two lowest-frequency trees, merge them, and re-insert their sum until a single prefix tree is formed."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- Input frequencies: a:2, b:4, c:8, d:16, e:16 (sum = 46).
- Greedy choice: Combine two smallest weights at every step.
- Priority queue min-heap enables O(k log k) building time for k symbols.

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: Why does Huffman coding require a min-heap rather than a simple sorted list?
A: A min-heap allows insertion and extraction of minimum elements in O(log k) time. Re-sorting a list on each merge would take O(k log k) per step, resulting in O(k^2 log k) overall time.

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---

## Slide 12: Huffman Tree Construction Step-by-Step.

**Presenter Role**: Presenter 3


--- SPEAKER NOTES ---
PRESENTER ROLE: Presenter 3
ESTIMATED DURATION: 60 seconds

VERBATIM TALKING SCRIPT:
"This diagram shows the complete Huffman prefix tree generated by our program. In step 1, a with frequency 2 and b with 4 are merged into parent node 6. In step 2, node 6 is merged with c of frequency 8 to form node 14. In step 3, node 14 merges with d of frequency 16 to create node 30. Finally, e with 16 and node 30 are merged into root 46. By assigning 0 to left branches and 1 to right branches, we generate instantaneous prefix codes by walking from root to each leaf."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- Step 1: 2 + 4 = 6
- Step 2: 6 + 8 = 14
- Step 3: 14 + 16 = 30
- Step 4: 16 + 30 = 46 (Root)
- Left branch represents 0; right branch represents 1.

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: Is the generated Huffman tree unique?
A: No. While the minimum total weighted path length is unique, tree structure can vary if ties exist, or if left/right branch assignments (0 vs 1) are inverted. Our code uses stable tuple tie-breaking to guarantee deterministic outputs.

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---

## Slide 13: Huffman Codebook & 30.4% Compression Verification.

**Presenter Role**: Presenter 3


--- SPEAKER NOTES ---
PRESENTER ROLE: Presenter 3
ESTIMATED DURATION: 60 seconds

VERBATIM TALKING SCRIPT:
"Here is our finalized codebook. Symbol e receives the single-bit code 0. Symbol d receives 11. Symbol c receives 101. And rare symbols a and b receive 4-bit codes 1000 and 1001. Summing the product of frequencies and bit lengths gives exactly 96 payload bits. A fixed-width encoding for 5 symbols requires 3 bits per symbol, totaling 138 bits. Huffman achieves a 30.43% reduction. Our unit test suite exhaustively validates that encoding and decoding round-trip perfectly without data loss. I now hand over to Presenter 4 for Graph Optimization."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- Symbol e (16 counts) uses 1 bit: 16 bits.
- Symbol d (16 counts) uses 2 bits: 32 bits.
- Symbol c (8 counts) uses 3 bits: 24 bits.
- Symbol b (4 counts) uses 4 bits: 16 bits.
- Symbol a (2 counts) uses 4 bits: 8 bits.
- Total = 96 bits vs 138 fixed = 30.43% savings.

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: What overhead does Huffman coding introduce in practical network storage?
A: In a complete compressed file, the codebook or frequency table must be transmitted alongside the bitstream so the decompressor can reconstruct the tree. For small files, this header overhead can reduce net savings.

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---

## Slide 14: Problem 4: Graph Optimization & Undirected Representation.

**Presenter Role**: Presenter 4


--- SPEAKER NOTES ---
PRESENTER ROLE: Presenter 4
ESTIMATED DURATION: 60 seconds

VERBATIM TALKING SCRIPT:
"Thank you, Presenter 3. Moving to Problem 4: We investigate graph optimization on the two assignment graphs: Figure 1 and Figure 2. We represented both graphs as nested adjacency lists in Python dictionaries, ensuring O(1) edge lookup time and O(V + E) memory efficiency. Because the handout diagrams contain no directional arrowheads, all edges are modeled symmetrically as undirected edges. In our initial graph inspection, we confirmed that Figure 1 contains 12 vertices from A to L. However, we uncovered a critical anomaly in Figure 2: it contains only 10 vertices from A to J—vertex L does not exist."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- Graph representation: dict of dicts for O(1) neighborhood access.
- Symmetric bidirectional modeling because no arrows exist in handout.
- Identification of Figure 2 anomaly: 10 vertices vs 12 vertices.

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: Why choose adjacency lists over an adjacency matrix?
A: Both Figure 1 and Figure 2 are sparse graphs (19 edges on 10-12 vertices). Adjacency lists require O(V + E) space, whereas an adjacency matrix requires O(V^2) space and forces algorithms like Dijkstra to scan absent edges.

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---

## Slide 15: Figure 1: Dijkstra Shortest Path (A to L = 20).

**Presenter Role**: Presenter 4


--- SPEAKER NOTES ---
PRESENTER ROLE: Presenter 4
ESTIMATED DURATION: 60 seconds

VERBATIM TALKING SCRIPT:
"Here is the verified shortest path on Figure 1 from vertex A to vertex L. Our Dijkstra implementation utilizes a binary min-heap to repeatedly settle the nearest unvisited vertex. The optimal path is A to D, D to H, H to E, E to J, and J to L, yielding an exact total distance of 20. Other potential paths, such as routing through vertices B, C, or G, accumulate higher weights. We independently verified this result against an all-pairs Floyd-Warshall implementation, and all distances from source A matched perfectly."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- Shortest path: A -> D -> H -> E -> J -> L with cost 20.
- Edge weights: 4 + 9 + 4 + 2 + 1 = 20.
- Min-heap relaxation runs in O((V + E) log V) time.
- Validated against Floyd-Warshall.

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: Why does Dijkstra require edge weights to be non-negative?
A: Dijkstra operates on a greedy invariant: once a vertex is extracted from the min-heap, its shortest path is assumed finalized. A negative edge could later offer a cheaper detour, invalidating the finalized distance.

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---

## Slide 16: Figure 2: Handout Anomaly & Defensive Architecture.

**Presenter Role**: Presenter 4


--- SPEAKER NOTES ---
PRESENTER ROLE: Presenter 4
ESTIMATED DURATION: 60 seconds

VERBATIM TALKING SCRIPT:
"This is a crucial slide for our viva defense. When analyzing Figure 2, we noticed a printing defect or typo in the original assignment handout: the question asks for shortest path from A to L on Figure 2, but Figure 2 only contains 10 vertices: A through J. Vertex L does not exist. Rather than silently crashing or inventing a fake vertex L, our program incorporates defensive error handling. It detects that L is absent from the vertex set and raises a clean, informative status. To prove Dijkstra works correctly on Figure 2, we demonstrated the shortest path to vertex J, which traverses A to I to J with a cost of 10."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- Academic honesty: Flagged the handout typo rather than faking data.
- Defensive coding: Input validation checks whether source and target exist.
- Farthest node J verified: A -> I -> J costs 10.

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: If an examiner argues that vertex L should have been added, how do you respond?
A: Adding an arbitrary vertex L with invented edge weights would be academically dishonest and ungrounded. Robust software must validate its inputs against the formal graph specification and handle missing targets gracefully.

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---

## Slide 17: Minimum Spanning Trees: Prim vs Kruskal.

**Presenter Role**: Presenter 4


--- SPEAKER NOTES ---
PRESENTER ROLE: Presenter 4
ESTIMATED DURATION: 60 seconds

VERBATIM TALKING SCRIPT:
"Next, we examine Minimum Spanning Trees using Prim’s algorithm. An MST connects all vertices in a connected graph using exactly V minus 1 edges while minimizing the total sum of edge weights. For Figure 1, the MST selects 11 edges with a total weight of 35. For Figure 2, the MST selects 9 edges with a total weight of 42. We independently implemented Kruskal’s algorithm using Disjoint Set Union-Find, and tested Prim starting from every possible vertex. Every single execution converged to the exact same total weights: 35 and 42."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- Prim MST totals: Figure 1 = 35; Figure 2 = 42.
- Number of edges in MST is strictly V - 1 (11 edges for Fig 1, 9 edges for Fig 2).
- Tested from all starting vertices; verified against independent Kruskal implementation.

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: How does Prim’s algorithm compare to Kruskal’s algorithm?
A: Prim grows a single tree vertex-by-vertex from a start node using a min-heap (best for dense graphs). Kruskal sorts all edges globally and adds lightest cycle-free edges using Union-Find (best for sparse graphs). Both produce identical total MST weights.

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---

## Slide 18: Dijkstra vs Prim: Shortest Path ≠ MST.

**Presenter Role**: Presenter 4


--- SPEAKER NOTES ---
PRESENTER ROLE: Presenter 4
ESTIMATED DURATION: 60 seconds

VERBATIM TALKING SCRIPT:
"One of the most frequent examination traps is confusing Shortest Path Trees with Minimum Spanning Trees. Figure 1 provides a mathematical proof that they are fundamentally distinct. Dijkstra finds a path from A to L costing 20, but the total edge weight of the full Shortest Path Tree is 43. In contrast, Prim finds an MST with total weight of only 35. However, if you travel from A to L along that MST, the distance is 24! Dijkstra optimizes locally for each vertex relative to source A. Prim optimizes globally for total network wire length. They solve two different problems."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- Concrete proof from Figure 1: SPT total weight = 43; MST total weight = 35.
- A-to-L path length: Dijkstra = 20; MST path = 24.
- Heap key difference: Dijkstra uses accumulated distance; Prim uses raw edge weight.

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: Under what condition would a Shortest Path Tree happen to be identical to an MST?
A: Only in special graph topologies, such as a simple path graph (line) or star graph where the cheapest global edges naturally coincide with shortest source distances.

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---

## Slide 19: 19 Unit Tests & Algorithmic Cross-Validation.

**Presenter Role**: Presenter 4 & Team


--- SPEAKER NOTES ---
PRESENTER ROLE: Presenter 4 & Team
ESTIMATED DURATION: 45 seconds

VERBATIM TALKING SCRIPT:
"Software reliability requires rigorous validation. Our test suite contains 19 automated unittest methods executed via standard Python unittest discover. Rather than merely comparing against hardcoded values, we implemented independent alternative algorithms for cross-checking: Dijkstra was verified against Floyd-Warshall across all node pairs; Prim was cross-verified against Kruskal; Hanoi was tested with a state simulator; and Huffman was tested with full string round trips. All 19 tests pass in under 0.05 seconds."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- 19 unittest methods pass with zero failures.
- Independent verification: Floyd-Warshall for Dijkstra, Kruskal for Prim.
- Edge cases tested: n=0 disks, disconnected components, malformed strings.

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: Why is independent cross-verification superior to snapshot testing?
A: Snapshot testing only checks if code output has not changed; if the original logic was flawed, the test still passes. Cross-verifying with Floyd-Warshall and Kruskal mathematically proves the output is correct according to different algorithmic principles.

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---

## Slide 20: Interactive CLI & Live Demonstration Guide.

**Presenter Role**: Presenter 1 & Team


--- SPEAKER NOTES ---
PRESENTER ROLE: Presenter 1 & Team
ESTIMATED DURATION: 45 seconds

VERBATIM TALKING SCRIPT:
"Our program features a dual-mode interface. Running python main.py opens an interactive menu allowing the user to select and inspect each problem individually. Running with the --all flag executes the entire pipeline in automated batch mode. If the examination panel requests a live demonstration of any algorithm or test, we can execute it immediately in the terminal."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- main.py supports interactive menu and scriptable batch flags.
- Live demo ready for any panel request.
- Strict exit codes and input sanitization.

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: How does the CLI handle user error, such as entering negative disks or invalid letters?
A: The CLI uses defensive try-except blocks and argument validation. It displays human-readable error messages and re-prompts the user rather than crashing with unhandled tracebacks.

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---

## Slide 21: Comprehensive Viva Defense & Examiner Q&A.

**Presenter Role**: All Presenters


--- SPEAKER NOTES ---
PRESENTER ROLE: All Presenters
ESTIMATED DURATION: 30 seconds

VERBATIM TALKING SCRIPT:
"We now transition to the Viva Defense portion of our presentation. We have prepared detailed, mathematically grounded answers for all expected examiner questions across all four problem domains. Each team member will address questions in their respective specialization."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- Formal transition to examiner defense phase.
- Demonstrates thorough team preparation and confidence.
- Pre-empts common examiner traps.

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: Are all team members prepared to answer questions on any part of the project?
A: Yes. While we partitioned primary presentation roles, every team member studied the complete codebase, mathematical proofs, and test suite.

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---

## Slide 22: Viva Defense: Graph Theory & Discrepancies.

**Presenter Role**: Presenter 4


--- SPEAKER NOTES ---
PRESENTER ROLE: Presenter 4
ESTIMATED DURATION: 60 seconds

VERBATIM TALKING SCRIPT:
"Examiners frequently probe graph edge cases. First, on Figure 2 missing L: we explain our defensive detection. Second, on negative weights: Dijkstra fails because once a node is settled, it is never reconsidered; negative edges require Bellman-Ford with O(V*E) runtime. Third, on disconnected graphs: Dijkstra leaves unreachable nodes at infinity, while Prim raises an error because a spanning tree must cover all vertices. Fourth, on cycles: non-negative cycles are harmless to Dijkstra, while Prim’s visited set prevents cycles by design."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- Q1: Handout typo handled with input validation.
- Q2: Negative edges break greedy settlement; need Bellman-Ford.
- Q3: Disconnected graphs raise error in Prim.
- Q4: Visited sets prevent cycle formation in MST.

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: Could we run Dijkstra with negative weights by adding a constant to make all weights positive?
A: No! Adding a constant k penalizes paths with more edges more heavily than paths with fewer edges, changing which path is shortest. Johnson’s algorithm uses vertex reweighting via Bellman-Ford potentials, which preserves shortest path equivalence.

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---

## Slide 23: Viva Defense: Trees, Queues & Greedy Compression.

**Presenter Role**: Presenter 2 & 3


--- SPEAKER NOTES ---
PRESENTER ROLE: Presenter 2 & 3
ESTIMATED DURATION: 60 seconds

VERBATIM TALKING SCRIPT:
"On tree mechanics: Level-order traversal requires a FIFO queue because breadth-first exploration requires visiting nodes in the exact order they were discovered layer by layer. On Huffman optimality: David Huffman proved in 1952 that an optimal prefix tree must place the two lowest frequency symbols as siblings at maximum depth. Furthermore, because all symbols are stored at leaf nodes, no code can possibly be a prefix of another, enabling instantaneous decoding without delimiters."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- Q5: FIFO queue is essential for BFS level-by-level exploration.
- Q6: Huffman greedy choice property & optimal substructure.
- Q7: Sequential labeling 2i, 2i+1 does not satisfy BST invariant.
- Q8: Leaf-only symbols guarantee prefix-free condition.

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: How does the decoder know when a symbol code ends without delimiters?
A: Because the code is prefix-free, the decoder reads bits sequentially down the tree from the root. The instant it reaches a leaf node, it emits that symbol and resets to the root. There is zero ambiguity.

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---

## Slide 24: Viva Defense: Recurrence Induction & Complexity Matrix.

**Presenter Role**: Presenter 1


--- SPEAKER NOTES ---
PRESENTER ROLE: Presenter 1
ESTIMATED DURATION: 60 seconds

VERBATIM TALKING SCRIPT:
"Here is our formal mathematical proof by induction for the Tower of Hanoi. For base case n equals 1, 2 to the 1 minus 1 equals 1 move, which is correct. Assuming it holds for k, moving k plus 1 disks requires moving k disks to auxiliary, moving the largest disk, then moving the k disks to the target. This gives 2 times 2 to the k minus 1 plus 1, which simplifies to 2 to the k plus 1 minus 1, completing the proof. Beside it, our comprehensive Big-O complexity matrix summarizes the exact asymptotic time and space complexities across all 4 problem implementations."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- Complete mathematical induction proof for T(n) = 2^n - 1.
- Rigorous Big-O summary matrix covering time and auxiliary space for all algorithms.
- Demonstrates theoretical mastery alongside practical code.

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: Can Dijkstra or Prim be improved to O(E + V log V)?
A: Yes! By replacing a standard binary min-heap with a Fibonacci heap, the decrease-key operation drops from O(log V) to O(1) amortized, achieving O(E + V log V). However, binary heaps have lower constant factors and simpler implementations in practice.

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---

## Slide 25: Viva Defense: Real-World Industry Applications.

**Presenter Role**: All Presenters


--- SPEAKER NOTES ---
PRESENTER ROLE: All Presenters
ESTIMATED DURATION: 45 seconds

VERBATIM TALKING SCRIPT:
"Lecturers often ask: Where are these data structures used in modern industry? We have mapped each assignment problem to real-world software engineering: Tower of Hanoi governs grandfather-father-son backup rotation schemes; Binary Trees form the foundation of browser DOM rendering and compiler ASTs; Huffman coding is an integral entropy stage in JPEG, MP3, and Gzip; Dijkstra powers OSPF internet packet routing; and Prim’s MST optimizes physical telecommunication cable and electrical power grids."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- Real-world practical applications demonstrated for all 4 assignment topics.
- Connects academic algorithms to modern engineering systems.

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: How does Gzip combine Huffman with other algorithms?
A: Gzip uses the DEFLATE algorithm, which first applies LZ77 to eliminate duplicate strings by replacing them with distance-length pointers, then applies Huffman coding to compress the resulting literal and distance tokens.

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---

## Slide 26: Project Wrap-Up, Repository Access & Q&A.

**Presenter Role**: Presenter 1 & Team


--- SPEAKER NOTES ---
PRESENTER ROLE: Presenter 1 & Team
ESTIMATED DURATION: 45 seconds

VERBATIM TALKING SCRIPT:
"In conclusion, we have implemented, verified, and analyzed all four assignment problems in a production-ready, zero-dependency Python package. Every calculation—from the 7 Hanoi moves to the 96 Huffman bits and the 35/42 MST totals—has been independently verified with mathematical cross-checks. Our repository is accessible on GitHub at Eager1337/Data-Structure. On behalf of our entire team, thank you for your time, and we now welcome any questions from Lecturer Coker and the examination panel."

KEY TECHNICAL POINTS TO HIGHLIGHT:
- Formal closing thanking the lecturer and panel.
- Final callout to GitHub repository Eager1337/Data-Structure.
- Immediate readiness for examiner Q&A.

ANTICIPATED EXAMINER VIVA QUESTION & MODEL ANSWER:
Q: Final concluding remarks ready.
A: Team stands ready for panel questions.

Implementation References: src/algorithms.py; outputs/results.json; tests/test_algorithms.py


---
