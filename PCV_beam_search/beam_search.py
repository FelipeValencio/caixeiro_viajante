import random
import math
import time

# Define a largura do feixe
beam_width = 3

# Defina o número máximo de iterações
max_iterations = 100

# Config cidades
NUM_CITIES = 100
MIN_VAL = 0
MAX_VAL = 100

DEBUG = True

cities = [(79, 65), (37, 90), (17, 66), (81, 98), (28, 74), (30, 37), (47, 35), (56, 23), (100, 37), (3, 47), (51, 91),
          (63, 23), (84, 70), (42, 24), (1, 84), (95, 96), (82, 9), (78, 16), (48, 2), (86, 60), (20, 1), (96, 86),
          (90, 35), (20, 49), (13, 3), (89, 71), (72, 14), (13, 94), (89, 98), (38, 81), (1, 93), (39, 40), (9, 88),
          (71, 53), (66, 45), (100, 58), (15, 27), (69, 82), (85, 70), (27, 50), (99, 64), (11, 94), (41, 67), (47, 20),
          (84, 87), (98, 69), (23, 60), (93, 61), (93, 89), (98, 27), (94, 9), (48, 89), (85, 35), (100, 14), (64, 91),
          (74, 5), (37, 95), (13, 28), (24, 81), (11, 2), (89, 84), (41, 89), (28, 69), (21, 3), (77, 64), (96, 57),
          (12, 85), (92, 54), (0, 34), (98, 17), (42, 25), (28, 39), (77, 78), (23, 30), (63, 6), (2, 42), (98, 75),
          (39, 80), (50, 54), (20, 27), (31, 88), (8, 87), (73, 10), (37, 28), (87, 71), (59, 22), (94, 69), (39, 44),
          (72, 96), (67, 86), (50, 19), (90, 93), (68, 80), (68, 76), (52, 47), (83, 73), (91, 0), (96, 31), (56, 52),
          (20, 48)]


# cities = []

def log(s):
    if DEBUG:
        print(s)


# Gera uma lista de tuplas aleatórias.
def generate_random_tuples():
    global cities
    for i in range(NUM_CITIES):
        while True:
            tuple_vals = (random.randint(MIN_VAL, MAX_VAL), random.randint(MIN_VAL, MAX_VAL))
            if tuple_vals not in cities:
                break
        cities.append(tuple_vals)


# Calcula a distância entre duas cidades, com distancia euclidiana
def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


# Calcular a distancia de um caminho
def caminho_length(caminho):
    length = 0
    for i in range(len(caminho)):
        # Sempre pega a proxima cidade da lista (o % eh para voltar ao comeco casa i+1 > len(caminho))
        length += distance(caminho[i], caminho[(i + 1) % len(caminho)])
    return length


# Gera um caminho inicial
def initial_caminho(cities):
    caminhos = []
    for i in range(beam_width):
        caminho = list(cities)
        random.shuffle(caminho)
        if caminho not in caminhos:
            caminhos.append(caminho)
    return caminhos


# Gera todos os vizinhos possiveis a partir dos k_best_neighbors
# Função que deixa o algoritmo pesado, não conseguimos encontrar maneiras de otimizar
def neighbors_caminhos(k_best_neighbors):
    neighbors = []
    for tour in k_best_neighbors:
        for i in range(len(tour)):
            for j in range(i + 1, len(tour)):
                neighbor = list(tour)
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                if neighbor not in neighbors:
                    neighbors.append(neighbor)
    # sort neighbors by score and keep only the top k
    neighbors = select_best_caminhos(neighbors, beam_width)
    return neighbors


# Seleciona os melhores k caminhos
def select_best_caminhos(caminhos, k):
    caminhos.sort(key=caminho_length)
    return caminhos[:k]


# main loop
def local_search_beam():
    global best_length, best_caminho, beam_width, max_iterations, cities
    # Gera um caminho inicial
    k_best_neighbors = initial_caminho(cities)

    # log("initial_caminho: " + str(k_best_neighbors))

    current_caminho = min(k_best_neighbors, key=caminho_length)
    best_length = caminho_length(current_caminho)

    iteration = 0

    while iteration < max_iterations:
        start = time.time()

        # Gera todos os vizinhos possiveis a partir dos k_best_neighbors e filtra os K melhores, k = beam_width
        k_best_neighbors = neighbors_caminhos(k_best_neighbors)

        log("k_best_neighbors len: " + str(len(k_best_neighbors)))

        # Seleciona o melhor caminho entre os k melhores vizinhos
        current_caminho = k_best_neighbors[0]

        # Atualiza o melhor caminho e melhor distancia
        current_length = caminho_length(current_caminho)
        if current_length < best_length:
            best_caminho = list(current_caminho)
            best_length = current_length

        print(f"Iteration {iteration + 1}: Best caminho length - {best_length}")

        iteration += 1

        end = time.time()

        print("tempo: " + str(end - start))

    return best_caminho, best_length


if not cities:
    start = time.time()
    generate_random_tuples()
    end = time.time()
    print("tempo generate_random_tuples:" + str(end - start))
log("cidades: " + str(cities))

# Executa o algoritmo e imprime os resultados
best_caminho, best_length = local_search_beam()
print('Best caminho:', best_caminho)
print('Best length:', best_length)
