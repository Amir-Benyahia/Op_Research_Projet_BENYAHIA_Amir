# Op Research Projet — BENYAHIA Amir

---

## Description

Implémentation from scratch en Python pur des algorithmes de flots en réseau, sans aucune librairie externe de graphes.
Tous les algorithmes reposent sur une structure de graphe résiduel maison avec arcs couplés forward/backward.
Le projet couvre le flot maximum, le flot de coût minimum et la détection de cycles négatifs,
avec une interface en ligne de commande et une visualisation PNG via Graphviz.

---

## Algorithmes implémentés

| Algorithme | Fichier | Complexité | Description |
|---|---|---|---|
| Ford-Fulkerson (Edmonds-Karp) | `algorithms/ford_fulkerson.py` | O(VE²) | Max flow + min cut |
| Min Cost Flow — Bellman-Ford | `algorithms/min_cost_flow_bf.py` | O(n²m) | Successive shortest paths, gère les coûts négatifs |
| Min Cost Flow — Dijkstra | `algorithms/min_cost_flow_dijkstra.py` | O(n(V+E)logV) | Dijkstra + renormalisation des coûts |
| Détection cycles négatifs | `algorithms/negative_cycle.py` | O(VE) | Garantit l'optimalité du flot |

---

## Structure du projet

```
Op_Research_Projet_BENYAHIA_Amir/
├── algorithms/
│   ├── ford_fulkerson.py          # BFS + augmentation + min cut
│   ├── min_cost_flow_bf.py        # Bellman-Ford + reconstruction de chemin
│   ├── min_cost_flow_dijkstra.py  # Potentiels de Johnson + Dijkstra
│   └── negative_cycle.py          # Détection et assertion cycle négatif
├── graph/
│   ├── residual_graph.py          # Classes Arc et ResidualGraph (liste d'adjacence)
│   └── visualizer.py              # Génération .dot et .png via Graphviz
├── examples/
│   ├── simple.txt                 # Graphe à 5 nœuds avec coûts
│   ├── assignment.txt             # Graphe d'affectation (Peter/Paul/Mary)
│   └── negative_cost.txt          # Graphe avec coûts négatifs (test BF vs Dijkstra)
├── tests/
│   ├── test_ford_fulkerson.py     # 7 tests — max flow, min cut, biparti, cas limites
│   ├── test_min_cost_flow.py      # 7 tests — BF vs Dijkstra, required_flow, diamant
│   └── test_negative_cycle.py    # 8 tests — détection, faux positifs, assert
├── main.py                        # Interface CLI + démonstrations hardcodées
└── README.md
```

---

## Structure de données : Graphe Résiduel

C'est la pièce centrale du projet. Le graphe résiduel est représenté par une **liste d'adjacence** (`dict[node → list[Arc]]`).

Chaque arc logique (i, j) du graphe original génère **deux objets `Arc` couplés** via un pointeur `arc.reverse` :

- **Arc forward** (i → j) : capacité résiduelle `u(i,j) - f(i,j)`, coût `c(i,j)`
- **Arc backward** (j → i) : capacité résiduelle `f(i,j) - l(i,j)`, coût `-c(i,j)`

Lors d'une augmentation de flot, les deux arcs sont mis à jour en **O(1)** grâce au pointeur `reverse` — sans reconstruction du graphe résiduel à chaque itération.

```
Arc original (i) ──[cap=u-f, cost=c]──▶ (j)
Arc inverse  (j) ──[cap=f-l, cost=-c]──▶ (i)
         └─── arc.reverse ───┘
```

Ce design permet :
- un accès immédiat à l'arc inverse (pas de recherche)
- une mise à jour atomique du résiduel en une passe
- une compatibilité directe avec Bellman-Ford et Dijkstra sans transformation du graphe

---

## Prérequis

- Python 3.8+
- Aucune dépendance externe pour les algorithmes
- `pytest` pour les tests : `pip install pytest`
- Graphviz pour la visualisation :
  - Mac : `brew install graphviz`
  - Linux : `apt install graphviz`

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
# Ford-Fulkerson sur un fichier
python main.py examples/simple.txt --algo ford_fulkerson

# Min cost flow Bellman-Ford
python main.py examples/assignment.txt --algo min_cost_bf

# Min cost flow Dijkstra
python main.py examples/negative_cost.txt --algo min_cost_dijkstra

# Avec visualisation PNG (génère outputs/NOM_ALGO.png)
python main.py examples/simple.txt --algo ford_fulkerson --visualize

# Démonstrations hardcodées
python main.py --demo

# Aide
python main.py --help
```

### Format du fichier d'entrée

```
# Commentaire
nodes 5          # nombre de noeuds
arc 0 1 10 2     # src dst capacité coût
arc 0 2 8 4
source 0         # noeud source
sink 4           # noeud puits
```

Le champ `coût` est optionnel (défaut : 0). Les lignes commençant par `#` sont ignorées.

### Exemples fournis

| Fichier | Description |
|---|---|
| `examples/simple.txt` | Graphe à 5 nœuds avec capacités et coûts, source=0, sink=4 |
| `examples/assignment.txt` | Graphe d'affectation (Peter, Paul, Mary → Bob, Mike, Julia), source=0, sink=7 |
| `examples/negative_cost.txt` | Graphe avec un arc de coût négatif — teste la robustesse de Bellman-Ford et la renormalisation Dijkstra |

---

## Tests

```bash
python -m pytest tests/
python -m pytest tests/ -v    # mode verbose
```

**22 tests passent**, répartis en trois fichiers :

- **`test_ford_fulkerson.py`** (7 tests) : vérifie que `max_flow == min_cut` sur plusieurs topologies (graphe simple, graphe pathologique, couplage biparti maximum, absence de chemin, arc unique).
- **`test_min_cost_flow.py`** (7 tests) : vérifie que Bellman-Ford et Dijkstra produisent des résultats identiques sur les mêmes graphes, teste la contrainte `required_flow`, le graphe diamant et les chemins parallèles.
- **`test_negative_cycle.py`** (8 tests) : vérifie la détection correcte des cycles négatifs, l'absence de faux positifs sur les arcs backward, le comportement de `assert_no_negative_cycle`, et les cas limites (nœud isolé, graphe à deux nœuds).

---

## Auteur

**Amir Benyahia** — Master Informatique 1ère année
