"""DCOMP320 solutions; Python 3.10+, standard library only.

All algorithms return data so they can be tested independently of the CLI.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import heapq
from itertools import count
from math import inf, isfinite
from typing import Iterator


def hanoi(n: int, source: str = "A", auxiliary: str = "B",
          target: str = "C") -> Iterator[tuple[int, str, str]]:
    """Yield legal moves (disk, from, to), smallest disk numbered 1."""
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError("Number of disks must be a non-negative integer.")
    if len({source, auxiliary, target}) != 3:
        raise ValueError("Three distinct peg names are required.")

    def solve(k: int, start: str, spare: str, end: str):
        if k == 0:
            return
        yield from solve(k - 1, start, end, spare)
        yield k, start, end
        yield from solve(k - 1, spare, start, end)

    return solve(n, source, auxiliary, target)


@dataclass
class TreeNode:
    value: int
    left: TreeNode | None = None
    right: TreeNode | None = None


def assignment_tree() -> TreeNode:
    """Reproduce the exact perfect binary tree 1..31 in the handout."""
    nodes = {i: TreeNode(i) for i in range(1, 32)}
    for i in range(1, 16):
        nodes[i].left, nodes[i].right = nodes[2 * i], nodes[2 * i + 1]
    return nodes[1]


def preorder(root: TreeNode | None) -> list[int]:
    result = []
    def visit(node):
        if node is not None:
            result.append(node.value)
            visit(node.left)
            visit(node.right)
    visit(root)
    return result


def inorder(root: TreeNode | None) -> list[int]:
    result = []
    def visit(node):
        if node is not None:
            visit(node.left)
            result.append(node.value)
            visit(node.right)
    visit(root)
    return result


def postorder(root: TreeNode | None) -> list[int]:
    result = []
    def visit(node):
        if node is not None:
            visit(node.left)
            visit(node.right)
            result.append(node.value)
    visit(root)
    return result


def levelorder(root: TreeNode | None) -> list[int]:
    if root is None:
        return []
    queue, result = deque([root]), []
    while queue:
        node = queue.popleft()
        result.append(node.value)
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)
    return result


@dataclass
class HuffmanNode:
    frequency: int
    symbol: str | None = None
    left: HuffmanNode | None = None
    right: HuffmanNode | None = None


def huffman(frequencies: dict[str, int]):
    """Return (root, codes, merges) with stable, documented tie breaking.

    Leaves enter in sorted symbol order; new parents follow existing nodes
    when their weights tie. The first popped child gets bit 0.
    """
    if not frequencies:
        raise ValueError("At least one symbol is required.")
    if any(not isinstance(s, str) or len(s) != 1 for s in frequencies):
        raise ValueError("Symbols must be single characters.")
    if any(isinstance(f, bool) or not isinstance(f, int) or f <= 0
           for f in frequencies.values()):
        raise ValueError("Frequencies must be positive integers.")
    serial = count()
    heap = [(frequencies[s], next(serial), HuffmanNode(frequencies[s], s), s)
            for s in sorted(frequencies)]
    heapq.heapify(heap)
    merges = []
    while len(heap) > 1:
        f1, _, left, label1 = heapq.heappop(heap)
        f2, _, right, label2 = heapq.heappop(heap)
        parent = HuffmanNode(f1 + f2, left=left, right=right)
        label = "(" + label1 + "+" + label2 + ")"
        merges.append((label1, f1, label2, f2, f1 + f2))
        heapq.heappush(heap, (f1 + f2, next(serial), parent, label))
    root = heap[0][2]
    codes = {}

    def walk(node: HuffmanNode, prefix: str):
        if node.symbol is not None:
            codes[node.symbol] = prefix or "0"
        else:
            walk(node.left, prefix + "0")
            walk(node.right, prefix + "1")

    walk(root, "")
    return root, codes, merges


def encode(text: str, codes: dict[str, str]) -> str:
    if any(symbol not in codes for symbol in text):
        raise ValueError("Text contains a symbol absent from the codebook.")
    return "".join(codes[s] for s in text)


def decode(bits: str, root: HuffmanNode) -> str:
    if any(bit not in "01" for bit in bits):
        raise ValueError("Encoded text must contain only 0 and 1.")
    if root.symbol is not None:
        if "1" in bits:
            raise ValueError("Single-symbol code is 0.")
        return root.symbol * len(bits)
    result, node = [], root
    for bit in bits:
        node = node.left if bit == "0" else node.right
        if node.symbol is not None:
            result.append(node.symbol)
            node = root
    if node is not root:
        raise ValueError("Incomplete Huffman code at end of input.")
    return "".join(result)


Graph = dict[str, dict[str, int | float]]


def make_graph(edges: list[tuple[str, str, int]],
               vertices: list[str] | None = None) -> Graph:
    graph = {v: {} for v in (vertices or [])}
    for u, v, weight in edges:
        if u == v or v in graph.get(u, {}):
            raise ValueError("Self loops and duplicate edges are not allowed.")
        graph.setdefault(u, {})[v] = weight
        graph.setdefault(v, {})[u] = weight
    validate_graph(graph)
    return dict(sorted(graph.items()))


def validate_graph(graph: Graph):
    """This project uses simple undirected graphs, nonnegative finite weights."""
    for u, neighbors in graph.items():
        for v, weight in neighbors.items():
            if (isinstance(weight, bool) or not isinstance(weight, (int, float))
                    or not isfinite(weight) or weight < 0):
                raise ValueError("Weights must be finite, non-negative numbers.")
            if u == v or v not in graph or graph[v].get(u) != weight:
                raise ValueError("Graph must be simple and undirected.")


FIGURE_1_EDGES = [
    ("A", "D", 4), ("B", "D", 8), ("B", "C", 2),
    ("C", "E", 5), ("C", "J", 10), ("D", "F", 6),
    ("D", "G", 3), ("D", "H", 9), ("D", "K", 6),
    ("F", "G", 1), ("F", "K", 7), ("G", "K", 4),
    ("H", "K", 6), ("H", "E", 4), ("H", "I", 3),
    ("E", "I", 9), ("E", "J", 2), ("I", "J", 7),
    ("J", "L", 1),
]
FIGURE_2_EDGES = [
    ("A", "B", 2), ("A", "D", 15), ("A", "I", 9),
    ("B", "C", 3), ("B", "D", 5), ("B", "E", 17),
    ("C", "E", 12), ("C", "F", 18), ("D", "E", 4),
    ("D", "G", 6), ("E", "F", 13), ("E", "G", 11),
    ("E", "H", 7), ("F", "H", 14), ("G", "H", 19),
    ("G", "I", 8), ("G", "J", 1), ("H", "J", 16),
    ("I", "J", 1),
]


def assignment_graphs() -> dict[str, Graph]:
    return {"Figure 1": make_graph(FIGURE_1_EDGES),
            "Figure 2": make_graph(FIGURE_2_EDGES)}


def adjacency_matrix(graph: Graph):
    vertices = sorted(graph)
    return vertices, [[0 if u == v else graph[u].get(v, inf)
                       for v in vertices] for u in vertices]


def dijkstra(graph: Graph, source: str):
    """Return distances, predecessors and snapshots after each settlement."""
    validate_graph(graph)
    if source not in graph:
        raise ValueError("Source vertex is absent from graph.")
    distances = dict.fromkeys(graph, inf)
    distances[source] = 0
    previous = dict.fromkeys(graph, None)
    heap, settled, trace = [(0, source)], set(), []
    while heap:
        distance, u = heapq.heappop(heap)
        if u in settled:
            continue
        settled.add(u)
        updates = []
        for v, weight in sorted(graph[u].items()):
            candidate = distance + weight
            if v not in settled and candidate < distances[v]:
                old = distances[v]
                distances[v], previous[v] = candidate, u
                heapq.heappush(heap, (candidate, v))
                updates.append((v, old, candidate, u))
        trace.append({"vertex": u, "distance": distance,
                      "updates": updates, "distances": distances.copy()})
    return distances, previous, trace


def reconstruct_path(previous: dict, source: str, target: str) -> list[str]:
    if source not in previous or target not in previous:
        raise ValueError("Requested vertex is absent from graph.")
    result, visited, current = [], set(), target
    while current is not None:
        if current in visited:
            raise ValueError("Predecessor map contains a cycle.")
        visited.add(current)
        result.append(current)
        if current == source:
            return list(reversed(result))
        current = previous[current]
    return []


def prim(graph: Graph, source: str = "A"):
    """Return (chosen edges, total, trace) for a connected graph's MST."""
    validate_graph(graph)
    if source not in graph:
        raise ValueError("Source vertex is absent from graph.")
    visited, heap, edges, trace, total = {source}, [], [], [], 0
    vertex_order = sorted(graph)

    def push_edges(u):
        for v, weight in sorted(graph[u].items()):
            if v not in visited:
                heapq.heappush(heap, (weight, u, v))

    push_edges(source)
    while heap and len(visited) < len(graph):
        weight, u, v = heapq.heappop(heap)
        if v in visited:
            continue
        visited.add(v)
        edges.append((u, v, weight))
        total += weight
        trace.append({"edge": (u, v, weight), "total": total,
                      "visited": [x for x in vertex_order if x in visited]})
        push_edges(v)
    if len(visited) != len(graph):
        raise ValueError("Graph is disconnected; a spanning tree does not exist.")
    return edges, total, trace