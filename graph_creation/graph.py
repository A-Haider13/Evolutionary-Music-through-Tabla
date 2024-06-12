import pandas as pd
import matplotlib.pyplot as plt

file_path = ".\\graph_data\\double_bols\\rank_based_selection_truncation\\output_goodpairs.csv"
file_path2 = ".\\graph_data\\double_bols\\rank_based_selection_truncation\\output_tempo.csv"

data = pd.read_csv(file_path)
data2 = pd.read_csv(file_path2)

filtered_data = data[data['Generation'] <= 50]
filtered_data2 = data2[data2['Generation'] <= 50]

plt.figure(figsize=(10, 6))

# For tempo
plt.plot(filtered_data2['Generation'], filtered_data2['Average_Fitness'], label='Average Fitness')
plt.plot(filtered_data2['Generation'], filtered_data2['Best_Fit'], label='Best Fitness of Tempo')
plt.plot(filtered_data2['Generation'], filtered_data2['Worst_Fit'], label='Worst Fitness')

# For Good Pairs
# plt.plot(filtered_data['Generation'], 100-(filtered_data['Average_Fitness']), label='Average Fitness')
# plt.plot(filtered_data['Generation'], 100-(filtered_data['Best_Fit']), label='Best Fitness of Good Pairs')
# plt.plot(filtered_data['Generation'], 100-(filtered_data['Worst_Fit']), label='Worst Fitness')

# Comparison
# plt.plot(filtered_data2['Generation'], filtered_data2['Best_Fit'], label='Best Fitness of Tempo')
# plt.plot(filtered_data['Generation'], (100-(filtered_data['Best_Fit']))*8, label='Best Fitness of Good Pairs multiplied by 8')

plt.xlabel('Generation')
plt.ylabel('Fitness Value')
plt.title('Fitness over generations of Tempo optimization of the Music') # For tempo
# plt.title('Fitness over generations of Good Pairs optimization of the Music') # For good pairs
# plt.title('Comparison of Fitness optimization of two factors') # For comparison


plt.legend()
plt.show()