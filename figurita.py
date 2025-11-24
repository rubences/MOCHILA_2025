import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(graph):
    G = nx.DiGraph()

    # Crear nodos con etiquetas
    for node in graph.nodes:
        label = f"(i={node.index}, W={node.weight}, P={node.priority})"
        G.add_node(id(node), label=label)

    # Crear aristas
    for node in graph.nodes:
        for edge in node.edges:
            G.add_edge(
                id(node), id(edge.next_node),
                label=edge.decision
            )

    pos = nx.spring_layout(G, seed=42)  # diseño automático agradable

    plt.figure(figsize=(16, 10))

    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, node_size=1200, node_color="#90caf9")

    # Dibujar aristas
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20)

    # Dibujar etiquetas de nodos
    labels = nx.get_node_attributes(G, 'label')
    nx.draw_networkx_labels(G, pos, labels, font_size=8)

    # Dibujar etiquetas de aristas
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_color='red')

    plt.title("Grafo de decisiones — Problema de la Mochila (Star Wars)")
    plt.axis('off')
    plt.show()
