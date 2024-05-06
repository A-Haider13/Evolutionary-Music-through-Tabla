import random 
import math
import numpy as np
from problem import Problem


class Tabla(Problem):

    def calculate_fitness(self, chromosome):
        solution = chromosome
        
        # Initialize fitness components
        rhythm_fitness = 0
        timing_fitness = 0
        dynamic_fitness = 0
        sound_quality_fitness = 0
        
        # Fitness calculation for each aspect
        rhythm_fitness = self.calculate_rhythm_fitness(solution)
        timing_fitness = self.calculate_timing_fitness(solution)
        dynamic_fitness = self.calculate_dynamic_fitness(solution)
        sound_quality_fitness = self.calculate_sound_quality_fitness(solution)
        
        # Aggregate overall fitness
        overall_fitness = (
            0.25 * rhythm_fitness +
            0.25 * timing_fitness +
            0.25 * dynamic_fitness +
            0.25 * sound_quality_fitness
        )
        
        return overall_fitness
    
    def calculate_rhythm_fitness(self, solution):
        # Calculate rhythm fitness based on the number of unique start times
        start_times = [start_time for _, start_time, _ in solution]
        rhythm_fitness = len(set(start_times)) / len(start_times)
        return rhythm_fitness
    
    def calculate_timing_fitness(self, solution):
        # Calculate timing fitness based on the regularity of start times
        start_times = [start_time for _, start_time, _ in solution]
        distances = np.diff(sorted(start_times))
        timing_fitness = np.std(distances)
        return timing_fitness
    
    def calculate_dynamic_fitness(self, solution):
        # Calculate dynamic fitness based on the volume adjustments
        volume_adjustments = [volume_db for _, _, volume_db in solution]
        dynamic_fitness = np.std(volume_adjustments)
        return dynamic_fitness
    
    def calculate_sound_quality_fitness(self, solution):
        # Calculate sound quality fitness based on the sound clips used
        sound_quality_fitness = 1.0
        return sound_quality_fitness
    
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
        solution = []
        start_time = 0
        for i in range(self.length):
            sound_name = random.choice(list(self.tabla_sounds.keys()))  # random start within 10 seconds
            volume_db = random.uniform(-10, 10)  # random volume adjustment
            solution.append((sound_name, start_time, volume_db))
            start_time += random.uniform(100, 500)  # random interval between 100ms and 500ms
        fitness = self.calculate_fitness(solution)
        chromosome = (solution,fitness)
        return chromosome

    