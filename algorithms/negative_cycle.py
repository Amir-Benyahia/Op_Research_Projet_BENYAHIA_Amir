# detection bellman-ford, n iterations au lieu de n-1
# si on peut encore relaxer a la nieme iteration -> cycle negatif


def detect_negative_cycle(graph):
    """Detecte un cycle négatif dans le graphe résiduel."""
    n = graph.num_nodes
    dist = {node: 0 for node in graph.adj}
    pred = {node: None for node in graph.adj}

    last_relaxed = None

    # n iterations (et pas n-1) pour pouvoir detecter
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

    # reconstruction du cycle : on remonte n fois pour etre sur d'etre dedans
    node = last_relaxed
    for _ in range(n):
        if pred[node] is None:
            return True, [node]
        node = pred[node].src

    # maintenant on est dans le cycle, on le parcourt
    cycle_start = node
    cycle = [cycle_start]
    if pred[cycle_start] is None:
        return True, cycle

    node = pred[cycle_start].src
    seen = {cycle_start}
    while node != cycle_start and node not in seen:
        cycle.append(node)
        seen.add(node)
        if pred[node] is None:
            break
        node = pred[node].src
    cycle.append(cycle_start)
    cycle.reverse()

    return True, cycle


def assert_no_negative_cycle(graph, context=""):
    """Leve une AssertionError si cycle negatif detecte."""
    has_cycle, cycle = detect_negative_cycle(graph)
    if has_cycle:
        msg = "Cycle négatif détecté"
        if context:
            msg += f" ({context})"
        if cycle:
            msg += f" : nœuds {cycle}"
        raise AssertionError(msg)
