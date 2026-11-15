# Individual presentation and viva preparation

These are preparation notes, not a claim that a presentation has been delivered.
Suggested duration: 8–10 minutes, adjusted to the lecturer's requirement.
Each member should be ready to explain the whole project, not just one function.

## Demonstration plan

1. **Introduction (45 seconds).** Explain the four problems and the data structures:
   recursion/call stack, binary tree, FIFO queue, min-heap and weighted graph.
2. **Hanoi (90 seconds).** Run menu option 1 with n=3. Show how three disks move in
   seven steps and why a larger disk never rests on a smaller one. Explain
   T(n)=2T(n−1)+1, hence 2^n−1.
3. **Traversals (90 seconds).** Run option 2. On the tree diagram, distinguish
   root-left-right, left-root-right, left-right-root and breadth-first order.
   Use the green visitation numbers to explain the first few visits.
4. **Huffman (90 seconds).** Run option 3. Combine 2+4=6, 6+8=14, 14+16=30 and
   16+30=46. Show one valid codebook and compute 8+16+24+32+16=96 bits.
5. **Graphs (2 minutes).** Run option 4. Explain the Figure 1 shortest path
   A–D–H–E–J–L and its cost 4+9+4+2+1=20. Discuss the missing L in Figure 2 and
   demonstrate A–I–J, cost 10. Explain why MST weights 35 and 42 are different
   optimization targets from source-to-destination path costs.
6. **Testing and conclusion (60 seconds).** Run the unit tests. Explain that
   Floyd–Warshall checks Dijkstra, Kruskal checks Prim, legal-state simulation
   checks Hanoi, and encoding/decoding plus exhaustive lengths check Huffman.

## Commands to have ready

```bash
python main.py
python main.py --all --disks 3
python -m unittest discover -s tests -v
```

## Likely questions and concise answers

**What is the Hanoi base case?** Zero disks: no moves. One disk requires a single move.

**How does the stack matter?** Recursive calls suspend their current work while
the smaller subproblem runs. Peg lists also behave as LIFO stacks, using append/pop
at the list end. The demo checks the top disk and target before each move.

**Why is Hanoi exponential?** Two n−1 subproblems and one move occur at every level.
Adding a disk roughly doubles the work: 7 moves for n=3, 15 for n=4.

**Why a queue for level order?** FIFO processes all earlier-discovered nodes first.
Deque append and popleft are approximately O(1); list.pop(0) would shift items.

**Is this a binary search tree?** No. The diagram numbers nodes in level order;
in-order traversal is not a sorted sequence. A binary tree need not satisfy BST ordering.

**Is this tree complete/full/perfect?** All three: every level is full, every internal
node has two children, and leaves are at the same depth. It has 31 nodes, 16 leaves,
15 internal nodes and height 4 edges (five levels).

**Can Huffman codes differ?** Yes. Equal-frequency tie choices or swapping left and
right branches can change bit strings while preserving optimal weighted length.
This code uses sorted symbols, heap insertion serial numbers and left=0/right=1.

**Why can't one code be a prefix of another?** Symbols are assigned only to leaves;
a leaf cannot be an ancestor of another leaf. This makes decoding unambiguous.

**Does 96 bits mean a full compressed file is 12 bytes?** Only the packed payload
is 12 bytes. A real format also needs codebook/header information. Printing the
bits as text is not binary compression and normally uses at least 96 characters.

**Why not give a unique encoded string from frequencies alone?** Frequencies
provide counts but no symbol order. The grouped example message is explicitly
chosen for demonstration; every order with those counts has the same bit length.

**Why does Dijkstra reject negative weights?** Its settlement proof requires that
extending a path cannot reduce its cost. Other algorithms are needed for general
negative-weight shortest-path problems.

**How is Dijkstra different from Prim?** Dijkstra selects the smallest accumulated
distance from the source. Prim selects the cheapest edge crossing from its current
tree to an unvisited vertex. Prim minimizes the tree's total edge weight.

**Can a shortest-path tree fail to be an MST?** Yes. Here the Figure 1 shortest-path
tree has total weight 43, while the MST weighs 35. The MST path from A to L costs
24, whereas the shortest path costs 20.

**Why infinity in the matrix?** It means no direct edge. Zero on the diagonal means
zero cost to the same vertex; a non-edge must not be confused with a zero-weight edge.

**What happens in a disconnected graph?** Dijkstra leaves unreachable distances at
infinity and reconstruction returns an empty path. This Prim implementation raises
a clear error because there is no spanning tree connecting every vertex.

**What about complexity with traces?** Core heap graph work is O(E log V) for simple
connected graphs, but retaining every distance/visited snapshot adds O(V²) time
and storage. The report separates algorithm cost from educational tracing cost.

## Personal reflection preparation

Discuss only your real experience: what you changed, which tests caught a mistake,
how you checked an edge weight, and which concept you can now explain more clearly.
Do not present generated notes as a personal learning history or invent contributions.