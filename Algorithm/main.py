import numpy as np
from pydub import AudioSegment
import random
import os

# Define the path to the Data folder containing tabla wav files
data_folder = 'Algorithm'

# Load the tabla sound clips from the Data folder
tabla_sounds = {
    'dha': AudioSegment.from_file(os.path.join(data_folder, 'dha.wav'), format='wav'),
    'dhin': AudioSegment.from_file(os.path.join(data_folder, 'dhin.wav'), format='wav'),
    'na': AudioSegment.from_file(os.path.join(data_folder, 'na.wav'), format='wav'),
    'ta': AudioSegment.from_file(os.path.join(data_folder, 'ta.wav'), format='wav')
}

# Define the chromosome representation
# For this example, a chromosome is a list of tuples, each containing
# (sound_name, start_time, volume_db), where:
# - sound_name: key for the tabla sound clip to play
# - start_time: relative start time in milliseconds
# - volume_db: volume adjustment in decibels

# Helper function to create a random chromosome
def create_random_chromosome(length, sound_keys):
    chromosome = []
    for i in range(length):
        sound_name = random.choice(sound_keys)
        start_time = i * (15000 / length)  # evenly spaced within 15 seconds
        volume_db = random.uniform(-10, 10)  # random volume adjustment
        chromosome.append((sound_name, start_time, volume_db))
    return chromosome

# Helper function to generate an audio segment from a chromosome
def generate_audio_from_chromosome(chromosome):
    audio = AudioSegment.silent(duration=15000)  # 15 seconds of silence
    for sound_name, start_time, volume_db in chromosome:
        sound_clip = tabla_sounds[sound_name]
        # Apply volume adjustment
        sound_clip = sound_clip + volume_db
        # Overlay sound at the specified start time
        audio = audio.overlay(sound_clip, position=int(start_time))
    return audio

# Define the fitness function
# A simple fitness function could be to reward even distribution and avoid overlapping sounds.
# This is a simple example; you can adjust it according to your preference.
def fitness_function(chromosome):
    # Check for overlap and penalize it
    start_times = [start_time for _, start_time, _ in chromosome]
    if len(set(start_times)) < len(start_times):
        return -10  # heavily penalize overlapping sounds
    # Reward spread across the duration (simple approach)
    distances = np.diff(sorted(start_times))
    uniformity_score = np.std(distances)  # lower standard deviation is better
    return -uniformity_score

# Genetic operators: Crossover and Mutation
def crossover(parent1, parent2):
    # Simple one-point crossover
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(chromosome, mutation_rate=0.1):
    for i in range(len(chromosome)):
        if random.uniform(0, 1) < mutation_rate:
            # Randomly change the sound clip or start time or volume
            chromosome[i] = (
                random.choice(list(tabla_sounds.keys())),
                chromosome[i][1],  # retain original start time
                chromosome[i][2] + random.uniform(-2, 2)  # small volume adjustment
            )
    return chromosome

# Evolutionary algorithm parameters
population_size = 10
num_generations = 20
mutation_rate = 0.1

# Initialize the population with random chromosomes
population = [create_random_chromosome(10, list(tabla_sounds.keys())) for _ in range(population_size)]

# Run the evolutionary algorithm
for generation in range(num_generations):
    # Evaluate fitness for the entire population
    fitness_scores = [fitness_function(chromosome) for chromosome in population]

    # Select the best chromosomes to become parents
    sorted_population = [x for _, x in sorted(zip(fitness_scores, population), reverse=True)]

    # Keep the best two for the next generation
    new_population = sorted_population[:2]

    # Create new chromosomes through crossover
    while len(new_population) < population_size:
        parent1, parent2 = random.choice(sorted_population), random.choice(sorted_population)
        child1, child2 = crossover(parent1, parent2)
        new_population.append(mutate(child1, mutation_rate))
        if len(new_population) < population_size:
            new_population.append(mutate(child2, mutation_rate))

    population = new_population

# After running the evolutionary algorithm, select the best chromosome
best_chromosome = max(population, key=fitness_function)

# Generate the audio from the best chromosome
best_audio = generate_audio_from_chromosome(best_chromosome)

# Save the generated audio to a file
output_path = 'generated_tabla.wav'
best_audio.export(output_path, format='wav')

print(f"Generated tabla rendition saved to {output_path}")
