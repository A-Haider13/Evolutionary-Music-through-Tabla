import random 
import math
import numpy as np
from problem import Problem

class Tabla(Problem):

    def calculate_fitness(self, chromosome):
        
        intervals = self.calculate_intervals(chromosome)
        tempo_fitness = self.calculate_tempo(chromosome,intervals)
        normalized_tempo = (tempo_fitness - 200) / (1000 - 200)
        bonus = 100-self.check_good_pairs(chromosome)
        normalized_bonus = (100-bonus) / (100)
        weighted_avg = (0.5*normalized_tempo + 0.5*normalized_bonus)*1000

        # return weighted_avg

        if self.mode == 0:
            return bonus
        elif self.mode == 1:
            return tempo_fitness
        else:
            return weighted_avg
        
        # return weighted_avg*1000
    
    def crossover(self,parent1, parent2):
        # Perform crossover to create a new chromosome from two parents
        crossover_point = random.randint(1, self.length - 1)

        child1_solution = parent1[0][:crossover_point] + parent2[0][crossover_point:]
        child2_solution = parent2[0][:crossover_point] + parent1[0][crossover_point:]

        # print("child fitness calculation")
        child1_fitness = self.calculate_fitness(child1_solution)
        child2_fitness = self.calculate_fitness(child2_solution)

        child1 = (child1_solution, child1_fitness)
        child2 = (child2_solution, child2_fitness)

        offsprings = [child1, child2]

        return offsprings

    def mutate(self, chromosome):
        mutated_chromosome = list(chromosome[0])  # Create a copy of the chromosome

        # mutation for tempo
        for i in range(len(mutated_chromosome)):
            if random.random() < self.mutation_rate:
                # mutation_point = random.randint(0, len(mutated_chromosome) - 1)
                new_start_time = mutated_chromosome[i][1] - random.uniform(-100, 200)
                if new_start_time > 200:
                    mutated_chromosome[i] = (
                        mutated_chromosome[i][0],  # Keep original sound name
                        new_start_time,  # Random start time within 100ms of original time
                        self.mutate_volume(mutated_chromosome[i][2])   
                    )      

        # mutation for good pairs
        for i in range(1,len(mutated_chromosome)-1):
            prefix_pair = self.check_good_pair(mutated_chromosome[i-1][0],mutated_chromosome[i][0])
            suffix_pair = self.check_good_pair(mutated_chromosome[i][0],mutated_chromosome[i+1][0])
            if (not prefix_pair) and (not suffix_pair):
                # print("trying to mutate",mutated_chromosome[i][0])
                if random.random() < self.mutation_rate:
                    sound_name = random.choice(list(self.tabla_sounds.keys()))
                    volume_db = random.uniform(-10, 10)
                    mutated_chromosome[i] = (sound_name, mutated_chromosome[i][1], volume_db)

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
        interval = 0
        total_time = 0
        for i in range(self.length):
            sound_name = random.choice(list(self.tabla_sounds.keys()))  
            volume_db = random.uniform(-10, 10)  # random volume adjustment
            solution.append((sound_name, interval, volume_db))
            interval = random.uniform(500, 1500)  # random interval between 500ms and 1500ms
            total_time += interval
        fitness = self.calculate_fitness(solution)
        chromosome = (solution,fitness)
        return chromosome

    def calculate_intervals(self,chromosome):
        intervals = []
        for i in range(len(chromosome)):
            a = chromosome[i][1]
            intervals.append(a)
        return intervals

    def calculate_tempo(self,chromosome,intervals):
        # Calculate the tempo of a chromosome

        total_time = sum(intervals)
        avg_interval = total_time / (len(chromosome)-1)

        return avg_interval
    
    def check_good_pair(self,sound1,sound2):
        if (sound1,sound2) in self.good_pairs:
            return True
        return False

    def check_good_pairs(self,chromosome):
        count = 0
        for i in range(1,len(chromosome)):
            if self.check_good_pair(chromosome[i-1][0],chromosome[i][0]):
                count += 1
        return count
