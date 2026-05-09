# Op Research Projet — BENYAHIA Amir

Master Informatique 1ère année

---

## Description

Implémentation des principaux algorithmes de flots vus en cours : Ford-Fulkerson pour le flot maximum, deux variantes du flot de coût minimum (Bellman-Ford et Dijkstra avec renormalisation), et un détecteur de cycles négatifs. Tout est codé en Python pur, sans librairie externe de graphes.

---

## Algorithmes implémentés

- Ford-Fulkerson — Edmonds-Karp (O(VE²))
- Min Cost Flow — Bellman-Ford (O(n²m))
- Min Cost Flow — Dijkstra avec potentiels de Johnson (O(n(V+E)logV))
- Détection de cycles négatifs — Bellman-Ford (O(VE))

---

## Structure du projet

```
Op_Research_Projet_BENYAHIA_Amir/
├── algorithms/
│   ├── ford_fulkerson.py          # BFS + augmentation + min cut
│   ├── min_cost_flow_bf.py        # Successive shortest paths via Bellman-Ford
│   ├── min_cost_flow_dijkstra.py  # Potentiels de Johnson + Dijkstra
│   └── negative_cycle.py          # Détection de cycles négatifs
├── graph/
│   ├── residual_graph.py          # Classes Arc et ResidualGraph
│   └── visualizer.py              # Génération .dot et .png via Graphviz
├── examples/
│   ├── simple.txt                 # Graphe à 5 nœuds avec coûts
│   ├── assignment.txt             # Graphe d'affectation biparti
│   └── negative_cost.txt          # Graphe avec coûts négatifs
├── tests/
│   ├── test_ford_fulkerson.py     # 7 tests
│   ├── test_min_cost_flow.py      # 7 tests
│   └── test_negative_cycle.py     # 8 tests
├── main.py                        # Interface CLI
└── README.md
```

---

## Graphe Résiduel

Le graphe résiduel est représenté par une **liste d'adjacence** (`dict[node → list[Arc]]`).

Chaque arc logique (i, j) du graphe original génère deux objets `Arc` couplés via un pointeur `arc.reverse` :

- Arc forward (i → j) : capacité résiduelle `u(i,j) - f(i,j)`, coût `c(i,j)`
- Arc backward (j → i) : capacité résiduelle `f(i,j) - l(i,j)`, coût `-c(i,j)`

```
Arc forward  (i) ──[cap=u-f, cost=c]──▶ (j)
Arc backward (j) ──[cap=f-l, cost=-c]──▶ (i)
         └─── arc.reverse ───┘
```

Lors d'une augmentation de flot, les deux arcs couplés sont mis à jour en **O(1)** grâce au pointeur `reverse`, sans reconstruction du graphe résiduel à chaque itération. Cette structure est compatible directement avec Bellman-Ford et Dijkstra.

---

## Prérequis

- Python 3.8+
- `pytest` pour les tests
- Graphviz pour la visualisation (optionnel)

---

## Installation

```bash
git clone https://github.com/Amir-Benyahia/Op_Research_Projet_BENYAHIA_Amir.git
cd Op_Research_Projet_BENYAHIA_Amir
```

---

## Utilisation

### Ligne de commande

```bash
# Ford-Fulkerson
python main.py examples/simple.txt --algo ford_fulkerson

# Min cost flow — Bellman-Ford
python main.py examples/assignment.txt --algo min_cost_bf

# Min cost flow — Dijkstra
python main.py examples/negative_cost.txt --algo min_cost_dijkstra

# Avec visualisation PNG (génère outputs/NOM_ALGO.png)
python main.py examples/simple.txt --algo ford_fulkerson --visualize

# Démonstrations
python main.py --demo
```

### Format du fichier d'entrée

```
# Commentaire
nodes 5          # nombre de nœuds
arc 0 1 10 2     # src dst capacité coût
arc 0 2 8 4
source 0
sink 4
```

Le champ `coût` est optionnel (défaut : 0). Les lignes commençant par `#` sont ignorées.

---

## Fichiers d'exemple

- `examples/simple.txt` — graphe à 5 nœuds avec capacités et coûts, source=0, sink=4.
- `examples/assignment.txt` — graphe d'affectation biparti (Peter, Paul, Mary → Bob, Mike, Julia).
- `examples/negative_cost.txt` — graphe avec un arc de coût négatif, pour comparer Bellman-Ford et Dijkstra renormalisé.

---

## Tests

```bash
python -m pytest tests/ -v
```

22 tests passent. Ils vérifient que `max_flow == min_cut` sur plusieurs topologies, que Bellman-Ford et Dijkstra produisent des résultats identiques sur les mêmes graphes, et que la détection de cycles négatifs ne remonte ni faux positifs ni faux négatifs.

---

## Auteur

Amir Benyahia
