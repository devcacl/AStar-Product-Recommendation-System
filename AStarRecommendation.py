import heapq

class Producto:
    def __init__(self, nombre, categoria, probabilidad_conversion):
        self.nombre = nombre
        self.categoria = categoria
        self.probabilidad_conversion = probabilidad_conversion

    def __repr__(self):
        return f"{self.nombre} ({self.categoria})"

class AStarRecommendation:
    def __init__(self, productos, heuristica):
        self.productos = productos
        self.heuristica = heuristica  # Función heurística: probabilidad de conversión
        self.grafo = self.crear_grafo()

    def crear_grafo(self):
        # Creando un grafo simplificado de productos, donde cada producto se conecta al siguiente
        grafo = {}
        for producto in self.productos:
            grafo[producto] = [p for p in self.productos if p != producto]
        return grafo

    def a_star(self, inicio, objetivo):
        fila_prioridad = []
        heapq.heappush(fila_prioridad, (0 + self.heuristica(inicio), 0, inicio))  # f = g + h
        visitados = set()
        caminos = {}

        while fila_prioridad:
            _, g, actual = heapq.heappop(fila_prioridad)

            if actual in visitados:
                continue

            visitados.add(actual)
            if actual == objetivo:
                break

            for vecino in self.grafo[actual]:
                if vecino not in visitados:
                    h = self.heuristica(vecino)
                    heapq.heappush(fila_prioridad, (g + 1 + h, g + 1, vecino))  # g es el costo acumulado
                    caminos[vecino] = actual

        # Recuperando el camino
        camino = []
        producto = objetivo
        while producto in caminos:
            camino.insert(0, producto)
            producto = caminos[producto]
        return camino

def heuristica(producto):
    # Cuanto mayor sea la probabilidad de conversión, más atractivo será el producto
    return -producto.probabilidad_conversion  # Vamos a minimizar la heurística (cuanto menor, mejor)

# Ejemplo de productos
productos = [
    Producto("Producto A", "Categoría 1", 0.9),
    Producto("Producto B", "Categoría 1", 0.8),
    Producto("Producto C", "Categoría 2", 0.7),
    Producto("Producto D", "Categoría 2", 0.6),
]

# Creando el sistema de recomendación
recomendador = AStarRecommendation(productos, heuristica)

# Buscar el mejor camino entre dos productos
inicio = productos[0]  # Producto A
objetivo = productos[2]  # Producto C

camino_recomendado = recomendador.a_star(inicio, objetivo)

# Mostrando la recomendación
print("Camino recomendado:")
for p in camino_recomendado:
    print(p)