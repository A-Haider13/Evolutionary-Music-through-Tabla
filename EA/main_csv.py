import sys
from EA import EA
import os

def main_test():
    parent_selection = "random"
    survivor_selection = "truncation"
    schemes = ["rank_based_selection","truncation","random","fitness_prop_selection","tournament_selection_2"]
    pop_size = 50
    offspring_size = 10
    generations_no = 500
    mutation_rate = 0.5 
    iterations = 1
    length = 50
    path = "graph_data/single_bols"
    good_pairs = [('DHA','DHIN'),('DHIN','DHA')]
    for PS in schemes:
        ps_name = PS
        if PS == "tournament_selection_2":
            ps_name = "tournament_selection"
        for SS in schemes:
            ss_name = SS
            if SS == "tournament_selection_2":
                ss_name = "tournament_selection"
            print("generating for",ps_name,ss_name)
            if not os.path.exists(f'{path}/{ps_name}_{ss_name}'):
                os.mkdir(f'{path}/{ps_name}_{ss_name}')
                for i in range(3):
                    EA(pop_size, offspring_size, generations_no, mutation_rate, iterations, PS, SS, length, good_pairs, i, path).run()
    # EA(pop_size, offspring_size, generations_no, mutation_rate, iterations, parent_selection, survivor_selection, length, good_pairs).run()

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

main_test()