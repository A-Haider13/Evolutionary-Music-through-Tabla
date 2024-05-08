import sys
from EA import EA
import os

def main_test():
    parent_selection = "rank_based_selection"
    schemes = ["rank_based_selection", "truncation", "random","fitness_prop_selection"]
    survivor_selection = "tournament_selection_2"
    pop_size = 30
    offspring_size = 10
    generations_no = 200
    mutation_rate = 0.5 
    iterations = 1
    length = 50
    for PS in schemes:
        ps_name = PS
        if PS == "tournament_selection_2":
            ps_name = "tournament_selection"
        ss_name = survivor_selection
        if survivor_selection == "tournament_selection_2":
            ss_name = "tournament_selection"
        print("generating for", ps_name, ss_name)
        if not os.path.exists(f'graph_data/{ps_name}_{ss_name}'):
            os.mkdir(f'graph_data/{ps_name}_{ss_name}')
            for i in range(3):
                # Create a folder named 'bruh'
                EA(pop_size, offspring_size, generations_no, mutation_rate, iterations, PS, survivor_selection, length, i).run()


def main():
    parent_selection = selection_scheme(sys.argv[3])
    survivor_selection = selection_scheme(sys.argv[4])
    pop_size = int(sys.argv[5])
    offspring_size = int(sys.argv[6])
    generations_no = int(sys.argv[7])
    mutation_rate = float(sys.argv[8])
    iterations = int(sys.argv[9])
    length = 20
    EA(pop_size, offspring_size, generations_no, mutation_rate, iterations, parent_selection, survivor_selection, length).run()

def selection_scheme(scheme):
    if scheme=="fps":
        return "fitness_prop_selection"
    elif scheme=="rbs":
        return "rank_based_selection"
    elif scheme=="tr":
        return "truncation"
    elif scheme=="rn":
        return "random"
    elif "ts" in scheme:
        size = scheme.split("_")[-1]
        return "tournament_selection_" + size

# main()

if sys.argv[1] == "test":
    main_test()
else:
    main()