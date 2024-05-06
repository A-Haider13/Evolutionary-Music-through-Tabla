import sys
from EA import EA

def main_test():
    problem = "Tabla"
    filename = "qa194.tsp"
    parent_selection = "truncation"
    survivor_selection = "random"
    pop_size = 10
    offspring_size = 2
    generations_no = 1
    mutation_rate = 0.5
    iterations = 1
    length = 10
    EA(pop_size, offspring_size, generations_no, mutation_rate, iterations, problem, parent_selection, survivor_selection, length, filename).run()


def main():
    problem = sys.argv[1]
    filename = sys.argv[2]
    parent_selection = selection_scheme(sys.argv[3])
    survivor_selection = selection_scheme(sys.argv[4])
    pop_size = int(sys.argv[5])
    offspring_size = int(sys.argv[6])
    generations_no = int(sys.argv[7])
    mutation_rate = float(sys.argv[8])
    iterations = int(sys.argv[9])
    length = 10
    EA(pop_size, offspring_size, generations_no, mutation_rate, iterations, problem, parent_selection, survivor_selection, length, filename).run()

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