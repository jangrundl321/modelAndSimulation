# Implementation of Experiments for exercise 3.2.2 and exercise 3.2.3
# TODO: -
#
#######################################################################################################################
# import libraries
from direct_method import direct_method_simulation
from first_reaction_method import first_reaction_method_simulation
import math


#######################################################################################################################
# experiments method
def run_experiments():
    x_dm = 0
    x_frm = 0
    y_dm = 0
    y_frm = 0

    list_of_x_dm_values = []
    list_of_x_frm_values = []

    for i in range(2):
        x_dm = direct_method_simulation(1000, 1000)
        x_frm = first_reaction_method_simulation(1000, 1000)

        list_of_x_dm_values.append(x_dm)
        list_of_x_frm_values.append(x_frm)

        y_dm += x_dm
        y_frm += x_frm

    average_dm = round((y_dm / 100))
    average_frm = round((y_frm / 100))

    for i in range(len(list_of_x_dm_values)):
        x_dm += (list_of_x_dm_values[i] - average_dm) ** 2 * 1 / 100

    for i in range(len(list_of_x_frm_values)):
        x_frm += (list_of_x_frm_values[i] - average_frm) ** 2 * 1 / 100

    standard_deviation_dm = round(abs(math.sqrt(x_dm)))
    standard_deviation_frm = round(abs(math.sqrt(x_frm)))

    print("Durchschnitt der Direct Method: " + str(average_dm))
    print("Durchschnitt der First Reaction Method: " + str(average_frm))

    print("Standardabweichung der Direct Method: " + str(standard_deviation_dm))
    print("Standardabweichung der First Reaction Method: " + str(standard_deviation_frm))


#######################################################################################################################
# run experiments

run_experiments()
