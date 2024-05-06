import random
import numpy as np
from pydub import AudioSegment
import os

class Problem():
    def __init__(self,population_size,offspring_size,generations,mutation_rate,iterations,length,filename):
        self.population_size = population_size
        self.offspring_size = offspring_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.iterations = iterations
        self.tournament_size = 2
        self.length = length
        self.filename = filename
        self.data_folder = 'Algorithm'
        self.tabla_sounds = {
            'dha': AudioSegment.from_file(os.path.join(self.data_folder, 'dha.wav'), format='wav'),
            'dhin': AudioSegment.from_file(os.path.join(self.data_folder, 'dhin.wav'), format='wav'),
            'na': AudioSegment.from_file(os.path.join(self.data_folder, 'na.wav'), format='wav'),
            'ta': AudioSegment.from_file(os.path.join(self.data_folder, 'ta.wav'), format='wav'),
            'tinak': AudioSegment.from_file(os.path.join(self.data_folder, 'tinak.wav'), format='wav')
        }
        self.data = self.read_file()
        self.init_population()
    
    def init_population(self):
        self.population = []  # Add this line to initialize the population attribute
        # Initialize the population with random individuals
        for _ in range(self.population_size):
            self.population.append(self.random_chromosome()) 
        # print(self.population[0])
        # print(self.population[1])
        for i in self.population:
            print(i[1])


    
    def fitness_prop_selection(self, p=False, s=False):
        if not p and not s:
            print("Specify whether to use the function for parent or survivor selection")
            return 
        # Select two parents using fitness proportionate selection
        fitness_values = [x[1] for x in self.population]
        total_fitness = sum(fitness_values)
        probabilities = [x / total_fitness for x in fitness_values]
        if p:
            choice = np.random.choice(range(len(self.population)), 2, p=probabilities, replace=False)
            parents = [self.population[choice[0]], self.population[choice[1]]]
            return parents
        if s:
            choice = np.random.choice(range(len(self.population)), self.population_size, p=probabilities, replace=False)
            survivors = [self.population[x] for x in choice]
            return survivors
    
    def rank_based_selection(self, p=False, s=False):
        if not p and not s:
            print("Specify whether to use the function for parent or survivor selection")
            return 
        # Select two parents using rank-based selection
        fitness_sorted = sorted(self.population, key=lambda x: x[1])
        fitness_range = range(1, len(fitness_sorted) + 1)
        probabilities = [x / sum([y for y in fitness_range]) for x in reversed(fitness_range)]
        if p:
            choice = np.random.choice(range(len(self.population)), 2, p=probabilities, replace=False)
            parents = [self.population[choice[0]], self.population[choice[1]]]
            return parents
        if s:
            choice = np.random.choice(range(len(self.population)), self.population_size, p=probabilities, replace=False)
            survivors = [self.population[x] for x in choice]
            return survivors

    def tournament_selection(self, p=False, s=False):
        if not p and not s:
            print("Specify whether to use the function for parent or survivor selection")
            return
        if p:
            parents = [self.tournament(), self.tournament()]
            return parents
        if s:
            survivors = [self.tournament()]
            return survivors
        
    def tournament(self):
        rand_n = []
        for i in range(self.tournament_size):
            rand_n.append(random.randint(1,len(self.population)))
        players = [self.population[i-1] for i in rand_n]
        ranking = sorted(players, key=lambda x: x[1])
        return ranking[0]

    def truncation(self, p=False, s=False):
        if not p and not s:
            print("Specify whether to use the function for parent or survivor selection")
            return 
        if p:
            # Selects two parents using truncation selection
            parents = sorted(self.population, key=lambda x: x[1])[:2]
            return parents
        if s:
            # Selects survivors using truncation selection
            survivors = sorted(self.population, key=lambda x: x[1])[:self.population_size]
            return survivors

    def random(self,p=False,s=False):
        if not p and not s:
            print("Specify whether to use function for parent or survivor selection")
            return 
        
        if p:
            choice = [random.randint(1,self.population_size)-1 for i in range(2)]
            parents = [self.population[choice[0]],self.population[choice[1]]]
            return parents
        if s:
            choice = [random.randint(1,self.population_size)-1 for i in range(self.population_size)]
            survivors = [self.population[choice[i]] for i in choice]
            return survivors
        
    def calculate_fitness(self, chromosome):
        pass 

    def random_chromosome(self):
        pass

    def read_file(self):
        pass
