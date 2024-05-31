import numpy as np
import konstante as konst
import random
import math
import objekti as obj
import inputs as inp
import copy
import multiprocessing


def crossover(elite_parent, non_elite_parent):
    offspring = []
    for i in range(2*inp.number_of_boxes): #length of a chromosome
        if np.random.uniform(0.0, 1.0) < konst.prob_crossover:
            offspring.append(elite_parent[i])
        else:
            offspring.append(non_elite_parent[i])
    return offspring

def mating(elites, non_elites):
    offspring_list = []
    for _ in range(konst.num_of_offsprings): #number of offsprings in each generation
        elite_parent = random.choice(elites) #selecting a random elite parent
        non_elite_parent = random.choice(non_elites) #selecting a random non-elite parent
        offspring = crossover(elite_parent, non_elite_parent)
        offspring_list.append(offspring)
    return offspring_list

def generate_chromosome():
    chromosome = []
    for _ in range(2*inp.number_of_boxes): #length of a chromosome is 2*n where n is the number of items to be packed
        chromosome.append(np.random.uniform(low=0.0, high=1.0))
    return chromosome

def mutation():
    mutants = []
    for _ in range(konst.num_mutants):
        mutant = generate_chromosome()
        mutants.append(mutant)
    return mutants


# def calculate_fitness(chromosome):
#     bins = copy.deepcopy(inp.bins)
#     boxes = copy.deepcopy(inp.boxes)
#     placement = obj.placement_procedure(chromosome[inp.number_of_boxes:], chromosome[:inp.number_of_boxes], bins, boxes)
#     fitness = obj.fitness_function(bins)
#     return fitness

# def cal_fitness(population):
#     with multiprocessing.Pool() as pool:
#         fitness_list = pool.map(calculate_fitness, population)
#     return fitness_list

def cal_fitness(population):
    fitness_list = list()
    for chromosome in population:
        bins = copy.deepcopy(inp.bins)
        boxes = copy.deepcopy(inp.boxes)
        placement = obj.placement_procedure(chromosome[inp.number_of_boxes:], chromosome[:inp.number_of_boxes], bins, boxes)
        fitness = obj.fitness_function(bins)
        fitness_list.append(fitness)
    return fitness_list

def evolutionary_process():

    population = []
    for _ in range(konst.num_individuals):
        chromosome = generate_chromosome()
        population.append(chromosome)

    fitness_list = cal_fitness(population)

    best_fitness = np.min(fitness_list)
    best_chromosome = population[np.argmin(fitness_list)]
    best_iteration = 0


    for g in range(konst.num_generations):

        sorted = np.argsort(fitness_list)
        
        elites = []
        for i in range(konst.num_elites):
            elites.append(population[sorted[i]])

        non_elites = []
        for i in range(konst.num_elites, konst.num_individuals):
            non_elites.append(population[sorted[i]])

        offsprings = mating(elites, non_elites)
        mutants = mutation()

        offspring_fitness_list = cal_fitness(offsprings)
        mutants_fitness_list = cal_fitness(mutants)
        elite_fitness_list = []
        for i in range(konst.num_elites):
            elite_fitness_list.append(fitness_list[sorted[i]])

        fitness_list = elite_fitness_list + offspring_fitness_list + mutants_fitness_list
        population = elites + mutants + offsprings

        best_fitness_population = np.inf
        for i in range(konst.num_individuals):
            if fitness_list[i] < best_fitness_population:
                best_fitness_population = fitness_list[i]


        if best_fitness_population < best_fitness:
            best_fitness = best_fitness_population
            best_iteration = g
            best_chromosome = population[np.argmin(fitness_list)]
            print(f'Generation: {g} \t Best Fitness: {best_fitness}')
        elif g % 50 == 0:
            print (f'Generation: {g} \t Best Fitness: {best_fitness}')
        #print(f'Generation: {g} \t Best Fitness: {best_fitness}')

def main():
    evolutionary_process()

if __name__ == "__main__":
    main()