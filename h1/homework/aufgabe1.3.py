#actual implementation of exercise 1.3
import numpy as np
import CellularAutomaton

histogram_of_steps = {}

def init(fire_row, fire_col):
    fire = 2
    forest = 1
    grass = 0
    states = {fire:"fire",
            forest:"forest",
            grass:"grass"}

    initial_grid = np.zeros((21, 21))
    for row, col in np.ndindex(initial_grid.shape):
        if col<11:
            initial_grid[row, col] = grass
        else:
            initial_grid[row, col] = forest

    initial_grid[fire_row, fire_col] = fire
    fire_grid = [np.full((initial_grid.shape), fire)]
    simple_CA = CellularAutomaton.CellularAutomaton(initial_grid, states, fire_grid)
    simple_CA.run()
    histogram_of_steps["CA with fire coordinates: " + str((fire_row, fire_col))] = simple_CA.steps

#using range(0, 20) takes ages, smaller ranges like range(0,2) seem to work/are fast
for row in range(0, 20):
    for col in range(0, 20):
        init(row, col)

sum_of_steps = 0
number_of_entries = 0
for x in histogram_of_steps:
    sum_of_steps += histogram_of_steps[x]
    number_of_entries += 1 
mean_steps = sum_of_steps/number_of_entries

print("Histogramm der Schritte: \n")
print(histogram_of_steps)
print("Durchschnittlichee Schrittanzahl: \n")
print(mean_steps)
print("Standardabweichung: \n")
print(mean_steps**0.5)