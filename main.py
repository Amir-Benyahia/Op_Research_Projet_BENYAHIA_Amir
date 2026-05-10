# main
# CLI + demos hardcodees

import argparse
import os
import sys

from graph.residual_graph import ResidualGraph
from algorithms.ford_fulkerson import ford_fulkerson, find_min_cut, print_flow_result
from algorithms.min_cost_flow_bf import min_cost_flow_bellman_ford
from algorithms.min_cost_flow_dijkstra import min_cost_flow_dijkstra
from algorithms.negative_cycle import detect_negative_cycle, assert_no_negative_cycle


# Parser de fichier graphe


def parse_graph_file(path):
    """Lit un fichier .txt et retourne (graph, source, sink)."""
    num_nodes = None
    arcs = []
    source = None
    sink = None

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            kw = parts[0]
            if kw == "nodes":
                num_nodes = int(parts[1])
            elif kw == "arc":
                src, dst, cap = int(parts[1]), int(parts[2]), int(parts[3])
                if len(parts) >= 5:
                    cost = int(parts[4])
                else:
                    cost = 0
                arcs.append((src, dst, cap, cost))
            elif kw == "source":
                source = int(parts[1])
            elif kw == "sink":
                sink = int(parts[1])

    if num_nodes is None:
        raise ValueError(f"{path} : directive 'nodes' manquante.")
    if source is None or sink is None:
        raise ValueError(f"{path} : directives 'source' / 'sink' manquantes.")

    g = ResidualGraph(num_nodes)
    for src, dst, cap, cost in arcs:
        g.add_arc(src, dst, cap, cost=cost)

    return g, source, sink



# Affichage


def print_arcs(graph, with_cost=False):
    """Affiche le flot sur chaque arc."""
    seen = set()
    for node in graph.adj:
        for arc in graph.adj[node]:
            original_cap = arc.capacity + arc.flow
            if original_cap <= 0:
                continue
            key = (arc.src, arc.dst)
            if key in seen:
                continue
            seen.add(key)
            line = f"  {arc.src} -> {arc.dst} : {arc.flow} / {original_cap}"
            if with_cost:
                line += f"  (coût unitaire : {arc.cost})"
            else:
                line += f"  (coût : {arc.cost})"
            print(line)


def print_ford_fulkerson_result(graph, max_flow, source):
    print(f"Flot max : {max_flow}")
    print("Flot sur chaque arc :")
    print_arcs(graph, with_cost=False)

    S, cut_arcs = find_min_cut(graph, source)
    cut_cap = sum(cap for _, _, cap in cut_arcs)
    s_nodes = ", ".join(str(n) for n in sorted(S))
    cut_str = ", ".join(f"({s}->{d}, cap={c})" for s, d, c in cut_arcs)
    print("Min Cut :")
    print(f"  S = {{{s_nodes}}}")
    print(f"  Arcs coupés : {cut_str}")
    if cut_cap == max_flow:
        status = "✓ égale au flot max"
    else:
        status = "✗ ERREUR"
    print(f"  Capacité totale : {cut_cap}  {status}")


def print_min_cost_result(algo_name, graph, total_flow, total_cost):
    print(f"Flot total : {total_flow}")
    print(f"Coût total : {total_cost}")
    print("Flot sur chaque arc :")
    print_arcs(graph, with_cost=True)



# Runner CLI


def run_algo(graph_path, algo, do_visualize):
    g, source, sink = parse_graph_file(graph_path)
    basename = os.path.splitext(os.path.basename(graph_path))[0]

    if algo == "ford_fulkerson":
        print("=== FORD-FULKERSON ===")
        assert_no_negative_cycle(g)
        max_flow = ford_fulkerson(g, source, sink)
        print_ford_fulkerson_result(g, max_flow, source)
        title = f"Ford-Fulkerson — {basename}"

    elif algo == "min_cost_bf":
        print("=== MIN COST FLOW (Bellman-Ford) ===")
        total_flow, total_cost = min_cost_flow_bellman_ford(g, source, sink)
        print_min_cost_result("Bellman-Ford", g, total_flow, total_cost)
        title = f"Min Cost Flow BF — {basename}"

    elif algo == "min_cost_dijkstra":
        print("=== MIN COST FLOW (Dijkstra) ===")
        total_flow, total_cost = min_cost_flow_dijkstra(g, source, sink)
        print_min_cost_result("Dijkstra", g, total_flow, total_cost)
        title = f"Min Cost Flow Dijkstra — {basename}"

    else:
        print(f"Algorithme inconnu : {algo}", file=sys.stderr)
        sys.exit(1)

    if do_visualize:
        from graph.visualizer import visualize
        os.makedirs("outputs", exist_ok=True)
        out = os.path.join("outputs", f"{basename}_{algo}")
        visualize(g, output_path=out, title=title)



