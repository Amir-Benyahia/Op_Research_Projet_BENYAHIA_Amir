# Visualisation Graphviz : genere un .dot puis appelle dot pour faire un .png
# vert = arc utilise, rouge = sature, noir = inutilise

import os
import subprocess


def generate_dot(graph, title="Graph", node_names=None, show_costs=True):
    """Construit le contenu du fichier .dot."""
    lines = [f'digraph "{title}" {{']
    lines.append('  rankdir=LR;')
    lines.append('  node [shape=circle];')

    for node in graph.adj:
        if node_names:
            label = node_names[node]
        else:
            label = str(node)
        lines.append(f'  {node} [label="{label}"];')

    seen = set()
    for node in graph.adj:
        for arc in graph.adj[node]:
            original_cap = arc.capacity + arc.flow
            if original_cap <= 0:
                continue
            arc_id = (arc.src, arc.dst)
            if arc_id in seen:
                continue
            seen.add(arc_id)

            label = f"{arc.flow}/{original_cap}"
            if show_costs:
                label += f", {arc.cost}"

            # couleur en fonction de l'utilisation
            if arc.flow == original_cap:
                color = "red"
            elif arc.flow > 0:
                color = "green"
            else:
                color = "black"

            lines.append(
                f'  {arc.src} -> {arc.dst} '
                f'[label="{label}", color="{color}", fontcolor="{color}"];'
            )

    lines.append("}")
    return "\n".join(lines)


def visualize(graph, output_path="output", title="Graph", node_names=None, show_costs=True):
    """Genere output.dot et output.png. Necessite Graphviz (brew install graphviz)."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    dot_content = generate_dot(graph, title, node_names, show_costs)
    dot_path = output_path + ".dot"
    png_path = output_path + ".png"

    with open(dot_path, "w") as f:
        f.write(dot_content)

    try:
        subprocess.run(["dot", "-Tpng", dot_path, "-o", png_path], check=True, capture_output=True)
        print(f"  Image générée : {png_path}")
    except FileNotFoundError:
        print("  Graphviz non installé. Lance : brew install graphviz")
    except subprocess.CalledProcessError as e:
        print(f"  Erreur Graphviz : {e}")

    return dot_path, png_path
