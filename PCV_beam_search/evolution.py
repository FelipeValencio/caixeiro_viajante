import random
import math
import numpy as np
import time

# Define the list of cities
# city_list = [(0, 0), (1, 2), (3, 1), (5, 2), (6, 4), (4, 6), (1, 5), (2, 3), (2, 7), (4, 0), (0, 6)]

# Define the parameters of the genetic algorithm
POPULATION_SIZE = 50
ELITE_SIZE = POPULATION_SIZE * 0.2
MUTATION_RATE = 0.2
GENERATIONS = 2000

# Config cidades
NUM_CITIES = 100
MIN_VAL = 0
MAX_VAL = 100

DEBUG = False

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


# Generate a list of random tuples.
def generate_random_tuples():
    global cities
    cities = []
    for i in range(NUM_CITIES):
        while True:
            tuple_vals = (random.randint(MIN_VAL, MAX_VAL), random.randint(MIN_VAL, MAX_VAL))
            if tuple_vals not in cities:
                break
        cities.append(tuple_vals)


# def generate_aresta_matriz():
#    global distanciaArestas
#    distanciaArestas = [[0 for x in range(NUM_CITIES)] for y in range(NUM_CITIES)]
#    for i in range(NUM_CITIES):
#        for j in range(0, NUM_CITIES):
#            distanciaArestas[i][j] = getDistance(cities[i], cities[j % len(cities)])


# Creates a random caminho through all the cities.
def create_caminho():
    caminho = random.sample(cities, len(cities))
    return caminho


# Creates a population of caminhos.
def create_population(population_size):
    population = []
    for i in range(population_size):
        while True:
            caminho = create_caminho()
            if caminho not in population:
                break
        population.append(caminho)
    return population


# Compute the distance between two cities
def getDistance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


# Compute the length of a caminho
def caminho_length(caminho):
    length = 0
    for i in range(len(caminho)):
        # consultar as distancias das arestas em uma matriz piorou a performance em mais ou menos 7x para 1000 cidades
        # length += distanciaArestas[cities.index(caminho[i])][cities.index(caminho[(i + 1) % len(caminho)])]

        # Sempre pega a proxima cidade da lista (o % eh para voltar ao comeco casa i+1 > len(caminho))
        length += getDistance(caminho[i], caminho[(i + 1) % len(caminho)])
    return length


# Selects the top elite_size caminhos as parents for mating.
def selection(population, elite_size):
    ranked_caminhos = rank_caminhos(population)
    elites = ranked_caminhos[:int(elite_size)]
    non_elites = roulette_wheel_selection(population, elite_size)
    return elites, non_elites


# Selects non-elite caminhos from the population using roulette wheel selection.
def roulette_wheel_selection(population, elite_size):
    fitness_scores = getFitness(population)
    total_fitness = 0
    for value in fitness_scores.values():
        total_fitness += value
    normalized_fitness = [score / total_fitness for score in fitness_scores.values()]
    cumulative_probabilities = list(np.cumsum(normalized_fitness))
    non_elites = []
    while len(non_elites) < len(population) - elite_size:
        r = random.random()
        for i, probability in enumerate(cumulative_probabilities):
            if r <= probability:
                if i not in non_elites:
                    non_elites.append(i)
                break
    return non_elites


# Ranks the caminhos in the population by their fitness (the shortest total distance).
def rank_caminhos(population):
    fitness_scores = getFitness(population)
    ranked_caminhos = sorted(fitness_scores.items(), key=lambda x: x[1], reverse=True)
    return [x[0] for x in ranked_caminhos]


def getFitness(population):
    fitness_scores = {}
    for i in range(len(population)):
        caminho = population[i]
        fitness_scores[i] = 1 / caminho_length(caminho)
    return fitness_scores


# Creates a mating pool of offspring for the next generation.
def mating_pool(population, elites, non_elites):
    pool = []
    for i in elites:
        pool.append(population[i])
    for i in range(len(non_elites)):
        parentElite = random.choice(elites)
        parentNonelite = random.choice(non_elites)
        child = crossover(population[parentElite], population[parentNonelite])
        pool.append(child)
    return pool


# Creates a new caminho by performing crossover between two parents.
def crossover(parent_elite, parent_nonelite):
    child = []
    # quantos genes (tuplas) serão usadas do parent elite ///
    gene_a = int(random.random() * len(parent_elite))
    gene_b = int(random.random() * len(parent_nonelite))
    start_gene = min(gene_a, gene_b)
    end_gene = max(gene_a, gene_b)
    for i in range(start_gene, end_gene):
        child.append(parent_elite[i])
    # ///
    # Os genes restantes são completos pelo pai não elite
    for i in range(len(parent_nonelite)):
        if parent_nonelite[i] not in child:
            child.append(parent_nonelite[i])
    return child


# function to apply mutation to the entire population
def mutate_population(population, mutation_rate):
    for i in range(len(population)):
        if random.random() < mutation_rate:
            population[i] = mutate(population[i])
    return population


# function to mutate a caminho by swapping two cities
def mutate(caminho):
    i, j = random.sample(range(len(caminho)), 2)
    caminho[i], caminho[j] = caminho[j], caminho[i]
    return caminho


def evolutionary():
    # Generate an initial caminho
    global bestcaminho, bestLength, bestcaminhoOverall, bestLengthOverall

    population = create_population(POPULATION_SIZE)

    caminhoRank = rank_caminhos(population)
    bestcaminho = list(population[caminhoRank[0]])
    bestLength = caminho_length(bestcaminho)

    bestcaminhoOverall = bestcaminho
    bestLengthOverall = bestLength

    # Initialize the generation counter
    generation = 0

    # Start the main loop
    while generation < GENERATIONS:

        start = time.time()

        log(f"Generation {generation + 1}")

        # log("population: " + str(population))
        log("population: ")

        # log("fitness: " + str(getFitness(population)))
        log("fitness: ")

        elites, non_elites = selection(population, ELITE_SIZE)

        # log("parents elite: " + str(elites))
        log("parents elite")
        # log("parents non_elites: " + str(non_elites))
        log("parents non_elites: ")

        pool = mating_pool(population, elites, non_elites)

        # log("next gen sem mutação: " + str(pool))
        log("next gen sem mutação: ")

        next_generation = mutate_population(pool, MUTATION_RATE)

        # log("next gen: " + str(next_generation))
        log("next gen: ")

        caminhoRank = rank_caminhos(population)
        bestcaminho = list(population[caminhoRank[0]])
        bestLength = caminho_length(bestcaminho)
        print(f"Generation {generation + 1}: Best caminho length - {bestLength} "
              f"Best Fitness - {1 / caminho_length(bestcaminho)}")

        if bestLength < bestLengthOverall:
            bestcaminhoOverall = bestcaminho
            bestLengthOverall = bestLength

        population = next_generation

        end = time.time()
        print(f"tempo Generation {generation + 1}: " + str(end - start))
        # Increment the generation counter
        generation += 1

    return bestcaminhoOverall, bestLengthOverall


if not cities:
    # Run the algorithm and print the results
    start = time.time()
    generate_random_tuples()
    end = time.time()
    print("tempo generate_random_tuples:" + str(end - start))
    log("cidades: " + str(cities))

# start = time.time()
# generate_aresta_matriz()
# end = time.time()
# print("tempo generate_aresta_matriz:" + str(end - start))

best_caminho, best_length = evolutionary()
print('melhor caminho: ' + str(best_caminho))
print('melhor distância:' + str(best_length))
