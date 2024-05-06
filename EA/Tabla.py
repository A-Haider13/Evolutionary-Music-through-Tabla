import random 
import math
import numpy as np
from problem import Problem


class TSP(Problem):

    def calculate_fitness(self,chromosome):
        total_fitness = 100
        return total_fitness
    
    def crossover(self,parent1, parent2):
        # Perform crossover to create a new chromosome from two parents
        new_chromosome1 = parent1[0].copy()
        new_chromosome2 = parent2[0].copy()
        fitness1 = self.calculate_fitness(new_chromosome1)
        fitness2 = self.calculate_fitness(new_chromosome2)
        offsprings = [(new_chromosome1,fitness1),(new_chromosome2,fitness2)]
        return offsprings

    def mutate(self, chromosome):
        # Perform mutation by swapping two cities in the chromosome based on mutation rate
        new_chromosome = chromosome[0].copy() 
        fitness = chromosome[1]
        
        new_chromosome = (new_chromosome,fitness)
        return new_chromosome

    def random_chromosome(self):
        #generate random chromosome from TSP set
        chromosome = []
        start_time = 0
        for i in range(self.length):
            sound_name = random.choice(list(self.tabla_sounds.keys()))  # random start within 10 seconds
            volume_db = random.uniform(-10, 10)  # random volume adjustment
            chromosome.append((sound_name, start_time, volume_db))
            start_time += random.uniform(100, 500)  # random interval between 100ms and 500ms
        return chromosome

    