def detect_negative_cycle(graph):
    """
    Détecte un cycle négatif dans le graphe résiduel via Bellman-Ford.

    Retourne :
        (False, None)       si pas de cycle négatif
        (True, cycle_nodes) si cycle négatif trouvé, avec les nœuds du cycle

    Complexité : O(VE)
    """
    INF = float('inf')
    n = graph.num_nodes
    dist = {node: 0 for node in graph.adj}
    pred = {node: None for node in graph.adj}

    last_relaxed = None

    for i in range(n):
        last_relaxed = None
        for node in graph.adj:
            for arc in graph.adj[node]:
                if arc.capacity <= 0:
                    continue
                if dist[node] + arc.cost < dist[arc.dst]:
                    dist[arc.dst] = dist[node] + arc.cost
                    pred[arc.dst] = arc
                    last_relaxed = arc.dst

    if last_relaxed is None:
        return False, None

    node = last_relaxed
    for _ in range(n):
        if pred[node] is None:
            return True, [node]
        node = pred[node].src

    cycle_start = node
    cycle = [cycle_start]
    if pred[cycle_start] is None:
        return True, cycle

    node = pred[cycle_start].src
    visited_in_cycle = {cycle_start}
    while node != cycle_start and node not in visited_in_cycle:
        cycle.append(node)
        visited_in_cycle.add(node)
        if pred[node] is None:
            break
        node = pred[node].src
    cycle.append(cycle_start)
    cycle.reverse()

    return True, cycle


def assert_no_negative_cycle(graph, context=""):
    """
    Lève une AssertionError si un cycle négatif est détecté.
    """
    has_neg_cycle, cycle = detect_negative_cycle(graph)
    if has_neg_cycle:
        msg = "Cycle négatif détecté"
        if context:
            msg += f" ({context})"
        if cycle:
            msg += f" : nœuds {cycle}"
        raise AssertionError(msg)
