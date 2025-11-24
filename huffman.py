# ===========================================================
#               TDA: Nodo del Árbol de Huffman
# ===========================================================

class HuffmanNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char      # carácter
        self.freq = freq      # frecuencia
        self.left = left
        self.right = right


    def is_leaf(self):
        return self.left is None and self.right is None


# ===========================================================
#               Clase Huffman (construcción + códigos)
# ===========================================================

import heapq

class HuffmanTree:
    def __init__(self, freq_table):
        self.freq_table = freq_table
        self.root = None
        self.codes = {}

    # Construcción del árbol de Huffman
    def build(self):
        pq = []

        # Convertir tabla de frecuencias en nodos
        for char, freq in self.freq_table.items():
            heapq.heappush(pq, (freq, HuffmanNode(char, freq)))

        # Construir árbol
        while len(pq) > 1:
            freq1, left = heapq.heappop(pq)
            freq2, right = heapq.heappop(pq)

            new_node = HuffmanNode(None, freq1 + freq2, left, right)
            heapq.heappush(pq, (new_node.freq, new_node))

        # Raíz del árbol
        self.root = pq[0][1]

    # Generación de códigos Huffman
    def generate_codes(self):

        def traverse(node, prefix):
            if node.is_leaf():
                self.codes[node.char] = prefix
                return

            traverse(node.left, prefix + "0")
            traverse(node.right, prefix + "1")

        traverse(self.root, "")
        return self.codes


# ===========================================================
#        DIBUJO DEL ÁRBOL COMPLETO — JERÁRQUICO + PNG
# ===========================================================

import networkx as nx
import matplotlib.pyplot as plt


# ---------------- Calcular niveles del árbol ----------------

def compute_levels(node, level, levels_dict):
    if node is None:
        return
    levels_dict[node] = level
    compute_levels(node.left,  level + 1, levels_dict)
    compute_levels(node.right, level + 1, levels_dict)


# --------------- Layout jerárquico estilo árbol ---------------

def hierarchy_pos(G, root):

    layers = {}
    for node in G.nodes:
        layers[node] = G.nodes[node]["level"]

    pos = {}
    max_layer = max(layers.values())

    # Agrupar nodos por nivel
    levels = {}
    for node, level in layers.items():
        levels.setdefault(level, []).append(node)

    # Distribución horizontal uniforme
    for level, nodes in levels.items():
        spacing = 1 / (len(nodes) + 1)
        for i, node in enumerate(nodes):
            pos[node] = (i * spacing, -level)

    return pos


# --------------- Dibujar y exportar a PNG ----------------

def draw_huffman_tree(tree, export_filename="huffman_tree.png"):

    G = nx.DiGraph()
    levels = {}

    # calcular niveles para layout
    compute_levels(tree.root, 0, levels)

    # crear nodos del gráfico
    for node, level in levels.items():
        if node.is_leaf():
            label = f"{node.char} ({node.freq})"
        else:
            label = f"* ({node.freq})"

        G.add_node(id(node), label=label, level=level)

        if node.left:
            G.add_edge(id(node), id(node.left), label="0")
        if node.right:
            G.add_edge(id(node), id(node.right), label="1")

    pos = hierarchy_pos(G, id(tree.root))

    plt.figure(figsize=(20, 12))

    nx.draw(
        G, pos,
        labels=nx.get_node_attributes(G, "label"),
        node_size=2000,
        node_color="#90caf9",
        font_size=8,
        arrowsize=20
    )

    nx.draw_networkx_edge_labels(
        G, pos,
        nx.get_edge_attributes(G, "label"),
        font_color="red"
    )

    plt.title("Árbol de Huffman — Layout Jerárquico")
    plt.axis("off")

    # EXPORTAR A PNG
    plt.savefig(export_filename, dpi=300, bbox_inches="tight")
    print(f"\n✅ Árbol de Huffman exportado como: {export_filename}\n")

    plt.show()


# ===========================================================
#                     PRUEBA FINAL
# ===========================================================

freq_table = {
    "A": 5,
    "B": 9,
    "C": 12,
    "D": 13,
    "E": 16,
    "F": 45
}

# Construcción
huffman = HuffmanTree(freq_table)
huffman.build()
codes = huffman.generate_codes()

print("===== CÓDIGOS HUFFMAN OBTENIDOS =====\n")
for char, code in codes.items():
    print(f"{char}: {code}")

# Dibujar y exportar PNG
draw_huffman_tree(huffman)
