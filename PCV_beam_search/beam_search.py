import random
import math
import time

# Define the cities as a list of (x, y) coordinates
# cities = [(0, 0), (1, 2), (3, 1), (5, 2), (6, 4), (4, 6), (1, 5), (2, 3), (2, 7), (4, 0), (0, 6)]

# Define the beam width
beam_width = 2

# Define the maximum number of iterations without improvement
max_iterations = 100

# Config cidades
NUM_CITIES = 10
MIN_VAL = 0
MAX_VAL = 100

DEBUG = False


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


# Compute the distance between two cities
def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


# Compute the length of a tour
def tour_length(tour):
    length = 0
    for i in range(len(tour)):
        # Sempre pega a proxima cidade da lista (o % eh para voltar ao comeco casa i+1 > len(tour))
        length += distance(tour[i], tour[(i + 1) % len(tour)])
    return length


# Generate an initial tour
def initial_tour(cities):
    tour = list(cities)
    random.shuffle(tour)
    return tour


# Generate all possible neighboring tours
def neighboring_tours(tour):
    neighbors = []
    for i in range(len(tour)):
        for j in range(i + 1, len(tour)):
            neighbor = list(tour)
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)

    return neighbors


# Select the k best tours
def select_best_tours(tours, k):
    tours.sort(key=tour_length)
    return tours[:k]


# Local search beam algorithm
def local_search_beam(cities, beam_width, max_iterations):
    # Generate an initial tour
    current_tour = initial_tour(cities)

    # Initialize the best tour and the best length
    best_tour = list(current_tour)
    best_length = tour_length(best_tour)

    # Initialize the iteration counter
    iteration = 0

    # Start the main loop
    while iteration < max_iterations:
        start = time.time()
        # Generate all possible neighboring tours
        neighbors = neighboring_tours(current_tour)

        # Select the best k neighbors
        k_best_neighbors = select_best_tours(neighbors, beam_width)

        # Select the best tour among the k best neighbors
        current_tour = min(k_best_neighbors, key=tour_length)

        # Update the best tour and the best length
        current_length = tour_length(current_tour)
        if current_length < best_length:
            best_tour = list(current_tour)
            best_length = current_length
            iteration -= 1

        print(f"Iteration {iteration + 1}: Best tour length - {best_length}")

        # Aumenta o contador quando o score não melhora
        iteration += 1

        end = time.time()

        log("tempo:" + str(end - start))

    return best_tour, best_length


# Run the algorithm and print the results
best_tour, best_length = local_search_beam(generate_random_tuples(), beam_width, max_iterations)
print('Best tour:', best_tour)
print('Best length:', best_length)
