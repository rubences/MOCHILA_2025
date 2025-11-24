# ===========================================================
#                      TDA: VÉRTICE
# ===========================================================

class Vertex:
    def __init__(self, name):
        self.name = name
        self.edges = []
        self.distance = float('inf')
        self.previous = None

    def add_edge(self, to, weight):
        self.edges.append(Edge(self, to, weight))

    def __repr__(self):
        return f"Vertex({self.name})"


# ===========================================================
#                      TDA: ARISTA
# ===========================================================

class Edge:
    def __init__(self, src, dest, weight):
        self.src = src
        self.dest = dest
        self.weight = weight

    def __repr__(self):
        return f"{self.src.name} --{self.weight}--> {self.dest.name}"


# ===========================================================
#                      TDA: GRAFO
# ===========================================================

class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, name):
        v = Vertex(name)
        self.vertices[name] = v
        return v

    def add_edge(self, src, dest, weight):
        self.vertices[src].add_edge(self.vertices[dest], weight)

    def get_vertex(self, name):
        return self.vertices[name]


# ===========================================================
#                  DIJKSTRA (ORIENTADO A OBJETOS)
# ===========================================================

import heapq

def dijkstra(graph, start_name):
    start = graph.get_vertex(start_name)
    start.distance = 0

    pq = []
    heapq.heappush(pq, (0, start))

    while pq:
        current_dist, u = heapq.heappop(pq)

        if current_dist > u.distance:
            continue

        for edge in u.edges:
            v = edge.dest
            new_dist = u.distance + edge.weight

            if new_dist < v.distance:
                v.distance = new_dist
                v.previous = u
                heapq.heappush(pq, (new_dist, v))


# ===========================================================
#        RECONSTRUCCIÓN DEL CAMINO ÓPTIMO
# ===========================================================

def reconstruct_path(graph, start, end):
    path = []
    current = graph.get_vertex(end)

    while current is not None:
        path.append(current.name)
        current = current.previous

    return list(reversed(path))


# ===========================================================
#           LAYOUT JERÁRQUICO (según distancia)
# ===========================================================

def hierarchy_pos_by_distance(graph):
    import math

    # Agrupar nodos por distancia
    levels = {}
    for v in graph.vertices.values():
        d = v.distance if v.distance != float('inf') else math.inf
        levels.setdefault(d, []).append(v.name)

    # Ordenar distancias
    ordered_levels = sorted(levels.keys())

    pos = {}
    for level_index, dist in enumerate(ordered_levels):
        nodes = levels[dist]
        spacing = 1 / (len(nodes) + 1)
        for i, name in enumerate(nodes):
            pos[name] = (i * spacing, -level_index)

    return pos


# ===========================================================
#           DIBUJAR GRAFO COMPLETO + EXPORT PNG
# ===========================================================

import networkx as nx
import matplotlib.pyplot as plt

def draw_dijkstra_graph(graph, export_filename="dijkstra_graph.png"):
    G = nx.DiGraph()

    # añadir nodos con etiquetas
    for v in graph.vertices.values():
        label = f"{v.name}\n(dist={v.distance})"
        G.add_node(v.name, label=label)

    # añadir aristas
    for v in graph.vertices.values():
        for e in v.edges:
            G.add_edge(e.src.name, e.dest.name, weight=e.weight)

    # Layout jerárquico basado en las distancias
    pos = hierarchy_pos_by_distance(graph)

    plt.figure(figsize=(20, 12))

    nx.draw(
        G, pos,
        labels=nx.get_node_attributes(G, "label"),
        node_size=2200,
        node_color="#90caf9",
        font_size=9,
        arrowsize=20
    )

    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=nx.get_edge_attributes(G, "weight"),
        font_color="red"
    )

    plt.title("Grafo Completo — Dijkstra (distancias mínimas)")
    plt.axis("off")

    # Exportar PNG
    plt.savefig(export_filename, dpi=300, bbox_inches="tight")
    print(f"\n✅ Grafo exportado como: {export_filename}\n")

    plt.show()


# ===========================================================
#               DIBUJAR SOLO EL CAMINO ÓPTIMO
# ===========================================================

def draw_path(graph, path):
    G = nx.DiGraph()

    # añadir aristas del camino
    for i in range(len(path) - 1):
        src = graph.get_vertex(path[i])
        dest = graph.get_vertex(path[i+1])

        # buscar peso real
        for e in src.edges:
            if e.dest == dest:
                G.add_edge(src.name, dest.name, weight=e.weight)

    pos = nx.spring_layout(G, seed=7)

    plt.figure(figsize=(12, 6))

    nx.draw(
        G, pos,
        with_labels=True,
        node_size=2500,
        node_color="#81c784",
        font_size=10,
        arrowsize=25
    )

    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=nx.get_edge_attributes(G, "weight"),
        font_color="blue"
    )

    plt.title("Camino Óptimo Encontrado por Dijkstra")
    plt.axis("off")
    plt.show()


# ===========================================================
#                     PRUEBA FINAL
# ===========================================================

# Crear grafo de ejemplo
g = Graph()

for name in ["A", "B", "C", "D", "E", "F"]:
    g.add_vertex(name)

g.add_edge("A", "B", 4)
g.add_edge("A", "C", 2)
g.add_edge("B", "C", 1)
g.add_edge("B", "D", 5)
g.add_edge("C", "D", 8)
g.add_edge("C", "E", 10)
g.add_edge("D", "E", 2)
g.add_edge("D", "F", 6)
g.add_edge("E", "F", 3)

start = "A"
end = "F"

dijkstra(g, start)
path = reconstruct_path(g, start, end)

print("\n==== DISTANCIAS MÍNIMAS ====")
for v in g.vertices.values():
    print(f"{v.name}: {v.distance}")

print("\n==== CAMINO ÓPTIMO A F ====")
print(" -> ".join(path))

# Dibujar grafo completo + exportar PNG
draw_dijkstra_graph(g)

# Dibujar solo el camino óptimo
draw_path(g, path)
