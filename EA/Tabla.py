import random 
import math
import numpy as np
from problem import Problem

class Tabla(Problem):

    def calculate_fitness(self, chromosome):
        
        # rhythm_entropy = self.calculate_permutation_entropy(chromosome)
        intervals = self.calculate_intervals(chromosome)
        tempo_fitness = self.calculate_tempo(chromosome,intervals)
        bonus = self.check_good_pairs(chromosome)
        # print("bonus:",bonus*100)
        # print(100-bonus)
        return_val = 100-bonus # good pairs
        # return_val = tempo_fitness #tempo
        return return_val
    
    def calculate_rhythm_fitness(self, solution):
        # Calculate rhythm fitness based on the number of unique start times
        start_times = [start_time for _, start_time, _ in solution]
        # print("-----------------------")
        # print(start_times)
        # print(len(start_times))
        # print(set(start_times))
        # print(len(start_times))
        rhythm_fitness = len(set(start_times)) / len(start_times)
        # print(rhythm_fitness)
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
        # pair1 = self.check_good_pair(parent1[0][crossover_point-1][0],parent2[0][crossover_point][0])
        # pair2 = self.check_good_pair(parent2[0][crossover_point][0],parent1[0][crossover_point-1][0])

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
        
        # for i in range(len(mutated_chromosome)):
        #     if random.random() < self.mutation_rate:
        #         # Perform mutation on the sound name
        #         mutated_chromosome[i] = (
        #             random.choice(list(self.tabla_sounds.keys())),  # Random sound name
        #             mutated_chromosome[i][1],  # Keep original start time
        #             self.mutate_volume(mutated_chromosome[i][2])   # Keep original volume
        #         )

        # print(mutated_chromosome)
        # print(self.calculate_fitness(mutated_chromosome))


        # mutation for tempo
        # for i in range(len(mutated_chromosome)):
        #     if random.random() < self.mutation_rate:
        #         # mutation_point = random.randint(0, len(mutated_chromosome) - 1)
        #         new_start_time = mutated_chromosome[i][1] - random.uniform(200, 400)
        #         if new_start_time > 200:
        #             mutated_chromosome[i] = (
        #                 mutated_chromosome[i][0],  # Keep original sound name
        #                 new_start_time,  # Random start time within 100ms of original time
        #                 self.mutate_volume(mutated_chromosome[i][2])   # Keep original volume
        #             )      

        # Recalculate fitness of mutated chromosome

        # mutation for good pairs
        for i in range(1,len(mutated_chromosome)-1):
            prefix_pair = self.check_good_pair(mutated_chromosome[i-1][0],mutated_chromosome[i][0])
            suffix_pair = self.check_good_pair(mutated_chromosome[i][0],mutated_chromosome[i+1][0])
            if ((not prefix_pair) and (not suffix_pair)):
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
            sound_name = random.choice(list(self.tabla_sounds.keys()))  # random start within 10 seconds
            volume_db = random.uniform(-10, 10)  # random volume adjustment
            solution.append((sound_name, interval, volume_db))
            interval = random.uniform(500, 1500)  # random interval between 100ms and 500ms
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

    def calculate_permutation_entropy(self,chromosome,intervals):
        # Calculate permutation entropy of a chromosome
        # print("--------------")
        
        permutation_count = dict()
        permutation_count['same'] = 1
        permutation_count['longer'] = 1
        permutation_count['shorter'] = 1
        
        for i in range(1,len(intervals)):
            a = intervals[i]-intervals[i-1]
            # print(a)
            if abs(a) < 200:
                permutation_count['same'] += 1
            elif a < 0:
                permutation_count['longer'] += 1
            else:
                permutation_count['shorter'] += 1

        # print(permutation_count)
        probabilities = {perm: count / (len(chromosome)-1) for perm, count in permutation_count.items()}
        # print(probabilities)

        entropy = 0
        for prob in probabilities.values():
            entropy -= prob * math.log(prob)

        return entropy

    def calculate_tempo(self,chromosome,intervals):
        # Calculate the tempo of a chromosome
        # print(intervals)
        # print(intervals)
        total_time = sum(intervals)
        # print(total_time)
        # print(total_time)
        avg_interval = total_time / (len(chromosome)-1)

        return avg_interval
    
    def check_good_pair(self,sound1,sound2):
        good_pairs = [('dha','dhin'),('dhin','dha'),('tun','na'),('na','tun')]
        if (sound1,sound2) in good_pairs:
            return True
        return False

    def check_good_pairs(self,chromosome):
        count = 0
        for i in range(1,len(chromosome)):
            if self.check_good_pair(chromosome[i-1][0],chromosome[i][0]):
                count += 1
        return count
