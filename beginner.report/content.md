# Start here: understand your project one step at a time

You do **not** need to understand the 39-page report first. This project is four
small programs grouped into one submission. Each program takes a problem and
uses an algorithm—a sequence of instructions—to solve it.

**Your first goal:** run Tower of Hanoi with three disks and explain its rules.
Then move to the other exercises. Do not memorize the code without understanding
what it does; you need to explain it during your individual presentation.

## 1. Which files matter?

| File | What you use it for |
| --- | --- |
| `main.py` | Run the project and choose an exercise from the menu. |
| `src/algorithms.py` | See the actual problem-solving instructions. |
| `project.report/report.pdf` | Read or print the complete assignment report. |
| `project.report/report-portable.md` | Read the report directly on GitHub with working diagrams. |
| `tests/test_algorithms.py` | Check the answers automatically. |
| `PRESENTATION_NOTES.md` | Prepare to explain the project to your lecturer. |

GitHub stores and shares the files. You normally run this project on a computer
with Python installed; simply viewing the repository does not run the program.

## 2. How to run it

1. Download the ZIP from the repository's `submission/` folder and extract it.
2. Open a terminal in the extracted project folder—the folder containing `main.py`.
3. Run:

```bash
python main.py
```

On some computers the command is `python3 main.py`. If neither command works,
Python may not be installed or configured on that computer.

The menu contains:

```text
1 Hanoi | 2 Tree | 3 Huffman | 4 Graphs | 5 All | 0 Exit
```

Choose **1**, then enter **3** when it asks for the number of disks.

## 3. Exercise one: Tower of Hanoi

Imagine three poles called **A**, **B** and **C**. Three disks start on A:
disk 3 is largest, disk 2 is medium, and disk 1 is smallest.

Your goal is to move the whole stack to C. B is a temporary storage pole.

There are three rules:

- Move only one disk at a time.
- Move only the top disk on a pole.
- Never put a bigger disk on top of a smaller disk.

Here is the complete solution for three disks:

| Step | Disk | Move |
| --- | --- | --- |
| 1 | Smallest, disk 1 | A to C |
| 2 | Medium, disk 2 | A to B |
| 3 | Smallest, disk 1 | C to B |
| 4 | Largest, disk 3 | A to C |
| 5 | Smallest, disk 1 | B to A |
| 6 | Medium, disk 2 | B to C |
| 7 | Smallest, disk 1 | A to C |

Try this physically using three pieces of paper of different sizes.

### What does recursion mean here?

Recursion means solving a smaller version of the same problem first.

To move **three** disks:

1. Move the top **two** disks out of the way, onto B.
2. Move the biggest disk to C.
3. Move the **two** smaller disks from B onto C.

Moving two disks follows the same pattern, but with one smaller disk. Moving
zero disks means there is nothing to do. That stopping condition is the **base case**.

The smallest possible number of moves is `2^n - 1`, where `n` is the number of disks:
one disk needs 1 move, two need 3, three need 7, and four need 15.

A **stack** means last in, first out. You can only remove the disk on top—not a
disk buried underneath another one. The program uses lists as the peg stacks.

**Explain it back:** “I move the smaller disks away, move the largest disk, then
move the smaller disks onto it. I repeat the same process for smaller stacks.”

## 4. Exercise two: tree traversals

A tree is a hierarchy of connected nodes. Each numbered circle in the assignment
is a **node**. The top node is the **root**. In a binary tree, a node has at most
two children: a left child and a right child.

A **traversal** is simply a rule for visiting every node.

Use this tiny teaching example first. It is **not** the full 31-node assignment tree:

```text
        1
       / \
      2   3
```

| Traversal | Rule | Result for this tiny example |
| --- | --- | --- |
| Pre-order | Root, then left, then right | 1, 2, 3 |
| In-order | Left, then root, then right | 2, 1, 3 |
| Post-order | Left, then right, then root | 2, 3, 1 |
| Level-order | Top level first, then the next level | 1, 2, 3 |

