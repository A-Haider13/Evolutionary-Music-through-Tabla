import pandas as pd
import matplotlib.pyplot as plt

file_path = ".\\graph_data\\Tournament_selection_truncation\\output_goodpairs.csv"
file_path2 = ".\\graph_data\\random_fitness_prop_selection\\output_tempo.csv"

data = pd.read_csv(file_path)
data2 = pd.read_csv(file_path2)

filtered_data = data[data['Generation'] <= 50]
filtered_data2 = data2[data2['Generation'] <= 50]

plt.figure(figsize=(10, 6))

# plt.plot(filtered_data['Generation'], 100-filtered_data['Average_Fitness'], label='Average Fitness')
plt.plot(filtered_data['Generation'], (100-filtered_data['Best_Fit']) * 8, label='Best Fitness of Good Pairs multiplied by 8')
plt.plot(filtered_data2['Generation'], filtered_data2['Best_Fit'], label='Best Fitness of Tempo')
# plt.plot(filtered_data['Generation'], 100-filtered_data['Worst_Fit'], label='Worst Fitness')

plt.xlabel('Generation')
plt.ylabel('Fitness Value')
plt.title('Comparison of Fitness Optimization of Two Factors')

plt.legend()
plt.show()