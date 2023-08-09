 #actual implementation of exercise 1.4
import numpy as np
import CellularAutomaton

#setting random seed
np.random.seed(0)

def generate_grid():
    grid = np.zeros((21, 21))

    for i in range(318):
        random_col = np.random.randint(0, 20)
        random_row = np.random.randint(0, 20)

        if grid[random_row, random_col] == 0:
            grid[random_row, random_col] = 1

    k = 0
    while k<5:
        random_col = np.random.randint(0, 20)
        random_row = np.random.randint(0, 20)
        if grid[random_row, random_col] == 0:
            k+=1
            grid[random_row, random_col] = 2
    
    print("Generated Grid: \n")
    print(grid)
    return grid

fire = 2
forest = 1
grass = 0

grid = generate_grid()
fire_grid = np.full((grid.shape), fire)
states = {fire:"fire",
        forest:"forest",
        grass:"grass"}

# also takes a very long time, seems good with smaller num of reps
ended_up_in_fire = 0
number_of_reps = 10000
for i in range(number_of_reps):
    grid = generate_grid()
    simple_CA = CellularAutomaton.CellularAutomaton(grid, states, fire_grid)
    simple_CA.run()
    if simple_CA.ended_up_in_fire:
        ended_up_in_fire += 1

print("Von " + str(number_of_reps) +" Simulationen sind " + str(ended_up_in_fire) + " im Feuerzustand geendet")

        

