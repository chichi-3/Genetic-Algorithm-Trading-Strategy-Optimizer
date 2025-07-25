

import random
from ga_config import PARAM_RANGES, GENE_KEYS, POPULATION_SIZE

def random_gene(key):
    value_range = PARAM_RANGES[key]

    if isinstance(value_range, list):  # Categorical (e.g., MA type)
        return random.choice(value_range)

    elif isinstance(value_range[0], int):  # Integer range
        return random.randint(value_range[0], value_range[1])

    elif isinstance(value_range[0], float):  # Float range
        precision = 1
        steps = int((value_range[1] - value_range[0]) * (10 ** precision)) + 1
        return round(random.randint(0, steps - 1) * (10 ** -precision) + value_range[0], precision)

def generate_random_chromosome():
    return [random_gene(key) for key in GENE_KEYS]

def generate_initial_population():
    return [generate_random_chromosome() for _ in range(POPULATION_SIZE)]

def mutate(chromosome):
    mutated = chromosome.copy()
    gene_index = random.randint(0, len(GENE_KEYS) - 1)
    key = GENE_KEYS[gene_index]
    mutated[gene_index] = random_gene(key)
    return mutated

def crossover(parent1, parent2):
    point = random.randint(1, len(GENE_KEYS) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2
