"""
Ford-Fulkerson (variante Edmonds-Karp) : calcul du flot maximum et de la coupe minimale.

Edmonds-Karp utilise un BFS pour trouver les chemins augmentants, ce qui garantit
une complexité O(VE²) indépendamment des valeurs de capacité.

Théorème Max-Flow Min-Cut :
    La valeur du flot maximum de s à t est égale à la capacité minimale
    d'une coupe séparant s de t.
"""

from collections import deque
from graph.residual_graph import ResidualGraph


def bfs_find_path(graph, source, sink):
    """
    BFS dans le graphe résiduel pour trouver un chemin augmentant source→sink.

    Seuls les arcs avec capacité résiduelle > 0 sont parcourus.

    Retourne :
        (path_arcs, bottleneck) — liste d'Arc et capacité minimale sur le chemin
        (None, 0)               — si sink est inatteignable
    """
    visited = {source: None}  # node → arc utilisé pour y arriver
    queue = deque([source])

    while queue:
        node = queue.popleft()
        if node == sink:
            path_arcs = []
            current = sink
            while visited[current] is not None:
                arc = visited[current]
                path_arcs.append(arc)
                current = arc.src
            path_arcs.reverse()
            bottleneck = min(arc.capacity for arc in path_arcs)
            return path_arcs, bottleneck

        for arc in graph.adj[node]:
            if arc.dst not in visited and arc.capacity > 0:
                visited[arc.dst] = arc
                queue.append(arc.dst)

    return None, 0


def ford_fulkerson(graph, source, sink):
    """
    Calcule le flot maximum de source vers sink (variante Edmonds-Karp).

    Retourne la valeur totale du flot maximum.

    Complexité : O(VE²)
    """
    max_flow_value = 0

    while True:
        path_arcs, bottleneck = bfs_find_path(graph, source, sink)
        if path_arcs is None or bottleneck == 0:
            break
        graph.augment(path_arcs, bottleneck)
        max_flow_value += bottleneck

    return max_flow_value


def find_min_cut(graph, source):
    """
    Trouve la coupe minimale après calcul du flot maximum.

    BFS dans le graphe résiduel depuis source :
    - S = nœuds atteignables (arcs résiduels disponibles)
    - T = nœuds inatteignables
    - coupe = arcs saturés allant de S vers T

    Retourne :
        S        — ensemble des nœuds côté source
        cut_arcs — liste de (src, dst, capacité) des arcs de la coupe
    """
    visited = set()
    queue = deque([source])
    visited.add(source)

    while queue:
        node = queue.popleft()
        for arc in graph.adj[node]:
            if arc.dst not in visited and arc.capacity > 0:
                visited.add(arc.dst)
                queue.append(arc.dst)

    S = visited
    cut_arcs = []
    for node in S:
        for arc in graph.adj[node]:
            if arc.dst not in S and arc.capacity == 0 and arc.reverse.capacity > 0:
                cut_arcs.append((arc.src, arc.dst, arc.reverse.capacity))

    return S, cut_arcs


def print_flow_result(graph, max_flow_value, source, sink, node_names=None):
    """
    Affiche le flot sur chaque arc et la coupe minimale.
    node_names : dict optionnel {id → nom} pour l'affichage.
    """
    def name(n):
        return node_names[n] if node_names else str(n)

    print(f"\n=== MAX FLOW RESULT ===")
    print(f"Source: {name(source)}, Sink: {name(sink)}")
    print(f"Max flow value: {max_flow_value}")
    print("\nFlot sur chaque arc (flot / capacité) :")
    for node in sorted(graph.adj.keys()):
        for arc in graph.adj[node]:
            original_cap = arc.capacity + arc.flow
            if original_cap > 0 and arc.flow >= 0:
                print(f"  {name(arc.src)} -> {name(arc.dst)}: {arc.flow} / {original_cap}")

    S, cut_arcs = find_min_cut(graph, source)
    print(f"\nMin Cut :")
    print(f"  S (côté source) = {{ {', '.join(name(n) for n in sorted(S))} }}")
    print(f"  Arcs de la coupe :")
    cut_capacity = 0
    for src, dst, cap in cut_arcs:
        print(f"    {name(src)} -> {name(dst)}, capacité = {cap}")
        cut_capacity += cap
    print(f"  Capacité totale = {cut_capacity}  (doit être égal au max flow = {max_flow_value})")
    assert cut_capacity == max_flow_value, (
        f"ERREUR : Max-Flow ({max_flow_value}) ≠ Min-Cut ({cut_capacity})"
    )
    print("  ✓ Théorème Max-Flow = Min-Cut vérifié")