# Demos hardcodees 

def demo_ford_fulkerson():
    print("\n" + "=" * 60)
    print("DEMO 1 : Ford-Fulkerson — Max Flow + Min Cut")
    print("=" * 60)

    # 0=S, 1=A, 2=B, 3=C, 4=T
    g = ResidualGraph(5)
    source, sink = 0, 4
    node_names = {0: "S", 1: "A", 2: "B", 3: "C", 4: "T"}

    g.add_arc(0, 1, 10)
    g.add_arc(0, 2, 10)
    g.add_arc(1, 3, 10)
    g.add_arc(2, 3, 10)
    g.add_arc(3, 4, 10)
    g.add_arc(1, 2, 1)

    assert_no_negative_cycle(g)
    max_flow = ford_fulkerson(g, source, sink)
    print_flow_result(g, max_flow, source, sink, node_names)


def demo_assignment_graph():
    print("\n" + "=" * 60)
    print("DEMO 2 : Graphe d'affectation Peter/Paul/Mary")
    print("=" * 60)

    g = ResidualGraph(13)
    source, sink = 0, 12
    node_names = {
        0: "Source", 1: "Peter", 2: "Paul", 3: "Mary",
        4: "M", 5: "D", 6: "N", 7: "B", 8: "O",
        9: "Bob", 10: "Mike", 11: "Julia", 12: "Sink",
    }

    # source -> personnes
    g.add_arc(0, 1, 3)
    g.add_arc(0, 2, 3)
    g.add_arc(0, 3, 3)
    # personnes -> projets
    g.add_arc(1, 4, 1); g.add_arc(1, 5, 1); g.add_arc(1, 6, 1)
    g.add_arc(2, 4, 1); g.add_arc(2, 7, 1); g.add_arc(2, 8, 1)
    g.add_arc(3, 5, 1); g.add_arc(3, 6, 1); g.add_arc(3, 8, 1)
    # projets -> taches
    g.add_arc(4, 9, 2); g.add_arc(5, 10, 2); g.add_arc(6, 11, 1)
    g.add_arc(7, 9, 2); g.add_arc(8, 11, 2)
    # taches -> sink
    g.add_arc(9, sink, 3); g.add_arc(10, sink, 2); g.add_arc(11, sink, 2)

    assert_no_negative_cycle(g)
    max_flow = ford_fulkerson(g, source, sink)
    print(f"\nMax flow (affectation) = {max_flow}  (attendu : 7)")

    S, cut_arcs = find_min_cut(g, source)
    cut_cap = sum(cap for _, _, cap in cut_arcs)
    print(f"Min Cut capacity = {cut_cap}  (doit = {max_flow})")
    assert cut_cap == max_flow
    print("✓ Max-Flow = Min-Cut vérifié")


def demo_min_cost_flow_bellman_ford():
    print("\n" + "=" * 60)
    print("DEMO 3 : Min Cost Flow — Bellman-Ford")
    print("=" * 60)

    g = ResidualGraph(5)
    source, sink = 0, 4

    g.add_arc(0, 1, 10, cost=2)
    g.add_arc(0, 2, 10, cost=4)
    g.add_arc(1, 3, 10, cost=1)
    g.add_arc(2, 3, 10, cost=3)
    g.add_arc(3, 4, 10, cost=1)
    g.add_arc(1, 2, 5, cost=1)

    assert_no_negative_cycle(g)
    flow, cost = min_cost_flow_bellman_ford(g, source, sink)
    print("Flot total :", flow)
    print("Coût total :", cost)


def demo_min_cost_flow_dijkstra():
    print("\n" + "=" * 60)
    print("DEMO 4 : Min Cost Flow — Dijkstra + Renormalisation")
    print("=" * 60)

    g = ResidualGraph(5)
    source, sink = 0, 4

    g.add_arc(0, 1, 10, cost=2)
    g.add_arc(0, 2, 10, cost=4)
    g.add_arc(1, 3, 10, cost=1)
    g.add_arc(2, 3, 10, cost=3)
    g.add_arc(3, 4, 10, cost=1)
    g.add_arc(1, 2, 5, cost=1)

    assert_no_negative_cycle(g)
    flow, cost = min_cost_flow_dijkstra(g, source, sink)
    print("Flot total :", flow)
    print("Coût total :", cost)
    print("(attendu : flow=10, cost=40)")


