"""Independent oracles: Floyd-Warshall for paths, Kruskal for MSTs."""
import random
import unittest
from itertools import product
from math import inf
from src.algorithms import *


def floyd_warshall(graph):
    vs, matrix = adjacency_matrix(graph)
    for k in range(len(vs)):
        for i in range(len(vs)):
            for j in range(len(vs)):
                matrix[i][j] = min(matrix[i][j], matrix[i][k] + matrix[k][j])
    return {u: dict(zip(vs, row)) for u, row in zip(vs, matrix)}


def kruskal_weight(graph):
    parent = {v: v for v in graph}
    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v
    total, accepted = 0, 0
    edges = sorted((w, u, v) for u in graph for v, w in graph[u].items() if u < v)
    for w, u, v in edges:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            total += w
            accepted += 1
    if accepted != len(graph) - 1:
        raise ValueError("Disconnected graph")
    return total


class HanoiTests(unittest.TestCase):
    def test_counts_and_legal_moves(self):
        for n in range(9):
            with self.subTest(n=n):
                pegs = {"A": list(range(n, 0, -1)), "B": [], "C": []}
                moves = list(hanoi(n))
                self.assertEqual(len(moves), 2 ** n - 1)
                for disk, u, v in moves:
                    self.assertEqual(pegs[u][-1], disk)
                    self.assertTrue(not pegs[v] or pegs[v][-1] > disk)
                    pegs[u].pop()
                    pegs[v].append(disk)
                self.assertEqual(pegs, {"A": [], "B": [], "C": list(range(n, 0, -1))})

    def test_known_sequence(self):
        self.assertEqual(list(hanoi(3)), [(1,"A","C"),(2,"A","B"),(1,"C","B"),
                                        (3,"A","C"),(1,"B","A"),(2,"B","C"),(1,"A","C")])

    def test_invalid(self):
        for n in (-1, 2.5, "3", True):
            with self.assertRaises(ValueError):
                hanoi(n)
        with self.assertRaises(ValueError):
            hanoi(2, "A", "A", "C")


class TreeTests(unittest.TestCase):
    def test_exact_traversals(self):
        tree = assignment_tree()
        self.assertEqual(preorder(tree), [1,2,4,8,16,17,9,18,19,5,10,20,21,11,22,23,3,6,12,24,25,13,26,27,7,14,28,29,15,30,31])
        self.assertEqual(inorder(tree), [16,8,17,4,18,9,19,2,20,10,21,5,22,11,23,1,24,12,25,6,26,13,27,3,28,14,29,7,30,15,31])
        self.assertEqual(postorder(tree), [16,17,8,18,19,9,4,20,21,10,22,23,11,5,2,24,25,12,26,27,13,6,28,29,14,30,31,15,7,3,1])
        self.assertEqual(levelorder(tree), list(range(1,32)))

    def test_structure(self):
        queue = [assignment_tree()]
        while queue:
            node = queue.pop(0)
            if node.value < 16:
                self.assertEqual(node.left.value, 2 * node.value)
                self.assertEqual(node.right.value, 2 * node.value + 1)
                queue.extend([node.left, node.right])
            else:
                self.assertIsNone(node.left)
                self.assertIsNone(node.right)

    def test_empty_single_and_skew(self):
        for fn in (preorder, inorder, postorder, levelorder):
            self.assertEqual(fn(None), [])
            self.assertEqual(fn(TreeNode(42)), [42])
        root = TreeNode(1, right=TreeNode(2, right=TreeNode(3)))
        self.assertEqual(inorder(root), [1,2,3])
        self.assertEqual(postorder(root), [3,2,1])


class HuffmanTests(unittest.TestCase):
    def setUp(self):
        self.freq = dict(zip("abcde", [2,4,8,16,16]))
        self.root, self.codes, self.merges = huffman(self.freq)

    def test_exact_codes_and_cost(self):
        self.assertEqual(self.codes, {"e":"0", "a":"1000", "b":"1001", "c":"101", "d":"11"})
        self.assertEqual(sum(self.freq[s] * len(self.codes[s]) for s in self.freq), 96)
        self.assertEqual([m[-1] for m in self.merges], [6,14,30,46])
        self.assertEqual(sum(m[-1] for m in self.merges), 96)

    def test_optimal_cost_by_exhaustive_lengths(self):
        # An optimal full binary tree with five leaves has depth at most four.
        # Kraft's inequality characterizes feasible binary prefix-code lengths.
        costs = [sum(f*l for f,l in zip(self.freq.values(), lengths))
                 for lengths in product(range(1,5), repeat=5)
                 if sum(2 ** -l for l in lengths) <= 1]
        self.assertEqual(min(costs), 96)

    def test_prefix_free(self):
        for s, code in self.codes.items():
            for t, other in self.codes.items():
                if s != t:
                    self.assertFalse(other.startswith(code))

    def test_round_trip(self):
        rng = random.Random(320)
        for n in (0,1,5,46,1000):
            text = "".join(rng.choice("abcde") for _ in range(n))
            self.assertEqual(decode(encode(text, self.codes), self.root), text)

    def test_single_symbol(self):
        root, codes, merges = huffman({"x":7})
        self.assertEqual(codes, {"x":"0"})
        self.assertEqual(decode(encode("xxxx", codes), root), "xxxx")
        self.assertEqual(merges, [])
        with self.assertRaises(ValueError):
            decode("1", root)

    def test_invalid_inputs(self):
        for f in ({}, {"a":0}, {"a":-1}, {"a":2.5}, {"a":True}, {"ab":2}):
            with self.assertRaises(ValueError):
                huffman(f)
        with self.assertRaises(ValueError):
            encode("z", self.codes)
        with self.assertRaises(ValueError):
            decode("102", self.root)
        with self.assertRaises(ValueError):
            decode("1", self.root)


