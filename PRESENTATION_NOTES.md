# DCOMP320 Team Presentation & Viva Defense Master Guide

**Course**: DCOMP320 Data Structures and Algorithms  
**Institution**: Limkokwing University of Creative Technology, Sierra Leone  
**Lecturer**: Amandus Benjamin Coker  
**Repository**: https://github.com/Eager1337/Data-Structure  
**Slide Deck**: `project.pptx-slides/presentation.pptx` (26 Slides, Native Morph Transitions, Examiner Q&A)

---

## 1. Presentation Structure & Timing (Total: 10–12 Minutes + 5–8 Minutes Viva)

| Section | Slides | Presenter Role | Focus & Core Takeaways |
| :--- | :--- | :--- | :--- |
| **01. Overview & Architecture** | Slides 1–3 | **Presenter 1** | Project scope, team role blueprint, zero-dependency Python design. |
| **02. Tower of Hanoi** | Slides 4–7 | **Presenter 1** | Recurrence $T(n)=2T(n-1)+1=2^n-1$, Morph state glides, $O(n)$ stack. |
| **03. Binary Tree Traversals** | Slides 8–10 | **Presenter 2** | 31-node perfect tree, 4 traversals, FIFO queue vs DFS stack memory. |
| **04. Huffman Coding** | Slides 11–13 | **Presenter 3** | Greedy min-heap, prefix-free tree building, 96 bits vs 138 (30.4% savings). |
| **05. Graph Optimization** | Slides 14–18 | **Presenter 4** | Dijkstra A→L=20, Figure 2 missing L anomaly, Prim MSTs (35 & 42), SPT $
e$ MST. |
| **06. Testing & Live Demo** | Slides 19–20 | **P4 & Team** | 19 unit tests passing, independent Floyd–Warshall & Kruskal checks, CLI. |
| **07. Viva Defense & Q&A** | Slides 21–26 | **All Members** | Graph edge cases, BFS vs DFS queues, induction proofs, Big-O matrix, closing. |

### Flexible Team Sizing Guide
- **4 Presenters**: 1 section each (P1 Hanoi, P2 Trees, P3 Huffman, P4 Graphs; all on Viva Q&A).
- **3 Presenters**: P1 takes Architecture & Hanoi; P2 takes Trees & Huffman; P3 takes Graphs, Testing & Viva.
- **2 Presenters**: P1 takes Architecture, Hanoi & Trees; P2 takes Huffman, Graphs, Testing & Viva.

---

## 2. Live Terminal Demonstration Cheat Sheet

Keep a terminal open at the project root ready for the panel:

```bash
# 1. Interactive menu demonstration
python main.py

# 2. Automated complete batch demonstration
python main.py --all --disks 3

# 3. Run all 19 automated unit tests (runs in < 0.05s)
python -m unittest discover -s tests -v
```

---

## 3. High-Priority Examiner Viva Questions & Model Answers

### Question 1: Why does Figure 2 not have vertex L, and how did your program handle it?
> **Answer**: In the assignment handout, Figure 2 only contains 10 vertices ($A$ through $J$). Vertex $L$ is absent. Rather than fabricating an arbitrary vertex $L$ with fake edges or crashing, our program programmatically inspects the graph vertex set. If target $L$ is requested on Figure 2, it reports `Not Applicable / Vertex not found`. We also demonstrated the shortest path to vertex $J$ ($A 	o I 	o J$, cost 10) to verify Dijkstra on Figure 2.

### Question 2: Why is a Shortest Path Tree (SPT) from Dijkstra NOT a Minimum Spanning Tree (MST)?
> **Answer**: Dijkstra minimizes the distance from a **single source** to each individual vertex ($O((V+E)\log V)$). Prim minimizes the **total sum of all edge weights** connecting all vertices. Figure 1 provides proof: the MST total weight is 35, but traveling from $A$ to $L$ along the MST costs 24 ($4+3+4+6+4+2+1$). Dijkstra’s shortest route from $A$ to $L$ costs 20, but the total edge weight of the complete SPT rooted at $A$ is 43 ($43 
e 35$).

### Question 3: Why does Level-Order traversal require a FIFO Queue while DFS uses a Stack/Recursion?
> **Answer**: Depth-First Search (pre, in, post) dives down a branch before backtracking (LIFO), which maps to the call stack. Breadth-First Search (Level-Order) must visit nodes in the exact order they were discovered across horizontal depth levels (FIFO). Using a stack would invert exploration into DFS. We used `collections.deque` because it provides $O(1)$ amortized `popleft()`, avoiding the $O(n)$ element-shifting penalty of Python `list.pop(0)`.

### Question 4: What is the recurrence relation and induction proof for Tower of Hanoi?
> **Answer**: $T(n) = 2T(n-1) + 1$, solving to $2^n - 1$.
> - **Base Case**: For $n=1$, $2^1 - 1 = 1$ move.
> - **Inductive Step**: Assume true for $k$: $T(k) = 2^k - 1$. For $k+1$ disks, we move $k$ disks to auxiliary ($T(k)$), move largest disk to target (1 move), then move $k$ disks from auxiliary to target ($T(k)$).
> - **Total**: $T(k+1) = 2(2^k - 1) + 1 = 2^{k+1} - 2 + 1 = 2^{k+1} - 1$. Q.E.D.

### Question 5: Why is Huffman coding greedy-choice optimal, and what does "prefix-free" guarantee?
> **Answer**: David Huffman proved in 1952 that an optimal prefix tree must place the two lowest frequency symbols as siblings at maximum depth. Combining them preserves optimal substructure. Because all symbols reside strictly at **leaf nodes** in the binary tree, no code word can possibly be a prefix of another code word. This guarantees instantaneous, unambiguous decoding without delimiters or backtracking.

### Question 6: Can Dijkstra handle negative edge weights or negative cycles?
> **Answer**: No. Dijkstra assumes that once a vertex is finalized and popped from the min-heap, its shortest path is permanently determined. A negative edge can later reduce that distance, violating the greedy settlement invariant. Negative cycles cause infinite loops. Handling negative weights requires Bellman-Ford ($O(V \cdot E)$) or Johnson’s algorithm.

---

## 4. Asymptotic Big-O Complexity Matrix

| Problem | Algorithm | Time Complexity | Auxiliary Space | Key Data Structure |
| :--- | :--- | :--- | :--- | :--- |
| **Tower of Hanoi** | Recursive Generator | $\Theta(2^n)$ exponential | $O(n)$ call stack | System Call Stack |
| **Binary Tree** | Pre / In / Postorder | $O(V)$ linear | $O(h)$ height ($5$ frames) | Call Stack (LIFO) |
| **Binary Tree** | Level-Order BFS | $O(V)$ linear | $O(w)$ max width ($16$ nodes) | `collections.deque` (FIFO) |
| **Huffman Coding** | Tree Construction | $O(k \log k)$ ($k$ symbols) | $O(k)$ tree nodes | `heapq` Min-Heap |
| **Huffman Coding** | Encode / Decode | $O(n)$ message length | $O(k)$ codebook | Hash Table / Tree |
| **Dijkstra** | Shortest Paths | $O((V+E)\log V)$ | $O(V + E)$ | Adjacency List + Min-Heap |
| **Prim** | Min Spanning Tree | $O((V+E)\log V)$ | $O(V + E)$ | Adjacency List + Min-Heap |
