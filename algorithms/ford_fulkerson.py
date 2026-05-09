# Ford-Fulkerson avec BFS = Edmonds-Karp
# complexite O(VE^2)

from collections import deque
from graph.residual_graph import ResidualGraph  # noqa: F401


def bfs_find_path(graph, source, sink):
    visited = {source: None}
    queue = deque([source])

    while queue:
        node = queue.popleft()
        if node == sink:
            # on remonte le chemin
            path = []
            current = sink
            while visited[current] is not None:
                arc = visited[current]
                path.append(arc)
                current = arc.src
            path.reverse()
            bottleneck = min(arc.capacity for arc in path)
            return path, bottleneck

        for arc in graph.adj[node]:
            if arc.dst not in visited and arc.capacity > 0:
                visited[arc.dst] = arc
                queue.append(arc.dst)

    return None, 0


def ford_fulkerson(graph, source, sink):
    """Calcule le flot max de source vers sink (Edmonds-Karp)."""
    max_flow_value = 0

    while True:
        path, bottleneck = bfs_find_path(graph, source, sink)
        if path is None or bottleneck == 0:
            break
        graph.augment(path, bottleneck)
        max_flow_value += bottleneck
        # print("debug:", max_flow_value)

    return max_flow_value


def find_min_cut(graph, source):
    """Trouve la coupe min apres calcul du flot max. Retourne (S, arcs)."""
    # BFS depuis source dans le residuel
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
                # arc sature S -> T = arc de la coupe
                cut_arcs.append((arc.src, arc.dst, arc.reverse.capacity))

    return S, cut_arcs


def print_flow_result(graph, max_flow_value, source, sink, node_names=None):
    """Affiche le flot et la coupe min."""
    def name(n):
        if node_names:
            return node_names[n]
        else:
            return str(n)

    print()
    print("=== MAX FLOW RESULT ===")
    print("Source:", name(source) + ", Sink:", name(sink))
    print("Max flow value:", max_flow_value)
    print()
    print("Flot sur chaque arc (flot / capacité) :")
    for node in sorted(graph.adj.keys()):
        for arc in graph.adj[node]:
            original_cap = arc.capacity + arc.flow
            if original_cap > 0 and arc.flow >= 0:
                print(f"  {name(arc.src)} -> {name(arc.dst)}: {arc.flow} / {original_cap}")

    S, cut_arcs = find_min_cut(graph, source)
    print()
    print("Min Cut :")
    print(f"  S (côté source) = {{ {', '.join(name(n) for n in sorted(S))} }}")
    print("  Arcs de la coupe :")
    cut_capacity = 0
    for src, dst, cap in cut_arcs:
        print(f"    {name(src)} -> {name(dst)}, capacité = {cap}")
        cut_capacity += cap
    print(f"  Capacité totale = {cut_capacity}  (doit être égal au max flow = {max_flow_value})")
    assert cut_capacity == max_flow_value, f"ERREUR : Max-Flow ({max_flow_value}) != Min-Cut ({cut_capacity})"
    print("  ✓ Théorème Max-Flow = Min-Cut vérifié")
