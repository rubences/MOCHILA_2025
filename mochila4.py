# =======================================================
#                  TDA: Item (Star Wars)
# =======================================================

class Item:
    def __init__(self, name, weight, priority):
        self.name = name
        self.weight = weight
        self.priority = priority

    def __repr__(self):
        return f"{self.name} (W:{self.weight}, P:{self.priority})"


# =======================================================
#                  TDA: Node (estado)
# =======================================================

class Node:
    def __init__(self, index, weight, priority):
        self.index = index
        self.weight = weight
        self.priority = priority
        self.edges = []

        # Para reconstrucción elegante
        self.parent = None
        self.action = None

    def add_edge(self, edge):
        self.edges.append(edge)


# =======================================================
#                  TDA: Edge
# =======================================================

class Edge:
    def __init__(self, next_node, decision):
        self.next_node = next_node
        self.decision = decision


# =======================================================
#                  TDA: Graph
# =======================================================

class Graph:
    def __init__(self, items, capacity):
        self.items = items
        self.capacity = capacity
        self.start = Node(0, 0, 0)
        self.nodes = [self.start]

    def build(self):
        queue = [self.start]

        while queue:
            current = queue.pop(0)

            if current.index == len(self.items):
                continue

            item = self.items[current.index]

            # ------------------------------------------
            # NO TOMAR (skip)
            # ------------------------------------------
            skip_node = Node(
                current.index + 1,
                current.weight,
                current.priority
            )
            skip_node.parent = current
            skip_node.action = "skip"

            self.nodes.append(skip_node)
            current.add_edge(Edge(skip_node, "skip"))
            queue.append(skip_node)

            # ------------------------------------------
            # TOMAR (take) solo si cabe
            # ------------------------------------------
            if current.weight + item.weight <= self.capacity:

                take_node = Node(
                    current.index + 1,
                    current.weight + item.weight,
                    current.priority + item.priority
                )
                take_node.parent = current
                take_node.action = "take"

                self.nodes.append(take_node)
                current.add_edge(Edge(take_node, "take"))
                queue.append(take_node)


# =======================================================
#                  Solver
# =======================================================

class KnapsackSolver:
    def __init__(self, graph):
        self.graph = graph

    def solve(self):
        best_node = None
        best_priority = -1

        stack = [self.graph.start]

        while stack:
            current = stack.pop()

            if current.index == len(self.graph.items):
                if current.priority > best_priority:
                    best_priority = current.priority
                    best_node = current

            for edge in current.edges:
                stack.append(edge.next_node)

        # reconstrucción elegante
        path = []
        node = best_node

        while node.parent is not None:
            item_index = node.parent.index
            item = self.graph.items[item_index]
            path.append((node.action, item))
            node = node.parent

        path.reverse()
        return path, best_priority


# =======================================================
#               FUNCIONES DE DIBUJO
# =======================================================

import networkx as nx
import matplotlib.pyplot as plt


# ---------------- Hierarchical Layout (tipo árbol) -------------------
def hierarchy_pos(G, root):

    layers = {}
    for node in G.nodes():
        layers[node] = G.nodes[node]['level']

    pos = {}
    max_layer = max(layers.values())

    # grupos por nivel
    levels = {}
    for node, level in layers.items():
        levels.setdefault(level, []).append(node)

    # distribución horizontal
    for level, nodes in levels.items():
        spacing = 1 / (len(nodes) + 1)
        for i, node in enumerate(nodes):
            pos[node] = (i * spacing, -level)

    return pos


# ---------------- Grafo completo ORDENADO + export PNG -------------------

def draw_full_graph_hierarchical(graph, export_filename="grafo_mochila.png"):

    G = nx.DiGraph()

    # añadir nodos con niveles
    for node in graph.nodes:
        label = f"(i={node.index}, W={node.weight}, P={node.priority})"
        G.add_node(id(node), label=label, level=node.index)

    # añadir aristas
    for node in graph.nodes:
        for edge in node.edges:
            G.add_edge(id(node), id(edge.next_node), label=edge.decision)

    # layout jerárquico
    pos = hierarchy_pos(G, id(graph.start))

    plt.figure(figsize=(20, 12))
    nx.draw(
        G, pos,
        labels=nx.get_node_attributes(G, 'label'),
        node_size=2000,
        node_color="#90caf9",
        font_size=8,
        arrowsize=20
    )

    nx.draw_networkx_edge_labels(G, pos, nx.get_edge_attributes(G, 'label'), font_color='red')

    plt.title("Grafo Completo del Problema de la Mochila (Star Wars)\nLayout Jerárquico")
    plt.axis("off")

    # ----------- EXPORTAR A PNG -----------
    plt.savefig(export_filename, dpi=300, bbox_inches='tight')
    print(f"\n✅ Grafo exportado como: {export_filename}\n")

    plt.show()


# ---------------------- Camino óptimo -----------------------------

def draw_solution_path(graph, solution):
    G = nx.DiGraph()

    current = graph.start
    nodes = [current]

    # reconstruir nodos usados en el camino
    for action, item in solution:
        for e in current.edges:
            if e.decision == action:
                next_node = e.next_node
                G.add_edge(id(current), id(next_node), label=action)
                nodes.append(next_node)
                current = next_node
                break

    labels = {id(n): f"(i={n.index}, W={n.weight}, P={n.priority})" for n in nodes}

    pos = nx.spring_layout(G, seed=7)

    plt.figure(figsize=(14, 7))
    nx.draw(
        G, pos, with_labels=True, labels=labels,
        node_size=2500, node_color="#81c784",
        arrowsize=25, font_size=9
    )

    nx.draw_networkx_edge_labels(G, pos, nx.get_edge_attributes(G, 'label'), font_color='blue')

    plt.title("Camino Óptimo — Problema de la Mochila (Star Wars)")
    plt.axis("off")
    plt.show()


# =======================================================
#                     PRUEBA FINAL
# =======================================================

items = [
    Item("Sable de luz", 5, 90),
    Item("Holoproyector", 2, 40),
    Item("Bláster DL-44", 4, 70),
    Item("Herramientas de reparación", 3, 50),
    Item("Mini-dron de reconocimiento", 6, 85)
]

capacity = 15

graph = Graph(items, capacity)
graph.build()

solver = KnapsackSolver(graph)
solution, total_priority = solver.solve()

print("\n=============================")
print("       SOLUCIÓN ÓPTIMA")
print("=============================\n")

for action, item in solution:
    print(f"{'Tomar' if action=='take' else 'Saltar'} → {item}")

print(f"\nPrioridad total: {total_priority}")
print("=============================\n")

# -------------------------------------------------------
# DIBUJAR grafo completo + exportar PNG
# -------------------------------------------------------
draw_full_graph_hierarchical(graph)

# -------------------------------------------------------
# DIBUJAR camino óptimo
# -------------------------------------------------------
draw_solution_path(graph, solution)
