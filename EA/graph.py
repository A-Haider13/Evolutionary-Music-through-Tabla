import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

def create_graph(mode,config="Random_Truncation",path="Data\\CompoundBols"):
    file_path = ".\\output_goodpairs.csv"
    file_path2 = ".\\output_tempo.csv"

    save_path = f'{path}\\{config}'

    data = pd.read_csv(file_path)
    data2 = pd.read_csv(file_path2)

    filtered_data = data[data['Generation'] <= 250]
    filtered_data2 = data2[data2['Generation'] <= 250]
    
    if not os.path.exists(save_path):
        print("Creating directory")
        os.mkdir(save_path)

    plt.figure(figsize=(10, 6))

    # For tempo
    if mode==0 or mode==3:
        plt.xlabel('Generation')
        plt.ylabel('Fitness Value')  
        plt.plot(filtered_data2['Generation'], filtered_data2['Average_Fitness'], label='Average Fitness')
        plt.plot(filtered_data2['Generation'], filtered_data2['Best_Fit'], label='Best Fitness of Tempo')
        plt.plot(filtered_data2['Generation'], filtered_data2['Worst_Fit'], label='Worst Fitness')
        plt.title('Fitness over generations of Tempo optimization of the Music') # For tempo
        plt.legend()
        if mode==3:
            plt.savefig(f'{save_path}\\Tempo.png')
            plt.clf()
    if mode==1 or mode==3:
    # # For Good Pairs
        plt.xlabel('Generation')
        plt.ylabel('Fitness Value')  
        plt.plot(filtered_data['Generation'], 100-(filtered_data['Average_Fitness']), label='Average Fitness')
        plt.plot(filtered_data['Generation'], 100-(filtered_data['Best_Fit']), label='Best Fitness of Good Pairs')
        plt.plot(filtered_data['Generation'], 100-(filtered_data['Worst_Fit']), label='Worst Fitness')
        plt.title('Fitness over generations of Good Pairs optimization of the Music') # For good pairs
        plt.legend()
        if mode==3:
            plt.savefig(f'{save_path}\\GP.png')
            plt.clf()
    if mode==2 or mode==3:
    # Comparison
        plt.xlabel('Generation')
        plt.ylabel('Fitness Value')  
        plt.plot(filtered_data2['Generation'], filtered_data2['Best_Fit'], label='Best Fitness of Tempo')
        plt.plot(filtered_data['Generation'], (100-(filtered_data['Best_Fit']))*8, label='Best Fitness of Good Pairs multiplied by 8')
        plt.title('Comparison of Fitness optimization of two factors') # For comparison
        plt.legend()
        if mode==3:
            plt.savefig(f'{save_path}\\Comparison.png')
            plt.clf()

if __name__ == "__main__":
    mode_txt = sys.argv[1]
    if mode_txt=="tempo":
        mode=0
    elif mode_txt=="gp":
        mode=1
    elif mode_txt=="comparison":
        mode=2
    elif mode_txt=="all":
        mode=3
    main(mode)