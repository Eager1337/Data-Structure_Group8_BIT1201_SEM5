"""Interactive menu and reproducible all-problem demonstration."""
import argparse
import json
from pathlib import Path
from math import inf
from src.algorithms import (
    hanoi, assignment_tree, preorder, inorder, postorder, levelorder,
    huffman, encode, decode, assignment_graphs, adjacency_matrix,
    dijkstra, reconstruct_path, prim,
)

FREQUENCIES = {"a": 2, "b": 4, "c": 8, "d": 16, "e": 16}


def fmt(value):
    return "inf" if value == inf else str(value)


def demo_hanoi(n):
    print(f"TOWER OF HANOI: n={n}; minimum moves={2 ** n - 1}")
    pegs = {"A": list(range(n, 0, -1)), "B": [], "C": []}
    print("Initial:", pegs)
    for step, (disk, source, target) in enumerate(hanoi(n), 1):
        if not pegs[source] or pegs[source][-1] != disk:
            raise AssertionError("Disk is not on top of source peg.")
        if pegs[target] and pegs[target][-1] < disk:
            raise AssertionError("Larger disk cannot rest on smaller disk.")
        pegs[source].pop()
        pegs[target].append(disk)
        print(f"{step:3}: disk {disk}, {source} -> {target}; {pegs}")
    return pegs


def demo_tree():
    print("TREE TRAVERSALS: provided tree, labels 1..31")
    root = assignment_tree()
    traversals = {"Pre-order": preorder(root), "In-order": inorder(root),
                  "Post-order": postorder(root), "Level-order": levelorder(root)}
    for name, sequence in traversals.items():
        print(f"{name}: {' '.join(map(str, sequence))}")
    return traversals


def demo_huffman():
    print("HUFFMAN CODING:", FREQUENCIES)
    root, codes, merges = huffman(FREQUENCIES)
    for i, (left, f1, right, f2, total) in enumerate(merges, 1):
        print(f"Merge {i}: {left}:{f1} + {right}:{f2} = {total}")
    for s in sorted(FREQUENCIES):
        print(f"{s}: frequency={FREQUENCIES[s]}, code={codes[s]}, "
              f"contribution={FREQUENCIES[s] * len(codes[s])} bits")
    # A demonstration order only: the handout specifies counts, not a message.
    message = "".join(s * FREQUENCIES[s] for s in sorted(FREQUENCIES))
    encoded = encode(message, codes)
    print("Demonstration message:", message)
    print("Encoded message:", encoded)
    print(f"Payload length: {len(encoded)} bits; packed bytes: {(len(encoded)+7)//8}")
    print("Decoded message matches:", decode(encoded, root) == message)
    return {"codes": codes, "merges": merges, "message": message,
            "encoded": encoded, "bits": len(encoded)}


def demo_graphs():
    results = {}
    for name, graph in assignment_graphs().items():
        print(f"\n{name.upper()}: {len(graph)} vertices, "
              f"{sum(map(len, graph.values())) // 2} undirected edges")
        vertices, matrix = adjacency_matrix(graph)
        print("Adjacency matrix (inf = no edge):")
        print("    " + " ".join(f"{v:>3}" for v in vertices))
        for vertex, row in zip(vertices, matrix):
            print(f"{vertex:>3} " + " ".join(f"{fmt(w):>3}" for w in row))
        distances, previous, trace = dijkstra(graph, "A")
        print("Dijkstra settlements and successful relaxations:")
        for i, step in enumerate(trace, 1):
            changes = "; ".join(f"{v}: {fmt(old)}->{new} via {u}"
                                for v, old, new, u in step["updates"])
            print(f"{i:2}. settle {step['vertex']}={step['distance']}; "
                  + (changes or "no improvements"))
        paths = {}
        print("All shortest paths from A:")
        for vertex in vertices:
            path = reconstruct_path(previous, "A", vertex)
            paths[vertex] = path
            print(f"A -> {vertex}: cost={fmt(distances[vertex])}; "
                  + " -> ".join(path))
        if "L" not in graph:
            print("A -> L: NOT APPLICABLE; Figure 2 contains no vertex L.")
            print("A -> J is the demonstration destination, not a relabelled L.")
        mst, cost, prim_trace = prim(graph, "A")
        print("Prim's MST (NOT a shortest-path algorithm):")
        for i, step in enumerate(prim_trace, 1):
            u, v, w = step["edge"]
            print(f"{i:2}. add {u}-{v} ({w}); cumulative weight={step['total']}")
        print("MST total weight:", cost)
        results[name] = {"vertices": vertices, "matrix": matrix,
                         "distances": distances, "previous": previous,
                         "trace": trace, "paths": paths, "mst": mst,
                         "mst_weight": cost, "prim_trace": prim_trace}
    return results


def run_all(n):
    demo_hanoi(n)
    print()
    tree = demo_tree()
    print()
    compression = demo_huffman()
    graphs = demo_graphs()
    return {"hanoi_n": n, "tree": tree, "huffman": compression, "graphs": graphs}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="Run all problems")
    parser.add_argument("--disks", type=int, default=3)
    parser.add_argument("--json", type=Path, help="Save all-demo results to JSON")
    args = parser.parse_args()
    if not 0 <= args.disks <= 15:
        parser.error("For a readable demonstration, --disks must be 0..15.")
    if args.all:
        results = run_all(args.disks)
        if args.json:
            args.json.parent.mkdir(parents=True, exist_ok=True)
            # Replace non-edge infinity with null for standards-compliant JSON.
            def clean(obj):
                if isinstance(obj, dict):
                    return {k: clean(v) for k, v in obj.items()}
                if isinstance(obj, (list, tuple)):
                    return [clean(v) for v in obj]
                return None if obj == inf else obj
            args.json.write_text(json.dumps(clean(results), indent=2) + "\n")
        return
    while True:
        print("\nDCOMP320: 1 Hanoi | 2 Tree | 3 Huffman | 4 Graphs | 5 All | 0 Exit")
        try:
            choice = input("Choice: ").strip()
            if choice == "0":
                return
            if choice in {"1", "5"}:
                n = int(input("Number of disks (0..15): "))
                if not 0 <= n <= 15:
                    raise ValueError("Choose 0..15 disks for a manageable display.")
                run_all(n) if choice == "5" else demo_hanoi(n)
            elif choice == "2":
                demo_tree()
            elif choice == "3":
                demo_huffman()
            elif choice == "4":
                demo_graphs()
            else:
                print("Choose 0, 1, 2, 3, 4 or 5.")
        except ValueError as error:
            print("Input error:", error)
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return


if __name__ == "__main__":
    main()