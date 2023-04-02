import random
import math
import numpy as np
import time

# Define the list of cities
# city_list = [(0, 0), (1, 2), (3, 1), (5, 2), (6, 4), (4, 6), (1, 5), (2, 3), (2, 7), (4, 0), (0, 6)]

# Define the parameters of the genetic algorithm
POPULATION_SIZE = 1000
ELITE_SIZE = POPULATION_SIZE * 0.2
MUTATION_RATE = 0.1
GENERATIONS = 100

# Config cidades
NUM_CITIES = 4000
MIN_VAL = 0
MAX_VAL = 100

DEBUG = True


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


def generate_aresta_matriz():
    global distanciaArestas
    distanciaArestas = [[0 for x in range(NUM_CITIES)] for y in range(NUM_CITIES)]
    for i in range(NUM_CITIES):
        for j in range(0, NUM_CITIES):
            distanciaArestas[i][j] = getDistance(cities[i], cities[j % len(cities)])


# Creates a random tour through all the cities.
def create_tour():
    tour = random.sample(cities, len(cities))
    return tour


# Creates a population of tours.
def create_population(population_size):
    population = []
    for i in range(population_size):
        while True:
            tour = create_tour()
            if tour not in population:
                break
        population.append(tour)
    return population


# Compute the distance between two cities
def getDistance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


# Compute the length of a tour
def tour_length(tour):
    length = 0
    for i in range(len(tour)):
        # consultar as distancias das arestas em uma matriz piorou a performance em mais ou menos 7x para 1000 cidades
        # length += distanciaArestas[cities.index(tour[i])][cities.index(tour[(i + 1) % len(tour)])]

        # Sempre pega a proxima cidade da lista (o % eh para voltar ao comeco casa i+1 > len(tour))
        length += getDistance(tour[i], tour[(i + 1) % len(tour)])
    return length


# Selects the top elite_size tours as parents for mating.
def selection(population, elite_size):
    ranked_tours = rank_tours(population)
    elites = ranked_tours[:int(elite_size)]
    non_elites = roulette_wheel_selection(population, elite_size)
    return elites, non_elites


# Selects non-elite tours from the population using roulette wheel selection.
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


# Ranks the tours in the population by their fitness (the shortest total distance).
def rank_tours(population):
    fitness_scores = getFitness(population)
    ranked_tours = sorted(fitness_scores.items(), key=lambda x: x[1], reverse=True)
    return [x[0] for x in ranked_tours]


def getFitness(population):
    fitness_scores = {}
    for i in range(len(population)):
        tour = population[i]
        fitness_scores[i] = 1 / tour_length(tour)
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


# Creates a new tour by performing crossover between two parents.
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


# function to mutate a tour by swapping two cities
def mutate(tour):
    i, j = random.sample(range(len(tour)), 2)
    tour[i], tour[j] = tour[j], tour[i]
    return tour


def evolutionary():
    # Generate an initial tour
    global bestTour, bestLength, bestTourOverall, bestLengthOverall

    population = create_population(POPULATION_SIZE)

    tourRank = rank_tours(population)
    bestTour = list(population[tourRank[0]])
    bestLength = tour_length(bestTour)

    bestTourOverall = bestTour
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

        #log("parents elite: " + str(elites))
        log("parents elite")
        #log("parents non_elites: " + str(non_elites))
        log("parents non_elites: ")

        pool = mating_pool(population, elites, non_elites)

        # log("next gen sem mutação: " + str(pool))
        log("next gen sem mutação: ")

        next_generation = mutate_population(pool, MUTATION_RATE)

        #log("next gen: " + str(next_generation))
        log("next gen: ")

        tourRank = rank_tours(population)
        bestTour = list(population[tourRank[0]])
        bestLength = tour_length(bestTour)
        print(f"Generation {generation + 1}: Best tour length - {bestLength}")

        if bestLength < bestLengthOverall:
            bestTourOverall = bestTour
            bestLengthOverall = bestLength

        population = next_generation

        end = time.time()
        print(f"tempo Generation {generation + 1}: " + str(end - start))
        # Increment the generation counter
        generation += 1

    return bestTourOverall, bestLengthOverall


# Run the algorithm and print the results
start = time.time()
generate_random_tuples()
end = time.time()
print("tempo generate_random_tuples:" + str(end - start))

# start = time.time()
# generate_aresta_matriz()
# end = time.time()
# print("tempo generate_aresta_matriz:" + str(end - start))

best_tour, best_length = evolutionary()
print('Best tour: ' + str(best_tour))
print('Best length:' + str(best_length))