class GraphTests(unittest.TestCase):
    def test_exact_distances_and_targets(self):
        graphs = assignment_graphs()
        d1, p1, _ = dijkstra(graphs["Figure 1"], "A")
        self.assertEqual(d1, dict(zip("ABCDEFGHIJKL", [0,12,14,4,17,8,7,13,16,19,10,20])))
        self.assertEqual(reconstruct_path(p1,"A","L"), ["A","D","H","E","J","L"])
        d2, p2, _ = dijkstra(graphs["Figure 2"], "A")
        self.assertEqual(d2, dict(zip("ABCDEFGHIJ", [0,2,5,7,11,23,11,18,9,10])))
        self.assertEqual(reconstruct_path(p2,"A","J"), ["A","I","J"])
        self.assertNotIn("L", graphs["Figure 2"])
        with self.assertRaises(ValueError):
            reconstruct_path(p2, "A", "L")

    def test_all_sources_against_floyd_warshall(self):
        for name, graph in assignment_graphs().items():
            oracle = floyd_warshall(graph)
            for source in graph:
                with self.subTest(graph=name, source=source):
                    distances, prev, trace = dijkstra(graph, source)
                    self.assertEqual(distances, oracle[source])
                    self.assertEqual(len(trace), len(graph))
                    for target in graph:
                        path = reconstruct_path(prev, source, target)
                        cost = sum(graph[u][v] for u,v in zip(path, path[1:]))
                        self.assertEqual(cost, distances[target])

    def test_mst_against_kruskal(self):
        for name, graph in assignment_graphs().items():
            expected = 35 if name == "Figure 1" else 42
            for source in graph:
                with self.subTest(graph=name, source=source):
                    edges, total, trace = prim(graph, source)
                    self.assertEqual(total, expected)
                    self.assertEqual(total, kruskal_weight(graph))
                    self.assertEqual(len(edges), len(graph)-1)
                    self.assertEqual(trace[-1]["visited"], sorted(graph))

    def test_matrices(self):
        for name, graph in assignment_graphs().items():
            vs, matrix = adjacency_matrix(graph)
            self.assertEqual(len(vs), 12 if name == "Figure 1" else 10)
            self.assertEqual(sum(map(len, graph.values())) // 2, 19)
            for i,u in enumerate(vs):
                for j,v in enumerate(vs):
                    self.assertEqual(matrix[i][j], matrix[j][i])
                    self.assertEqual(matrix[i][j], 0 if u == v else graph[u].get(v, inf))

    def test_random_connected_graphs(self):
        rng = random.Random(320)
        for n in range(2,11):
            vs = [str(i) for i in range(n)]
            edges = [(vs[i-1], vs[i], rng.randrange(0,20)) for i in range(1,n)]
            pairs = {frozenset((u,v)) for u,v,_ in edges}
            for i in range(n):
                for j in range(i+1,n):
                    if frozenset((vs[i],vs[j])) not in pairs and rng.random() < .3:
                        edges.append((vs[i],vs[j],rng.randrange(0,20)))
            graph = make_graph(edges)
            oracle = floyd_warshall(graph)
            for source in graph:
                self.assertEqual(dijkstra(graph, source)[0], oracle[source])
            self.assertEqual(prim(graph, vs[0])[1], kruskal_weight(graph))

    def test_disconnected_zero_single(self):
        graph = make_graph([("A","B",0)], ["A","B","C"])
        distances, prev, _ = dijkstra(graph, "A")
        self.assertEqual(distances, {"A":0,"B":0,"C":inf})
        self.assertEqual(reconstruct_path(prev,"A","C"), [])
        with self.assertRaises(ValueError):
            prim(graph)
        self.assertEqual(prim({"A":{}}), ([],0,[]))

    def test_invalid_graphs(self):
        for graph in ({"A":{"B":-1},"B":{"A":-1}},
                      {"A":{"B":1},"B":{}},
                      {"A":{"B":inf},"B":{"A":inf}},
                      {"A":{"A":0}},
                      {"A":{"B":True},"B":{"A":True}}):
            with self.assertRaises(ValueError):
                dijkstra(graph,"A")
            with self.assertRaises(ValueError):
                prim(graph,"A")
        with self.assertRaises(ValueError):
            dijkstra({"A":{}}, "Z")
        with self.assertRaises(ValueError):
            make_graph([("A","B",1),("B","A",2)])
        with self.assertRaises(ValueError):
            reconstruct_path({"A":None,"B":"C","C":"B"},"A","B")


if __name__ == "__main__":
    unittest.main(verbosity=2)