# Structure du graphe résiduel - liste d'adjacence
# Chaque arc a un pointeur "reverse" vers son arc inverse


class Arc:
    """Un arc du graphe résiduel."""

    def __init__(self, src, dst, capacity, cost=0, lower=0):
        self.src = src
        self.dst = dst
        self.capacity = capacity
        self.cost = cost
        self.lower = lower  # pour les bornes inf, pas vraiment utilisé ici
        self.flow = 0
        self.reverse = None


class ResidualGraph:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.adj = {i: [] for i in range(num_nodes)}

    def add_arc(self, src, dst, capacity, cost=0, lower=0):
        # forward = arc original, backward = arc inverse (cap 0 au depart)
        forward = Arc(src, dst, capacity - lower, cost, lower)
        backward = Arc(dst, src, 0, -cost, 0)
        forward.reverse = backward
        backward.reverse = forward
        self.adj[src].append(forward)
        self.adj[dst].append(backward)
        return forward

    def augment(self, path_arcs, flow_amount):
        # update les deux arcs (forward et backward) en O(1) grace au reverse
        for arc in path_arcs:
            arc.capacity -= flow_amount
            arc.reverse.capacity += flow_amount
            arc.flow += flow_amount
            arc.reverse.flow -= flow_amount
