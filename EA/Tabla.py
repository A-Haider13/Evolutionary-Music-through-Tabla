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
        crossover_point = random.randint(1, self.length - 1)

        child1_solution = parent1[0][:crossover_point] + parent2[0][crossover_point:]
        child2_solution = parent2[0][:crossover_point] + parent1[0][crossover_point:]

        child1_fitness = self.calculate_fitness(child1_solution)
        child2_fitness = self.calculate_fitness(child2_solution)

        child1 = (child1_solution, child1_fitness)
        child2 = (child2_solution, child2_fitness)

        offsprings = [child1, child2]

        return offsprings

    def mutate(self, chromosome):
        mutated_chromosome = list(chromosome[0])  # Create a copy of the chromosome
        
        for i in range(len(mutated_chromosome)):
            if random.random() < self.mutation_rate:
                # Perform mutation on the sound name
                mutated_chromosome[i] = (
                    random.choice(list(self.tabla_sounds.keys())),  # Random sound name
                    mutated_chromosome[i][1],  # Keep original start time
                    self.mutate_volume(mutated_chromosome[i][2])   # Keep original volume
                )
                
        # Recalculate fitness of mutated chromosome
        mutated_fitness = self.calculate_fitness(mutated_chromosome)
        
        return (mutated_chromosome, mutated_fitness)
    
    def mutate_volume(self, volume):
        # Add random noise to volume within the specified range
        noise = np.random.uniform(-self.volume_mutation_range, self.volume_mutation_range)
        mutated_volume = volume + noise
        # Ensure volume remains within the valid range
        mutated_volume = max(-10, min(10, mutated_volume))
        return mutated_volume

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

    