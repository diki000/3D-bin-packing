import numpy as np
import konstante as konst
import random
import math
import objekti as obj
import inputs_import as inp
import copy
import multiprocessing
import matplotlib.pyplot as plt

def crossover(elite_parent, non_elite_parent): #pokazao se loš
    offspring = []
    for i in range(2*inp.number_of_boxes + inp.number_of_bins): #length of a chromosome
        if np.random.uniform(0.0, 1.0) < konst.prob_crossover:
            offspring.append(elite_parent[i])
        else:
            offspring.append(non_elite_parent[i])
    return offspring

def crossover_2(elite_parent, non_elite_parent):
    point = random.randint(1, len(elite_parent) - 1)
    child1 = np.concatenate((elite_parent[:point], non_elite_parent[point:]))
    child2 = np.concatenate((non_elite_parent[:point], elite_parent[point:]))
    return child1, child2


def sbx_crossover(elite_parent, non_elite_parent): #pokazao se loš
    offspring = []
    for i in range(2*inp.number_of_boxes + inp.number_of_bins): #length of a chromosome
        if np.random.uniform(0.0, 1.0) < konst.prob_crossover:
            beta = np.random.uniform(0.0, 1.0)
            if beta <= 0.5:
                beta = math.pow(2.0*beta, 1.0/(konst.eta_crossover + 1.0))
            else:
                beta = math.pow(0.5 / (1.0 - beta), 1.0 / (konst.eta_crossover + 1.0))
            
            if beta < 0:
                beta = 0
            elif beta > 1:
                beta = 1

            offspring.append(0.5 * ((1 + beta) * elite_parent[i] + (1 - beta) * non_elite_parent[i]))
        else:
            offspring.append(non_elite_parent[i])
    return offspring

def select(population, fitnesses, k=3):
    selected = random.sample(list(zip(population, fitnesses)), k)
    selected.sort(key=lambda x: x[1])
    return selected[0][0]

def select_2(elites, non_elites): #pokazao se loš
    offspring_list = []
    for _ in range(konst.num_of_offsprings): #number of offsprings in each generation
        elite_parent = random.choice(elites) #selecting a random elite parent
        non_elite_parent = random.choice(non_elites) #selecting a random non-elite parent
        offspring = sbx_crossover(elite_parent, non_elite_parent)
        offspring_list.append(offspring)
    return offspring_list

def generate_chromosome():
    chromosome = []
    for _ in range(2*inp.number_of_boxes + inp.number_of_bins): #length of a chromosome is 2*n where n is the number of items to be packed
        chromosome.append(np.random.uniform(low=0.0, high=1.0))
    return chromosome

def mutation():
    mutants = []
    for _ in range(konst.num_mutants):
        chromosome = generate_chromosome()
        mutants.append(chromosome)
    return mutants


def mutation_2(chromosome): #less aggressive mutation
    for i in range(2*inp.number_of_boxes + inp.number_of_bins): #length of a chromosome
        if np.random.uniform(0.0, 1.0) < konst.prob_mutation:
            chromosome[i] = np.random.uniform(low=0.0, high=1.0)
    return chromosome

def calculate_fitness(chromosome):
    bins = copy.deepcopy(inp.bins)
    boxes = copy.deepcopy(inp.boxes)
    placement = obj.placement_procedure(chromosome[:inp.number_of_boxes], chromosome[inp.number_of_boxes:inp.number_of_boxes*2], chromosome[inp.number_of_boxes*2:],bins, boxes)
    fitness = obj.fitness_function(bins, chromosome[inp.number_of_boxes*2:])
    return fitness

def cal_fitness(population): #parallel fitness calculation
    with multiprocessing.Pool() as pool:
        fitness_list = pool.map(calculate_fitness, population)
    return fitness_list

def evolutionary_process():
    generations = []
    mean_fitness_values = []
    best_fitness_values = []
    population = []
    for _ in range(konst.num_individuals):  
        chromosome = generate_chromosome()
        population.append(chromosome)

    fitness_list = cal_fitness(population)

    best_fitness = np.min(fitness_list)
    best_chromosome = population[np.argmin(fitness_list)]
    best_iteration = 0


    for g in range(konst.num_generations):
        fitness_list = cal_fitness(population)
        new_population = []
        top_individuals = np.argsort(fitness_list)[:konst.num_elites]
        new_population.extend([population[i] for i in top_individuals])

        for _ in range((konst.num_individuals-konst.num_elites) // 2):
            parent1 = select(population, fitness_list)
            parent2 = select(population, fitness_list)
            
            child1, child2 = crossover_2(parent1, parent2)
            
            child1 = mutation_2(child1)
            child2 = mutation_2(child2)
            
            new_population.extend([child1, child2])
        
        population = new_population
        best_fitness_population = min(fitness_list)
        generations.append(g)
        mean_fitness_values.append(np.mean(fitness_list))
        best_fitness_values.append(best_fitness_population)
        

        if best_fitness_population < best_fitness:
            best_fitness = best_fitness_population
            best_iteration = g
            best_chromosome = population[np.argmin(fitness_list)]
            print(f'\nGeneration: {g} \t Best Fitness: {best_fitness}\n')

        # print(f'Generation: {g} \t Best Fitness: {best_fitness_population} \t Mean Fitness: {np.mean(fitness_list)}')
    
    #write all the results to a file
    with open('results-best.txt', 'a') as f:
            f.write(f'{best_fitness}\n')
    
    # plt.plot(generations, mean_fitness_values, label='Mean Fitness')
    # plt.plot(generations, best_fitness_values, label='Best Fitness')
    # plt.xlabel('Generations')
    # plt.title('Evolution of Mean and Best Fitness Values')
    # plt.show()

def main():
    evolutionary_process()

if __name__ == "__main__":
    main()