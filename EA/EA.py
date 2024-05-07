from Tabla import Tabla
import pandas as pd
import matplotlib.pyplot as plt
from pydub import AudioSegment
import os

class EA: 
    def __init__(self, population_size, offspring_size, generations, mutation_rate, iterations, parent_selection_scheme, survivor_selection_scheme, length):
        self.parent_selection_scheme = parent_selection_scheme
        self.survivor_selection_scheme = survivor_selection_scheme
        self.data_folder = 'Algorithm'
        self.tabla_sounds = {
            'dha': AudioSegment.from_file(os.path.join(self.data_folder, 'dha.wav'), format='wav'),
            'dhin': AudioSegment.from_file(os.path.join(self.data_folder, 'dhin.wav'), format='wav'),
            'na': AudioSegment.from_file(os.path.join(self.data_folder, 'na.wav'), format='wav'),
            'ta': AudioSegment.from_file(os.path.join(self.data_folder, 'ta.wav'), format='wav'),
            'tinak': AudioSegment.from_file(os.path.join(self.data_folder, 'tinak.wav'), format='wav'),
            'ke': AudioSegment.from_file(os.path.join(self.data_folder, 'ke.wav'), format='wav'),
            're': AudioSegment.from_file(os.path.join(self.data_folder, 're.wav'), format='wav'),
            'tun': AudioSegment.from_file(os.path.join(self.data_folder, 'tun.wav'), format='wav'),
        }
        self.length = length
        self.instance = Tabla(population_size, offspring_size, generations, mutation_rate, iterations, length, self.data_folder, self.tabla_sounds)
        self.iterations = iterations  # Store the number of iterations

    def run(self):
        top_solutions = []
        worst_solutions = []
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

        for i in range(self.instance.iterations):
            top_solution_iteration = (None,float('inf'))  # Initialize top solution for current iteration
            worst_solution_iteration = (None,0)  # Initialize worst solution for current iteration
            generation_scores_iteration = []  # Initialize list for storing generation-wise scores for current iteration
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
                self.instance.population = survivors
                top_solution_generation = min(self.instance.population, key=lambda x: x[1])
                worst_solution_generation = max(self.instance.population, key=lambda x: x[1])

                print("Generation: ", j + 1)
                if j==0:
                    self.generate_audio_from_chromosome(top_solution_generation[0]).export('good_initial.wav', format='wav')
                print("Top solution for this generation: ", top_solution_generation[1])
                print("Worst solution for this generation: ", worst_solution_generation[1])  # Print the fitness value
                if top_solution_iteration[1] >= top_solution_generation[1]:
                    top_solution_iteration = top_solution_generation

                if worst_solution_iteration[1] <= worst_solution_generation[1]:
                    worst_solution_iteration = worst_solution_generation


            generation_scores.append(generation_scores_iteration)  # Append the list of scores for the current iteration
            top_solutions.append(top_solution_iteration)  # Append the fitness value only
            worst_solutions.append(worst_solution_iteration)
            self.instance.init_population()  # Reinitialize the population for the next iteration

        toppest_solution = min(top_solutions, key=lambda x: x[1])
        worst_solution = max(worst_solutions, key=lambda x: x[1])
        self.generate_audio_from_chromosome(toppest_solution[0]).export('bad.wav', format='wav')
        self.generate_audio_from_chromosome(worst_solution[0]).export('good.wav', format='wav')

        # print(top_solutions)
        # self.save_to_csv(top_solutions, generation_scores)
        # self.plot_graph(top_solutions)

    def save_to_csv(self, top_solutions, generation_scores):
        # Create a DataFrame from the top solutions
        df = pd.DataFrame(top_solutions, columns=['Iteration', 'Best Fitness'])

        # Prepare a new DataFrame in the desired format
        generations = []
        for gen in range(1, self.instance.generations + 1):
            gen_data = [f'Gen {gen}']  # Start with generation label
            for iteration in range(1, self.iterations + 1):
                # Extract the fitness score for the current iteration and generation
                score = generation_scores[iteration - 1][gen - 1]
                gen_data.append(score)
            # Append the list for the current generation to the list of all generations
            generations.append(gen_data)

        # Convert the list of lists into a DataFrame
        new_df = pd.DataFrame(generations, columns=['Generations'] + [f'Iteration {i}' for i in range(1, self.iterations + 1)])

        # Add the Best Fitness Score column
        new_df['Best Fitness Score'] = [min(row[1:]) for _, row in new_df.iterrows()]

        # Save the DataFrame to a CSV file
        new_df.to_csv('top_solutions_transformed.csv', index=False)

    def plot_graph(self, top_solutions):
        # Plot the bar graph
        x = list(range(1, self.iterations + 1))  # x-axis values
        y = [solution[1] for solution in top_solutions]  # y-axis values
        plt.bar(x, y, color='skyblue')

        # Add labels on top of bars
        for i, v in enumerate(y):
            plt.text(x[i], v, str(v), ha='center', va='bottom')

        plt.xlabel('Iterations')
        plt.ylabel('Fitness Value', labelpad=0.001)  # Adjust labelpad here
        plt.title('Best Fitness Value over Iterations')

        # Add grid for better visualization
        plt.grid(True)

        # Show plot
        plt.show()

    def generate_audio_from_chromosome(self,chromosome):
        audio = AudioSegment.silent(duration=(self.length//4)*1000)  # 15 seconds of silence
        for sound_name, start_time, volume_db in chromosome:
            sound_clip = self.tabla_sounds[sound_name]
            # Apply volume adjustment
            sound_clip = sound_clip + volume_db
            # Overlay sound at the specified start time
            audio = audio.overlay(sound_clip, position=int(start_time))
        return audio