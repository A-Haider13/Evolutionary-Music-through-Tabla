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