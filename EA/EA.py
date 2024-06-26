from Tabla import Tabla
from pydub import AudioSegment
import os
import csv

class EA: 
    def __init__(self, population_size, offspring_size, generations, mutation_rate, iterations, parent_selection_scheme, survivor_selection_scheme, length, good_pairs, mode=None, path=None):
        self.parent_selection_scheme = parent_selection_scheme
        self.survivor_selection_scheme = survivor_selection_scheme
        self.mode = mode
        self.path = path
        self.data_folder = 'Bols'
        self.tabla_sounds = {
            'DHA': AudioSegment.from_file(os.path.join(self.data_folder, 'DoubleHandedBols/DHA.wav'), format='wav'),
            'DHIN': AudioSegment.from_file(os.path.join(self.data_folder, 'DoubleHandedBols/DHIN.wav'), format='wav'),
            'GE': AudioSegment.from_file(os.path.join(self.data_folder, 'SingleHandedBols/GE.wav'), format='wav'),
            'GHE': AudioSegment.from_file(os.path.join(self.data_folder, 'SingleHandedBols/GHE.wav'), format='wav'),
            'KA': AudioSegment.from_file(os.path.join(self.data_folder, 'SingleHandedBols/KA.wav'), format='wav'),
            'KAT': AudioSegment.from_file(os.path.join(self.data_folder, 'SingleHandedBols/KAT.wav'), format='wav'),
            'TA': AudioSegment.from_file(os.path.join(self.data_folder, 'SingleHandedBols/TA.wav'), format='wav'),
            'TIN': AudioSegment.from_file(os.path.join(self.data_folder, 'SingleHandedBols/TIN.wav'), format='wav'),
            'TIT': AudioSegment.from_file(os.path.join(self.data_folder, 'SingleHandedBols/TIT.wav'), format='wav'),
            'TU': AudioSegment.from_file(os.path.join(self.data_folder, 'SingleHandedBols/TU.wav'), format='wav'), 
            # Additional 8 Bols
            'DHINGIN-DHENGEN': AudioSegment.from_file(os.path.join(self.data_folder, 'CompoundBols/DHINGIN-DHENGEN.wav'), format='wav'),
            'DHIT': AudioSegment.from_file(os.path.join(self.data_folder, 'CompoundBols/DHIT.wav'), format='wav'),
            'DHITT': AudioSegment.from_file(os.path.join(self.data_folder, 'CompoundBols/DHITT.wav'), format='wav'),
            'DIN-DIN-DUN': AudioSegment.from_file(os.path.join(self.data_folder, 'CompoundBols/DIN-DIN-DUN.wav'), format='wav'),
            'GADIGEN': AudioSegment.from_file(os.path.join(self.data_folder, 'CompoundBols/GADIGEN.wav'), format='wav'),
            'GHDASN': AudioSegment.from_file(os.path.join(self.data_folder, 'CompoundBols/GHDASN.wav'), format='wav'),
            'KATIT': AudioSegment.from_file(os.path.join(self.data_folder, 'CompoundBols/KATIT.wav'), format='wav'),
            'TIN-TENE': AudioSegment.from_file(os.path.join(self.data_folder, 'CompoundBols/TIN-TENE.wav'), format='wav'),
            'TITT': AudioSegment.from_file(os.path.join(self.data_folder, 'CompoundBols/TITT.wav'), format='wav'),
        }
        self.length = length
        self.instance = Tabla(population_size, offspring_size, generations, mutation_rate, iterations, length, self.data_folder, self.tabla_sounds, good_pairs, mode)
        self.iterations = iterations  # Store the number of iterations

    def run(self):
        high_solutions = []
        low_solutions = []
        generation_scores = []  # Initialize list to store generation-wise scores

        if "tournament_selection" in self.parent_selection_scheme:
            psf = self.parent_selection_scheme[:20]
            tn_size = self.parent_selection_scheme.split("_")[-1]
            self.instance.tournament_size = int(tn_size)
            self.parent_selection_scheme = psf

        if "tournament_selection" in self.survivor_selection_scheme:
            ssf = self.survivor_selection_scheme[:20]
            tn_size = self.survivor_selection_scheme.split("_")[-1]
            self.instance.tournament_size = int(tn_size)
            self.survivor_selection_scheme = ssf

        parent_selection_function = getattr(self.instance, self.parent_selection_scheme)
        survivor_selection_function = getattr(self.instance, self.survivor_selection_scheme)
        if not callable(parent_selection_function) or not callable(survivor_selection_function):
            print("Invalid selection scheme")
            return
    
        if self.mode==0:
            if self.path:
                self.write_headers(f'{self.path}/{self.parent_selection_scheme}_{self.survivor_selection_scheme}/output_goodpairs.csv',['Generation', 'Average_Fitness', 'Worst_Fit', 'Best_Fit'])
            else:
                self.write_headers('output_goodpairs.csv',['Generation', 'Average_Fitness', 'Worst_Fit', 'Best_Fit'])
        elif self.mode==1:
            if self.path:
                self.write_headers(f'{self.path}/{self.parent_selection_scheme}_{self.survivor_selection_scheme}/output_tempo.csv',['Generation', 'Average_Fitness', 'Worst_Fit', 'Best_Fit'])
            else:
                self.write_headers('output_tempo.csv',['Generation', 'Average_Fitness', 'Worst_Fit', 'Best_Fit'])
        elif self.mode==2:
            if self.path:
                self.write_headers(f'{self.path}/{self.parent_selection_scheme}_{self.survivor_selection_scheme}/output_combined.csv',['Generation', 'Average_Fitness', 'Worst_Fit', 'Best_Fit'])
            else:
                self.write_headers('output_combined.csv',['Generation', 'Average_Fitness', 'Worst_Fit', 'Best_Fit'])


        for i in range(self.instance.iterations):

            high_solution_iteration = (None,0)  # Initialize top solution for current iteration
            low_solution_iteration = (None,float('inf'))  # Initialize worst solution for current iteration

            generation_scores_iteration = []  # Initialize list for storing generation-wise scores for current iteration

            # self.write_headers('output_goodpairs.csv',['Generation', 'Average_Fitness', 'Best_Fit', 'Worst_Fit'])

            for j in range(self.instance.generations):
                generation_score = min(self.instance.population, key=lambda x: x[1])[1]  # Get the best fitness for the current generation
                generation_scores_iteration.append(generation_score)  # Append the score to the list
                for k in range(0, self.instance.offspring_size, 2):
                    parents = parent_selection_function(p=True)
                    offsprings = self.instance.crossover(parents[0], parents[1])
                    self.instance.population.append(self.instance.mutate(offsprings[0]))
                    self.instance.population.append(self.instance.mutate(offsprings[1]))
                    self.instance.population.append(offsprings[0])
                    self.instance.population.append(offsprings[1])

                survivors = survivor_selection_function(s=True)
        
                fitness_values = [x[1] for x in survivors]
                avg_fitness = sum(fitness_values) / len(fitness_values)

                self.instance.population = survivors
                high_solution_generation = max(self.instance.population, key=lambda x: x[1])
                low_solution_generation = min(self.instance.population, key=lambda x: x[1])

                if self.mode==0:
                    if self.path:
                        self.write_to_csv(f'{self.path}/{self.parent_selection_scheme}_{self.survivor_selection_scheme}/output_goodpairs.csv', j + 1, avg_fitness, high_solution_generation[1], low_solution_generation[1])
                    else:
                        self.write_to_csv('output_goodpairs.csv', j + 1, avg_fitness, high_solution_generation[1], low_solution_generation[1])
                elif self.mode==1:
                    if self.path:
                        self.write_to_csv(f'{self.path}/{self.parent_selection_scheme}_{self.survivor_selection_scheme}/output_tempo.csv', j + 1, avg_fitness, high_solution_generation[1], low_solution_generation[1])
                    else:
                        self.write_to_csv('output_tempo.csv', j + 1, avg_fitness, high_solution_generation[1], low_solution_generation[1])
                elif self.mode==2:
                    if self.path:
                        self.write_to_csv(f'{self.path}/{self.parent_selection_scheme}_{self.survivor_selection_scheme}/output_combined.csv', j + 1, avg_fitness, high_solution_generation[1], low_solution_generation[1])
                    else:
                        self.write_to_csv('output_combined.csv', j + 1, avg_fitness, high_solution_generation[1], low_solution_generation[1])

                # self.write_to_csv('output_goodpairs.csv', j + 1, avg_fitness, 100-high_solution_generation[1], 100-low_solution_generation[1])

                print("Generation: ", j + 1)

                if j==0:
                    self.generate_audio_from_chromosome(high_solution_generation[0]).export('initial.wav', format='wav')

                print("Top solution for this generation: ", low_solution_generation[1])
                print("Worst solution for this generation: ", high_solution_generation[1])  # Print the fitness value

                if high_solution_iteration[1] <= high_solution_generation[1]:
                    high_solution_iteration = high_solution_generation

                if low_solution_iteration[1] >= low_solution_generation[1]:
                    low_solution_iteration = low_solution_generation

            generation_scores.append(generation_scores_iteration)  # Append the list of scores for the current iteration
            high_solutions.append(high_solution_iteration)  # Append the fitness value only
            low_solutions.append(low_solution_iteration)
            self.instance.init_population()  # Reinitialize the population for the next iteration

        highest_solution = max(high_solutions, key=lambda x: x[1])
        lowest_solution = min(low_solutions, key=lambda x: x[1])
        self.generate_audio_from_chromosome(highest_solution[0]).export('bad.wav', format='wav')
        self.generate_audio_from_chromosome(lowest_solution[0]).export('good.wav', format='wav')

    def write_headers(self,filename,arr):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(arr)

    def write_to_csv(self,filename, generation, avg_fitness, top_fitness, low_fitness):
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([generation, avg_fitness, top_fitness, low_fitness])

    def generate_audio_from_chromosome(self,chromosome):
        # intervals = [x[1] for x in chromosome]
        # good_pairs = self.instance.check_good_pairs(chromosome)
        total_time = 0
        for i in range(len(chromosome)):
            total_time += chromosome[i][1]
        bol_time = self.length * 100
        total_time += bol_time
        audio = AudioSegment.silent(duration=15000) 
        start_time = 0
        for sound_name, interval, volume_db in chromosome:
            start_time += interval
            sound_clip = self.tabla_sounds[sound_name]
            # Apply volume adjustment
            sound_clip = sound_clip + volume_db
            # Overlay sound at the specified start time
            audio = audio.overlay(sound_clip, position=int(start_time))
        return audio
    
    def check_good_pairs(self,chromosome):
        count = 0
        for i in range(1,len(chromosome)):
            pair = self.instance.check_good_pair(chromosome[i-1][0],chromosome[i][0])
            if pair:
                count += 1
