
import random
from ga_config import POPULATION_SIZE, NUM_GENERATIONS, MUTATION_RATE, CROSSOVER_RATE, ELITE_PERCENT, SURVIVOR_PERCENT
from ga_utils import generate_initial_population, generate_random_chromosome, crossover, mutate
from fitness_function import fitness


def run_ga():
    population = generate_initial_population()
    best_chromosome = None
    best_fitness = float('-inf')

    for generation in range(NUM_GENERATIONS):
        # Evaluate fitness for all
        scored_population = [(chrom, fitness(chrom)) for chrom in population]
        scored_population.sort(key=lambda x: x[1], reverse=True)

        # Keep best chromosome
        top_chromosome, top_score = scored_population[0]
        if top_score > best_fitness:
            best_chromosome = top_chromosome
            best_fitness = top_score

        # Select Elites
        num_elites = int(POPULATION_SIZE * ELITE_PERCENT)
        elites = [chrom for chrom, score in scored_population[:num_elites]]

        # Cull bottom chromosomes
        survivor_count = int(SURVIVOR_PERCENT * POPULATION_SIZE)
        survivors = [chrom for chrom, score in scored_population[:survivor_count]]

        # Crossover
        num_crossovers = int(POPULATION_SIZE * CROSSOVER_RATE)
        for _ in range(num_crossovers):   # Using '_' because the loop variable is not needed just repeat this block N times
            p1, p2 = random.sample(survivors, 2)
            c1, c2 = crossover(p1, p2)
            survivors.append(c1)
            survivors.append(c2)

        # Mutation
        num_mutations = int(POPULATION_SIZE * MUTATION_RATE)
        for _ in range(num_mutations):
            idx = random.randint(0, len(survivors) - 1)
            survivors[idx] = mutate(survivors[idx])

        # Add missing elites if mutated
        for elite in elites:
          if elite not in survivors:
            survivors.append(elite)

        # Fill with new chromosomes
        while len(survivors) < POPULATION_SIZE:
          new_chromosome = generate_random_chromosome()
          survivors.append(new_chromosome)

        population = survivors

        print(f"Gen {generation + 1:03d} | Best Score: {round(top_score, 2)} | Best Chromosome: {top_chromosome}")

    return best_chromosome, best_fitness
