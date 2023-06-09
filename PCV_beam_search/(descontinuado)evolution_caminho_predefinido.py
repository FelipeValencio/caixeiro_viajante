import random
import math
import numpy as np

# Define the list of cities
# city_list = [(0, 0), (1, 2), (3, 1), (5, 2), (6, 4), (4, 6), (1, 5), (2, 3), (2, 7), (4, 0), (0, 6)]

# Define the parameters of the genetic algorithm
POPULATION_SIZE = 100
ELITE_SIZE = POPULATION_SIZE * 0.2
MUTATION_RATE = 0.1
GENERATIONS = 1000

# Config cidades
NUM_CITIES = 100
NUM_ARESTAS = int((NUM_CITIES * (NUM_CITIES - 1)) / 2)
MIN_VAL = 0
MAX_VAL = 100

DEBUG = False

lista_arestas = []


def log(s):
    if DEBUG:
        print(s)


def generate_random_tuples():
    """
    Generate a list of random tuples.

    Args:
    - num_tuples (int): the number of tuples to generate
    - min_val (int): the minimum value for each element in the tuple
    - max_val (int): the maximum value for each element in the tuple

    Returns:
    - A list of num_tuples tuples, where each tuple contains random values between min_val and max_val.
    """
    tuples = []
    for i in range(NUM_CITIES):
        while True:
            tuple_vals = (random.randint(MIN_VAL, MAX_VAL), random.randint(MIN_VAL, MAX_VAL))
            if tuple_vals not in tuples:
                break
        tuples.append(tuple_vals)
    return tuples


# Gera arestas aleatórias, o grafo sempre sera conexo pois todas as cidades se conectam a pelo menos um outro grafo
# nao eh possivel laços nem arestas duplas entre dois grafos
def generate_random_arestas():
    for i in range(1, NUM_ARESTAS):
        while True:
            aresta = (random.randint(0, NUM_CITIES - 1),
                      random.choice([x for x in range(0, NUM_CITIES - 1) if x not in [i]]))
            if aresta not in lista_arestas and aresta[::-1] not in lista_arestas and aresta[0] != aresta[1]:
                break
        lista_arestas.append(aresta)


# Creates a random caminho through all the cities.
def create_caminho(cities):
    while True:
        caminho = random.sample(cities, len(cities))
        count_control = 0
        for i in range(0, len(caminho)):
            if (cities.index(caminho[i]), cities.index(caminho[(i + 1) % len(caminho)])) in lista_arestas \
                    or (cities.index(caminho[(i + 1) % len(caminho)]), cities.index(caminho[i])) in lista_arestas:
                count_control += 1
        if count_control == len(caminho):
            return caminho


# Creates a population of caminhos.
def create_population(cities, population_size):
    population = []
    for i in range(population_size):
        while True:
            caminho = create_caminho(cities)
            if caminho not in population:
                break
        population.append(caminho)
    return population


# Compute the distance between two cities
def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


# Compute the length of a caminho
def caminho_length(caminho):
    length = 0
    for i in range(len(caminho)):
        # Sempre pega a proxima cidade da lista (o % eh para voltar ao comeco casa i+1 > len(caminho))
        length += distance(caminho[i], caminho[(i + 1) % len(caminho)])
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


def evolutionary(cities):
    # Generate an initial caminho
    global bestcaminho, bestLength, bestcaminhoOverall, bestLengthOverall

    generate_random_arestas()

    population = create_population(cities, POPULATION_SIZE)

    caminhoRank = rank_caminhos(population)
    bestcaminho = list(population[caminhoRank[0]])
    bestLength = caminho_length(bestcaminho)

    bestcaminhoOverall = bestcaminho
    bestLengthOverall = bestLength

    # Initialize the generation counter
    generation = 0

    # Start the main loop
    while generation < GENERATIONS:
        log(f"Generation {generation + 1}")

        log("population: " + str(population))

        log("fitness: " + str(getFitness(population)))

        elites, non_elites = selection(population, ELITE_SIZE)

        log("parents elite: " + str(elites))
        log("parents non_elites: " + str(non_elites))

        pool = mating_pool(population, elites, non_elites)

        log("next gen sem mutação: " + str(pool))

        next_generation = mutate_population(pool, MUTATION_RATE)

        log("next gen: " + str(next_generation))

        caminhoRank = rank_caminhos(population)
        bestcaminho = list(population[caminhoRank[0]])
        bestLength = caminho_length(bestcaminho)
        print(f"Generation {generation + 1}: Best caminho length - {bestLength}")

        if bestLength < bestLengthOverall:
            bestcaminhoOverall = bestcaminho
            bestLengthOverall = bestLength

        population = next_generation

        # Increment the generation counter
        generation += 1

    return bestcaminhoOverall, bestLengthOverall


# Run the algorithm and print the results
best_caminho, best_length = evolutionary(generate_random_tuples())
print('Best caminho: ' + str(best_caminho))
print('Best length:' + str(best_length))
