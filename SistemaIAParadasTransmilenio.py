import heapq #Libreria que ayuda con la gestión de las colas
import math # Libreria que integra funciones matematicas avanzadas
            #dentro de Python

# 1. Grafo con algunas de las troncales y estaciones de Transmilenio

# En este grafo se representa cada estación a través de un nodo, donde se
# añaden características como una estación vecina, que contiene un peso; y
# unas coordenadas ficticias para hacer el cálculo posteriormente

grafo = {
    # Troncal Norte
    "Portal Norte": {"vecinos": [("Calle 127", 5)], "coord": (0, 10)},
    "Calle 127": {"vecinos": [("Calle 100", 5)], "coord": (1, 9)},
    "Calle 100": {"vecinos": [("Héroes", 6)], "coord": (2, 8)},
    "Héroes": {"vecinos": [("Calle 72", 4)], "coord": (3, 7)},
    "Calle 72": {"vecinos": [("Calle 63", 3)], "coord": (4, 6)},
    "Calle 63": {"vecinos": [("Calle 45", 4)], "coord": (5, 5)},
    "Calle 45": {"vecinos": [("Av. Jiménez", 5)], "coord": (6, 4)},

    # Avenida Jimenez
    "Av. Jiménez": {"vecinos": [("Museo del Oro", 2), ("Calle 26", 4)], "coord": (7, 3)},
    "Museo del Oro": {"vecinos": [], "coord": (8, 3)},
    "Calle 26": {"vecinos": [("Portal Américas", 15)], "coord": (7, 2)},

    # Troncal Suba
    "Portal Suba": {"vecinos": [("Suba Calle 100", 7)], "coord": (-2, 7)},
    "Suba Calle 100": {"vecinos": [("Suba Calle 80", 6)], "coord": (-1, 6)},
    "Suba Calle 80": {"vecinos": [("Héroes", 10)], "coord": (1, 7)},

    # Troncal Américas
    "Portal Américas": {"vecinos": [("Banderas", 6)], "coord": (8, 0)},
    "Banderas": {"vecinos": [("Marsella", 5)], "coord": (7, 1)},
    "Marsella": {"vecinos": [("Av. Jiménez", 12)], "coord": (7, 2)}
}

# 2. Se hace el grafo bidireccional, con el fin de que, al ejecutar el programa,
# se pueda iniciar desde cualquier estación
def hacer_bidireccional(grafo):
    nuevo_grafo = {}
    for nodo in grafo:
        nuevo_grafo[nodo] = {
            "vecinos": list(grafo[nodo]["vecinos"]),
            "coord": grafo[nodo]["coord"]
        }
    for nodo in grafo:
        for vecino, peso in grafo[nodo]["vecinos"]:
            existe = any(n == nodo for n, _ in nuevo_grafo[vecino]["vecinos"])
            if not existe:
                nuevo_grafo[vecino]["vecinos"].append((nodo, peso))
    return nuevo_grafo

# 3. Se añade la heurística para que el sistema haga una solución de la
# problemática de la forma más eficiente posible

def heuristica(nodo_actual, nodo_objetivo, grafo):
    x1, y1 = grafo[nodo_actual]["coord"]
    x2, y2 = grafo[nodo_objetivo]["coord"]
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


# 4. Reglas para un contexto variable

def aplicar_reglas(preferencia, hora, clima, grafo_original):
    nuevo_grafo = {}

    for nodo in grafo_original:
        nuevo_grafo[nodo] = {
            "vecinos": [],
            "coord": grafo_original[nodo]["coord"]
        }

        for vecino, peso in grafo_original[nodo]["vecinos"]:

            # Hora pico
            if hora == "pico":
                peso *= 1.5

            # Lluvia
            if clima == "lluvia":
                peso *= 1.3

            # Rapidez
            if preferencia == "rapido":
                peso *= 0.8

            # Menos transbordos
            if preferencia == "menos_transbordos":
                peso *= 1.2

            nuevo_grafo[nodo]["vecinos"].append((vecino, peso))

    return nuevo_grafo

# =========================================================
# 5. ALGORITMO A*
# =========================================================

def a_estrella(grafo, inicio, fin):

    cola = []
    heapq.heappush(cola, (0, inicio))

    costo_g = {nodo: float("inf") for nodo in grafo}
    costo_g[inicio] = 0

    padres = {}

    while cola:
        _, actual = heapq.heappop(cola)

        if actual == fin:
            camino = []
            while actual in padres:
                camino.append(actual)
                actual = padres[actual]
            camino.append(inicio)
            camino.reverse()
            return camino, costo_g[fin]

        for vecino, peso in grafo[actual]["vecinos"]:
            nuevo_costo = costo_g[actual] + peso

            if nuevo_costo < costo_g[vecino]:
                costo_g[vecino] = nuevo_costo

                prioridad = nuevo_costo + heuristica(vecino, fin, grafo)
                heapq.heappush(cola, (prioridad, vecino))

                padres[vecino] = actual

    return None, float("inf")

# =========================================================
# 6. SISTEMA PRINCIPAL
# =========================================================

def sistema_transmilenio():
    print("=== SISTEMA INTELIGENTE TRANSMILENIO (FINAL) ===")

    # 🔁 Convertir a bidireccional
    grafo_base = hacer_bidireccional(grafo)

    print("\nEstaciones disponibles:")
    for estacion in grafo_base:
        print("-", estacion)

    inicio = input("\nInicio: ")
    fin = input("Destino: ")

    if inicio not in grafo_base or fin not in grafo_base:
        print("❌ Estación inválida")
        return

    preferencia = input("Preferencia (rapido / menos_transbordos): ")
    hora = input("Hora (normal / pico): ")
    clima = input("Clima (normal / lluvia): ")

    # 🧠 Aplicar reglas (IA)
    grafo_modificado = aplicar_reglas(preferencia, hora, clima, grafo_base)

    # 🚀 Buscar ruta
    ruta, costo = a_estrella(grafo_modificado, inicio, fin)

    if ruta:
        print("\n✅ Ruta óptima encontrada:")
        print(" → ".join(ruta))
        print("⏱️ Tiempo estimado:", round(costo, 2), "min")
    else:
        print("❌ No se encontró ruta")

# =========================================================
# EJECUCIÓN
# =========================================================

sistema_transmilenio()