For a larger tree, “left” and “right” mean complete child subtrees, not just one node.
Your assignment tree contains **31 nodes**. Choose menu option **2** to see its
four complete results. The green `#` labels in the report diagrams show the visit
position; the original numbers inside the circles do not change.

Level-order uses a **queue**: first in, first out, like people waiting in a line.

**Explain it back:** “The tree stays the same. Only the order in which I visit its
nodes changes.”

## 5. Exercise three: Huffman coding

Computers can represent information using bits: **0** and **1**.
Huffman coding gives letters different-length bit codes. Frequently occurring
letters can use fewer bits, saving space across a whole message.

The assignment says:

```text
a appears 2 times
b appears 4 times
c appears 8 times
d appears 16 times
e appears 16 times
```

The program repeatedly combines the two smallest frequencies:

```text
2 + 4 = 6
6 + 8 = 14
14 + 16 = 30
16 + 30 = 46
```

These combinations form a tree. Following left/right branches gives each letter
its binary code. The submitted program uses:

```text
a = 1000
b = 1001
c = 101
d = 11
e = 0
```

For example, the message `ae` becomes `10000`: the code for a (`1000`) followed
by the code for e (`0`). The decoder can separate these codes because none is
the beginning of another complete code. That property is called **prefix-free**.

The full assignment's payload length is:

```text
2×4 + 4×4 + 8×3 + 16×2 + 16×1 = 96 bits
```

The first factor is how many times the letter appears; the second is how many
bits its code uses. Choose menu option **3** to see the steps and decoding check.
The 96-bit figure counts message bits only, not a real file's header or codebook.

**Explain it back:** “I repeatedly combine the two least frequent groups, then
use their tree to produce short, unambiguous binary codes.”

## 6. Exercise four: weighted graphs

Treat each circle as a town. A line is a road. The number on a line is its travel
cost—not necessarily distance in kilometers, because the assignment gives no units.

There are two different questions:

- **Dijkstra:** What is the cheapest route from A to each town?
- **Prim:** What is the cheapest collection of roads that connects every town?

### Dijkstra example from Figure 1

The cheapest route from A to L is:

```text
A -> D -> H -> E -> J -> L
Cost: 4 + 9 + 4 + 2 + 1 = 20
```

Dijkstra keeps the cheapest cost found so far for each town. It chooses the
unsettled town with the lowest cost and checks whether roads from it improve
other towns' costs. Improving a recorded cost is called **relaxation**.

### Prim is a different task

Prim connects all the towns while minimizing the **total cost of the connecting
network**. Its result is called a **minimum spanning tree**, abbreviated MST.
It does not promise the cheapest route between two particular towns.

Your MST totals are **35 for Figure 1** and **42 for Figure 2**.
Do not compare those whole-network totals directly to one route's cost of 20.

Figure 2 contains **no town L**. The report states this instead of inventing one.
Its separate A-to-J example is `A -> I -> J`, costing `9 + 1 = 10`.

Choose menu option **4** to see both graphs' results.

**Explain it back:** “Dijkstra finds cheapest routes from a starting point.
Prim builds the cheapest network connecting all points.”

## 7. How do we know the answers are correct?

Run:

```bash
python -m unittest discover -s tests -v
```

You should see **19 tests** and **OK**. The tests check legal disk moves, tree
orders, encoding and decoding, and graph results. Separate algorithms check
Dijkstra and Prim, so the project is not only checking its answers against itself.

Tests passing means the checked cases behave as expected. It does not mean
you can skip learning how the algorithms work.

## 8. Your next learning steps

1. Run Hanoi with three disks and reproduce the seven moves physically.
2. Explain recursion without reading the code.
3. Learn the three-node tree example, then look at the real tree diagrams.
4. Calculate the Huffman total of 96 bits yourself.
5. Explain the difference between a cheapest route and a cheapest network.
6. Open `PRESENTATION_NOTES.md` and practice the likely lecturer questions.

The completed report still needs your genuine names and student IDs. Follow your
university's rules on disclosing assistance; do not claim work or contributions
you did not actually perform. Use this guide to learn the project, not to pretend
you already understand it.