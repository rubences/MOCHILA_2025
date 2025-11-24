# -------------------------------------------------------
# TDA: Item (objeto de Star Wars)
# -------------------------------------------------------

class Item:
    def __init__(self, name, weight, priority):
        self.name = name
        self.weight = weight
        self.priority = priority

    def __repr__(self):
        return f"{self.name} (W:{self.weight}, P:{self.priority})"


# -------------------------------------------------------
# TDA: Node del grafo
# -------------------------------------------------------

class Node:
    def __init__(self, index, weight, priority):
        self.index = index        # índice del objeto considerado
        self.weight = weight      # peso acumulado
        self.priority = priority  # prioridad acumulada
        
        self.edges = []           # aristas hacia nodos hijos

        # Datos para reconstrucción elegante
        self.parent = None        # nodo padre
        self.action = None        # "take" o "skip"

    def add_edge(self, edge):
        self.edges.append(edge)


# -------------------------------------------------------
# TDA: Edge (transición entre nodos)
# -------------------------------------------------------

class Edge:
    def __init__(self, next_node, decision):
        self.next_node = next_node
        self.decision = decision  # "take" o "skip"


# -------------------------------------------------------
# TDA: Grafo completo (grafo de decisiones)
# -------------------------------------------------------

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

            # si ya consideramos todos los objetos, no expandimos más
            if current.index == len(self.items):
                continue

            item = self.items[current.index]

            # ----------------------------------------------------
            # Opción 1: NO TOMAR (skip)
            # ----------------------------------------------------
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

            # ----------------------------------------------------
            # Opción 2: TOMAR (take) si el peso lo permite
            # ----------------------------------------------------
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


# -------------------------------------------------------
# Solucionador de la mochila mediante grafo
# -------------------------------------------------------

class KnapsackSolver:
    def __init__(self, graph):
        self.graph = graph

    def solve(self):

        best_node = None
        best_priority = -1

        stack = [self.graph.start]

        # -----------------------------------------------
        # Buscar el nodo con mayor prioridad
        # -----------------------------------------------
        while stack:
            current = stack.pop()

            # nodo terminal
            if current.index == len(self.graph.items):
                if current.priority > best_priority:
                    best_priority = current.priority
                    best_node = current

            for edge in current.edges:
                stack.append(edge.next_node)

        # -----------------------------------------------
        # ⭐ Reconstrucción elegante mediante parent
        # -----------------------------------------------
        path = []
        node = best_node

        while node.parent is not None:
            item_index = node.parent.index
            item = self.graph.items[item_index]

            path.append((node.action, item))
            node = node.parent

        path.reverse()
        return path, best_priority


# -------------------------------------------------------
# PRUEBA COMPLETA — STAR WARS
# -------------------------------------------------------

items = [
    Item("Sable de luz", 5, 90),
    Item("Holoproyector", 2, 40),
    Item("Bláster DL-44", 4, 70),
    Item("Herramientas de reparación", 3, 50),
    Item("Mini-dron de reconocimiento", 6, 85)
]

capacity = 15

# Construcción del grafo
graph = Graph(items, capacity)
graph.build()

# Resolver
solver = KnapsackSolver(graph)
solution, total_priority = solver.solve()

# Imprimir resultados
print("\n===========================")
print("   SOLUCIÓN ÓPTIMA")
print("===========================\n")

for action, item in solution:
    accion = "Tomar" if action == "take" else "Saltar"
    print(f"{accion}: {item}")

print(f"\nPrioridad total lograda: {total_priority}")
print("===========================\n")
