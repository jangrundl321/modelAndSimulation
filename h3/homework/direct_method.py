# Implementation of Direct Method Simulation for exercise 3.2.1
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
# Direct Method Simulation Function
def direct_method_simulation(forest, fire, plot=False):
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
            a_1 = b * forest * fire
            a_2 = c * fire
            sum_a = a_0 + a_1 + a_2

            sum_a_rand = random.randint(0, int(sum_a))
            rand = random.uniform(0, 1)

            if rand == 1:
                continue
            if sum_a_rand <= a_0:
                forest += 1
                list_of_forest_fires.append((forest, fire))
            elif a_0 < sum_a_rand <= a_0 + a_1:
                forest -= 1
                fire += 1
                list_of_forest_fires.append((forest, fire))
            else:
                fire -= 1
                list_of_forest_fires.append((forest, fire))

            t += np.log(1 - rand) / (-sum_a)
            list_of_forests.append(forest)
            list_of_fires.append(fire)

    if plot:
        plot_graph_method(list_of_forests, list_of_fires)

    return len(list_of_forest_fires)

# direct_method_simulation(1000, 1000, True)
