import random 
import math
import numpy as np
from problem import Problem

class TSP(Problem):

    def calculate_fitness(self,chromosome):
        total_distance = 0.0
        num_cities = len(chromosome)

        for i in range(num_cities - 1):
            # Calculate Euclidean distance between consecutive cities
            city1 = self.data[chromosome[i] - 1]
            city2 = self.data[chromosome[i + 1] - 1]
            distance = math.sqrt((city2[0] - city1[0])**2 + (city2[1] - city1[1])**2)
            total_distance += distance

        # Add distance from the last city back to the starting city
        total_distance += math.sqrt((self.data[-1][0] - self.data[0][0])**2 + 
                                    (self.data[-1][1] - self.data[0][1])**2)

        return total_distance
    
    def crossover(self,parent1, parent2):
        # Perform crossover to create a new chromosome from two parents
        crossover_point = np.random.randint(1, len(parent1[0])//2)
        crossover_point_2 = np.random.randint(len(parent1[0])//2, len(parent1[0])-1)

        # Create a new chromosome by combining parts of both parents
        first_half = parent1[0][:crossover_point]
        second_half = parent2[0][crossover_point:crossover_point_2]
        third_half = parent1[0][crossover_point_2:]

        new_chromosome1 = first_half + [x for x in second_half if x not in first_half]
        new_chromosome1 = new_chromosome1 + [x for x in third_half if x not in new_chromosome1]
        self.insert_missing(parent1,new_chromosome1)

        first_half = parent2[0][:crossover_point]
        second_half = parent1[0][crossover_point:crossover_point_2]
        third_half = parent2[0][crossover_point_2:]

        new_chromosome2 = first_half + [x for x in second_half if x not in first_half]
        new_chromosome2 = new_chromosome2 + [x for x in third_half if x not in new_chromosome2]
        self.insert_missing(parent2,new_chromosome2)

        fitness1 = self.calculate_fitness(new_chromosome1)
        fitness2 = self.calculate_fitness(new_chromosome2)
        offsprings = [(new_chromosome1,fitness1),(new_chromosome2,fitness2)]
        return offsprings

    def mutate(self, chromosome):
        # Perform mutation by swapping two cities in the chromosome based on mutation rate
        new_chromosome = chromosome[0].copy() 
        fitness = chromosome[1]

        r = np.random.random() < self.mutation_rate
        if r < self.mutation_rate:
            mutation_point = np.random.randint(0, len(new_chromosome),2)
            new_chromosome[mutation_point[0]], new_chromosome[mutation_point[1]] = new_chromosome[mutation_point[1]], new_chromosome[mutation_point[0]]
            # new_chromosome = new_chromosome[mutation_point:] + [x for x in new_chromosome[:mutation_point] if x not in new_chromosome[mutation_point:]]
            # self.insert_missing(chromosome,new_chromosome)

            fitness = self.calculate_fitness(new_chromosome)

        new_chromosome = (new_chromosome,fitness)
        return new_chromosome

    def random_chromosome(self):
        #generate random chromosome from TSP set
        solution = list(range(1,len(self.data)+1))
        random.shuffle(solution)
        fitness = self.calculate_fitness(solution)
        chromosome = (solution,fitness)
        return chromosome
    
    def insert_missing(self,chromosome,new_chromosome):
        missing = []
        for i in range(1,len(chromosome[0])+1):
            if i not in new_chromosome:
                # index = random.randint(0,len(new_chromosome)-1)
                # new_chromosome.insert(index,i)
                new_chromosome.append(i)
                missing.append(i)
        np.random.shuffle(missing)
        # new_chromosome.extend(missing) 
    
    def read_file(self):
        data = ReadFile(self.filename).read()
        return data


#Class for reading file
class ReadFile:
    def __init__(self,filename):
        self.filename = filename
        self.data = []

    # open file
    def read(self):
        try:
            with open(self.filename) as f:
                content = f.readlines()
                print("Reading file {}...".format(self.filename))
                self.parse_data(content)
                print("File read successfully")
                return self.data
        except:
            print("Error: File {} not found".format(self.filename))

    # reads and parses city data
    def parse_data(self,content):
        nodes_start = False

        for line in content:
            if line.startswith("NODE_COORD_SECTION"):
                nodes_start = True
                continue
            
            if nodes_start:
                if line.startswith("EOF"):
                    break
                self.data.append(self.parse_city_data(line))

        return self.data

    #formats city data
    def parse_city_data(self,city_data):
        city = city_data.split()
        city = (float(city[1]),float(city[2]))
        return city