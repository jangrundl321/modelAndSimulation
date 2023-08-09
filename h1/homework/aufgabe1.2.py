#actual implementation of exercise 1.2

import CellularAutomaton
import numpy as np

fire = 2
forest = 1
grass = 0
states = {fire:"fire",
         forest:"forest",
         grass:"grass"}
initial_grid = np.array([[fire, grass, grass], 
                        [grass, grass, forest],
                        [grass, forest, grass]])
fire_grid = np.full((initial_grid.shape), fire)

simple_CA = CellularAutomaton.CellularAutomaton(initial_grid, states, fire_grid)
simple_CA.run()