def demo_comparison_bf_vs_dijkstra():
    print("\n" + "=" * 60)
    print("DEMO 5 : Comparaison Bellman-Ford vs Dijkstra")
    print("=" * 60)

    def make_graph():
        g = ResidualGraph(6)
        g.add_arc(0, 1, 8, cost=3)
        g.add_arc(0, 2, 6, cost=1)
        g.add_arc(1, 3, 5, cost=2)
        g.add_arc(2, 3, 4, cost=4)
        g.add_arc(2, 4, 5, cost=2)
        g.add_arc(3, 5, 7, cost=1)
        g.add_arc(4, 5, 6, cost=3)
        g.add_arc(1, 4, 3, cost=1)
        return g

    g1 = make_graph()
    g2 = make_graph()
    flow_bf, cost_bf = min_cost_flow_bellman_ford(g1, 0, 5)
    flow_dj, cost_dj = min_cost_flow_dijkstra(g2, 0, 5)

    print(f"Bellman-Ford : flow={flow_bf}, cost={cost_bf}")
    print(f"Dijkstra     : flow={flow_dj}, cost={cost_dj}")

    if flow_bf == flow_dj and cost_bf == cost_dj:
        print("✓ Résultats identiques")
    else:
        print("✗ DIVERGENCE !")


def demo_negative_cycle_detection():
    print("\n" + "=" * 60)
    print("DEMO 6 : Détection de Cycles Négatifs")
    print("=" * 60)

    # cycle de cout +1 = pas negatif
    g1 = ResidualGraph(4)
    g1.add_arc(0, 1, 10, cost=2)
    g1.add_arc(1, 2, 10, cost=3)
    g1.add_arc(2, 0, 10, cost=-4)
    g1.add_arc(0, 3, 10, cost=1)
    has1, _ = detect_negative_cycle(g1)
    print(f"\nGraphe 1 (cycle de coût +1) : cycle négatif = {has1}  (attendu : False)")

    # cycle de cout -3
    g2 = ResidualGraph(3)
    g2.add_arc(0, 1, 10, cost=1)
    g2.add_arc(1, 2, 10, cost=1)
    g2.add_arc(2, 0, 10, cost=-5)
    has2, cycle2 = detect_negative_cycle(g2)
    print(f"\nGraphe 2 (cycle de coût -3) : cycle négatif = {has2}  (attendu : True)")
    if cycle2:
        print(f"  Nœuds du cycle : {cycle2}")

    # cycle 1->2->3->1
    g3 = ResidualGraph(5)
    g3.add_arc(0, 1, 10, cost=2)
    g3.add_arc(1, 2, 10, cost=3)
    g3.add_arc(2, 3, 10, cost=-8)
    g3.add_arc(3, 1, 10, cost=2)
    g3.add_arc(0, 4, 10, cost=1)
    has3, cycle3 = detect_negative_cycle(g3)
    print(f"\nGraphe 3 (cycle 1→2→3→1, coût=-3) : cycle négatif = {has3}  (attendu : True)")
    if cycle3:
        print(f"  Nœuds du cycle : {cycle3}")


def run_demos():
    demo_ford_fulkerson()
    demo_assignment_graph()
    demo_min_cost_flow_bellman_ford()
    demo_min_cost_flow_dijkstra()
    demo_comparison_bf_vs_dijkstra()
    demo_negative_cycle_detection()
    print("\n" + "=" * 60)
    print("✓ Toutes les démonstrations terminées avec succès.")
    print("=" * 60)

# Point d'entree


def main():
    parser = argparse.ArgumentParser(
        description="Algorithmes de flots — Max Flow et Min Cost Flow.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Exemples :\n"
            "  python main.py examples/simple.txt --algo ford_fulkerson\n"
            "  python main.py examples/simple.txt --algo min_cost_bf\n"
            "  python main.py examples/simple.txt --algo min_cost_dijkstra\n"
            "  python main.py examples/simple.txt --algo ford_fulkerson --visualize\n"
            "  python main.py --demo"
        ),
    )
    parser.add_argument("graph_file", nargs="?", help="Chemin vers le fichier graphe (.txt)")
    parser.add_argument(
        "--algo",
        choices=["ford_fulkerson", "min_cost_bf", "min_cost_dijkstra"],
        help="Algorithme à exécuter :\n"
             "  ford_fulkerson    — flot maximum (BFS) + coupe minimum\n"
             "  min_cost_bf       — flot de coût minimum (Bellman-Ford)\n"
             "  min_cost_dijkstra — flot de coût minimum (Dijkstra + potentiels)",
    )
    parser.add_argument("--visualize", action="store_true",
                        help="Génère une image PNG dans outputs/ (nécessite Graphviz)")
    parser.add_argument("--demo", action="store_true",
                        help="Lance les démonstrations hardcodées (ignore graph_file et --algo)")

    args = parser.parse_args()

    if args.demo:
        run_demos()
        return

    if not args.graph_file:
        parser.error("graph_file requis (ou utilise --demo).")
    if not args.algo:
        parser.error("--algo requis (ford_fulkerson | min_cost_bf | min_cost_dijkstra).")

    run_algo(args.graph_file, args.algo, args.visualize)


if __name__ == "__main__":
    main()
