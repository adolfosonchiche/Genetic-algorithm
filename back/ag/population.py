import random


class Population:
    def __init__(self, population_size):
        self.current_towns = []
        self.current_town = None
        self.population_size = population_size

    def generate_initial_population(self, edges):
        return [[random.randint(int(edge.min_capacity), int(edge.max_capacity)) for edge in edges] for _ in range(int(self.population_size))]
