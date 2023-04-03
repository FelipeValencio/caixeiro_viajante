import random
import math
import time

# Define a largura do feixe
beam_width = 3

# Defina o número máximo de iterações
max_iterations = 100

# Config cidades
NUM_CITIES = 1000
MIN_VAL = 0
MAX_VAL = 100

DEBUG = True


def log(s):
    if DEBUG:
        print(s)


# Gera uma lista de tuplas aleatórias.
def generate_random_tuples():
    tuples = []
    for i in range(NUM_CITIES):
        while True:
            tuple_vals = (random.randint(MIN_VAL, MAX_VAL), random.randint(MIN_VAL, MAX_VAL))
            if tuple_vals not in tuples:
                break
        tuples.append(tuple_vals)
    return tuples


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


# Select the k best tours
def select_best_caminhos(caminhos, k):
    caminhos.sort(key=caminho_length)
    return caminhos[:k]


# main loop
def local_search_beam(cities):
    global best_length, best_caminho, beam_width, max_iterations
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


# Executa o algoritmo e imprime os resultados
best_caminho, best_length = local_search_beam(generate_random_tuples())
print('Best caminho:', best_caminho)
print('Best length:', best_length)
