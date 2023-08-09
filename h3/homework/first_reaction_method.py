# Implementation of First Reaction Method for exercise 3.2.3
# TODO: -
#
#######################################################################################################################
# import libraries
import numpy as np
import random
import matplotlib.pyplot as plt
from tabulate import tabulate


#######################################################################################################################
# plot helper method
def plot_graph_method(list_of_forests, list_of_fires):
    plt.plot(list_of_forests, "g")
    plt.plot(list_of_fires, "r")
    plt.xlabel("Number of Events")
    plt.ylabel("Number of Objects")
    plt.suptitle("grün = Wald, rot = Feuer")
    plt.show()
    data = [
        ["0.1", list_of_forests[int(len(list_of_forests) / 10 * 1)], list_of_fires[int(len(list_of_fires) / 10 * 1)]],
        ["0.2", list_of_forests[int(len(list_of_forests) / 10 * 2)], list_of_fires[int(len(list_of_fires) / 10 * 2)]],
        ["0.3", list_of_forests[int(len(list_of_forests) / 10 * 3)], list_of_fires[int(len(list_of_fires) / 10 * 3)]],
        ["0.4", list_of_forests[int(len(list_of_forests) / 10 * 4)], list_of_fires[int(len(list_of_fires) / 10 * 4)]],
        ["0.5", list_of_forests[int(len(list_of_forests) / 10 * 5)], list_of_fires[int(len(list_of_fires) / 10 * 5)]],
        ["0.6", list_of_forests[int(len(list_of_forests) / 10 * 6)], list_of_fires[int(len(list_of_fires) / 10 * 6)]],
        ["0.7", list_of_forests[int(len(list_of_forests) / 10 * 7)], list_of_fires[int(len(list_of_fires) / 10 * 7)]],
        ["0.8", list_of_forests[int(len(list_of_forests) / 10 * 8)], list_of_fires[int(len(list_of_fires) / 10 * 8)]],
        ["0.9", list_of_forests[int(len(list_of_forests) / 10 * 9)], list_of_fires[int(len(list_of_fires) / 10 * 9)]],
        ["1.0", list_of_forests[int(len(list_of_forests) - 1)], list_of_fires[int(len(list_of_fires) - 1)]]]
    col_names = ["Zeit", "Wald", "Feuer"]
    print(tabulate(data, headers=col_names, tablefmt="fancy_grid"))


#######################################################################################################################
# First Reaction Method Simulation Function

def first_reaction_method_simulation(forest, fire, plot=False):
    list_of_forest_fires = [(forest, fire)]
    # factors for R_i
    a = 20
    b = 0.01
    c = 20

    t = 0
    list_of_forests = []
    list_of_fires = []

    while t <= 1:
        if 0 < forest and 0 < fire:
            a_0 = a * forest
            rand = random.uniform(0, 1)
            a_0_rand = np.log(1 - rand) / (-a_0)

            a_1 = b * forest * fire
            rand = random.uniform(0, 1)
            a_1_rand = np.log(1 - rand) / (-a_1)

            a_2 = c * fire
            rand = random.uniform(0, 1)
            a_2_rand = np.log(1 - rand) / (-a_2)

            if a_0_rand <= a_1_rand and a_0_rand <= a_2_rand:
                forest += 1
                list_of_forest_fires.append((forest, fire))
                t += a_0_rand
            elif a_1_rand <= a_0_rand and a_1_rand <= a_2_rand:
                forest -= 1
                fire += 1
                list_of_forest_fires.append((forest, fire))
                t += a_1_rand
            else:
                fire -= 1
                list_of_forest_fires.append((forest, fire))
                t += a_2_rand

            list_of_forests.append(forest)
            list_of_fires.append(fire)

    if plot:
        plot_graph_method(list_of_forests, list_of_fires)

    return len(list_of_forest_fires)

# first_reaction_method_simulation(1000, 1000, True)
