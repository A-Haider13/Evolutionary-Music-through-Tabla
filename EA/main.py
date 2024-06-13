import sys
from EA import EA
from graph import create_graph



def main_test():
    parent_selection = "random"
    survivor_selection = "truncation"
    pop_size = 100
    offspring_size = 20
    generations_no = 250
    mutation_rate = 0.5 
    iterations = 1
    length = 50
    good_pairs = [('DHA','DHIN'),('DHIN','DHA')]
    path = ""
    for i in range(3):
        EA(pop_size, offspring_size, generations_no, mutation_rate, iterations, parent_selection, survivor_selection, length, good_pairs,i,path).run()
    create_graph(3,config=f'pop{pop_size}_off{offspring_size}')

def main():
    parent_selection = selection_scheme(sys.argv[3])
    survivor_selection = selection_scheme(sys.argv[4])
    pop_size = int(sys.argv[5])
    offspring_size = int(sys.argv[6])
    generations_no = int(sys.argv[7])
    mutation_rate = float(sys.argv[8])
    iterations = int(sys.argv[9])
    length = 20
    good_pairs = [('DHA','DHIN'),('DHIN','DHA')]
    EA(pop_size, offspring_size, generations_no, mutation_rate, iterations, parent_selection, survivor_selection, length, good_pairs).run()

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