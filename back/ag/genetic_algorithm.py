import random

from back.ag.individual import Individual
from back.ag.population import Population


class GeneticAlgorithm:
    def __init__(self, model_config, nodes, ):
        self.populations = []
        self.model_config = model_config
        self.mutation_rate = model_config.mutation_rate
        self.generations = int(model_config.generations)
        self.population_size = int(model_config.population_size)
        self.efficiency = model_config.efficiency
        self.num_mutations = int(model_config.num_mutations)
        self.nodes = nodes
        self.population_ob = Population(self.model_config.population_size)

    def run_genetic_algorithm(self):
        print("start genetic algorithm")
        self.populations = []
        for node in self.nodes:
            population = self.population_ob.generate_initial_population(node.connections)
            self.populations.append(Individual(population, node.connections, node))

        print(self.populations[0].population)
        for generation in range(self.generations):
            total_fitness = 0
            for population in self.populations:
                fitness_list = [self.fitness(ind) for ind in population.population]
                new_population = []
                while len(new_population) < self.population_size:
                    print("new pop")
                    print(fitness_list)
                    parent1 = self.select(population.population, fitness_list)
                    parent2 = self.select(population.population, fitness_list)
                    child1, child2 = self.crossover(parent1, parent2)
                    new_population.append(self.mutate(child1, self.mutation_rate, self.num_mutations, population.street))
                    new_population.append(self.mutate(child2, self.mutation_rate, self.num_mutations, population.street))
                population.population = new_population
                best_fitness = max(population.population)
                print(new_population)
                print(f'Generation {generation}, Best Fitness {best_fitness}')
            if self.efficiency and total_fitness >= int(self.efficiency):
                print(self.populations)
                break

        return self.populations

    # Función de aptitud
    def fitness(self, individual):
        print("funcion aptitud")
        print(individual)
        return sum(individual)

    def select(self, population, fitnesses):
        total_fitness = sum(fitnesses)
        pick = random.uniform(0, total_fitness)
        current = 0
        for individual, fitness in zip(population, fitnesses):
            current += fitness
            if current > pick:
                return individual

    # Cruce
    def crossover(self, parent1, parent2):
        point = random.randint(1, len(parent1) - 1)
        return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]

    def mutate(self, individual, mutation_rate, num_mutations, edges):
        for _ in range(num_mutations):
            index = random.randrange(len(individual))
            if random.random() < mutation_rate:
                individual[index] = random.randint(int(edges[index].min_capacity), int(edges[index].max_capacity))
        return individual

