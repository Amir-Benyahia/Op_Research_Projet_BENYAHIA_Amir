# Algorithmes de Flots en Python

Implémentation from scratch des algorithmes de flots en Python — sans aucune librairie externe.

---

## Algorithmes implémentés

| Algorithme | Description |
|---|---|
| **Ford-Fulkerson** | Calcul du flot maximum par chemins augmentants (BFS), avec détection du coupe minimum (théorème max-flow min-cut). |
| **Détection de cycles négatifs** | Bellman-Ford sur le graphe résiduel complet ; identifie les nœuds du cycle et lève une assertion si demandé. |
| **Min Cost Flow — Bellman-Ford** | Flot de coût minimum par chemins augmentants successifs les moins chers ; tolère les coûts négatifs sur les arcs. |
| **Min Cost Flow — Dijkstra** | Variante plus rapide utilisant la renormalisation de Johnson (potentiels de Johnson) pour rendre tous les coûts réduits positifs et appliquer Dijkstra à chaque itération. |

---

## Structure du projet

```
Op_Research_Projet_Benyahia_Amir/
│
├── graph/
│   ├── __init__.py
│   └── residual_graph.py        # Classes Arc et ResidualGraph (liste d'adjacence)
│
├── algorithms/
│   ├── __init__.py
│   ├── negative_cycle.py        # detect_negative_cycle, assert_no_negative_cycle
│   ├── ford_fulkerson.py        # bfs_find_path, ford_fulkerson, find_min_cut, print_flow_result
│   ├── min_cost_flow_bf.py      # bellman_ford_shortest_path, reconstruct_path, min_cost_flow_bellman_ford
│   └── min_cost_flow_dijkstra.py# initialize_potentials_bellman_ford, dijkstra_with_potentials, min_cost_flow_dijkstra
│
├── tests/
│   ├── __init__.py
│   ├── test_ford_fulkerson.py   # 7 tests — max flow, min cut, graphe biparti, cas limites
│   ├── test_min_cost_flow.py    # 7 tests — BF vs Dijkstra, required_flow, graphes variés
│   └── test_negative_cycle.py  # 8 tests — cycles négatifs, faux positifs, cas limites
│
├── main.py                      # Démonstrations des 4 algorithmes
└── README.md
```

---

## Prérequis

- Python 3.8 ou supérieur
- Aucune dépendance externe pour les algorithmes
- `pytest` uniquement pour exécuter les tests

---

## Installation

```bash
git clone <url-du-repo>
cd Op_Research_Projet_Benyahia_Amir
```

---

## Utilisation

```bash
python3 main.py
```

Le script enchaîne six démonstrations :

1. **Ford-Fulkerson** — graphe à 5 nœuds, affichage du flot sur chaque arc, vérification max-flow = min-cut.
2. **Graphe d'affectation** — réseau Peter/Paul/Mary avec 3 personnes, 5 projets et 3 tâches ; max flow attendu = 7.
3. **Min Cost Flow Bellman-Ford** — même graphe avec coûts, affiche `total_flow` et `total_cost`.
4. **Min Cost Flow Dijkstra** — même graphe, vérifie que le résultat est identique à Bellman-Ford.
5. **Comparaison BF vs Dijkstra** — graphe à 6 nœuds, les deux algorithmes doivent produire des résultats identiques.
6. **Détection de cycles négatifs** — trois graphes distincts avec affichage des nœuds du cycle détecté.

---

## Tests

```bash
python3 -m pytest tests/ -v
```

22 tests couvrent :

- **Ford-Fulkerson** (7 tests) : flot maximum, égalité max-flow/min-cut, graphe pathologique, couplage biparti, absence de chemin, arc unique.
- **Min Cost Flow** (7 tests) : résultats identiques BF et Dijkstra, contrainte `required_flow`, graphe diamant, chemin unique, chemins parallèles.
- **Cycles négatifs** (8 tests) : détection correcte, absence de faux positifs sur arcs backward, `assert_no_negative_cycle`, nœud isolé, graphe à deux nœuds.

---

## Structure de données

Le graphe résiduel est représenté par une **liste d'adjacence** (`dict[node, list[Arc]]`). Chaque arc logique génère deux objets `Arc` couplés par un pointeur `reverse` : l'arc forward (capacité initiale, coût c) et l'arc backward (capacité 0, coût −c). Lors d'une augmentation de flot, les capacités des deux arcs sont mises à jour en O(1) via ce pointeur. Ce couplage garantit la cohérence du résiduel sans reconstruction, et la liste d'adjacence permet de ne parcourir que les voisins actifs — ce qui est efficace pour des graphes creux, typiques des problèmes de flots.

---

## Auteur

**Amir Benyahia** — Master Informatique 1ère année
