import numpy as np


#defining Cellular Automatons broadly as Class
class CellularAutomaton:
    def __init__(self, grid, states, fire_grid):
        self.grid = grid
        self.states = states 
        self.steps = 0
        self.sim_not_stuck = True
        self.ended_up_in_fire = False
        self.fire_grid = fire_grid

    #defining Moore neighborhood as function
    def moore_neighborhood(self, row, col):
        grid = self.grid
        neighborhood = []
        for x, y in (
                (row - 1, col), (row + 1, col), (row, col - 1),
                (row, col + 1), (row - 1, col - 1), (row - 1, col + 1),
                (row + 1, col - 1), (row + 1, col + 1)):
            if not (0 <= x < len(grid) and 0 <= y < len(grid[x])):
                # out of bounds
                continue
            else:
                neighborhood.append((x, y))
        return neighborhood

    #update grid after every step by rules
    def update(self):
        current_grid = self.grid
        new_grid = np.zeros((current_grid.shape[0], current_grid.shape[1]))
        for row, col in np.ndindex(current_grid.shape):
            neighborhood = self.moore_neighborhood(row, col)
            counter_fire_in_neighborhood = 0
            counter_forest_in_neighborhood = 0

            for x in neighborhood:
                if current_grid[x] == 2:
                    counter_fire_in_neighborhood += 1
                elif current_grid[x] == 1:
                    counter_forest_in_neighborhood += 1

            if (current_grid[row, col] == 0 and counter_fire_in_neighborhood >= 1) \
                    or (current_grid[row, col] == 1 and counter_fire_in_neighborhood >= 3)\
                    or (current_grid[row, col] == 2):
                new_grid[row, col] = 2
            elif (current_grid[row, col] == 0 and counter_forest_in_neighborhood >= 2)\
                    or (current_grid[row, col] == 1):
        
                new_grid[row, col] = 1
            else:
                new_grid[row, col] = 0

        if(np.array_equal(current_grid,self.fire_grid)):
            self.ended_up_in_fire = True
            self.sim_not_stuck = False
        if(np.array_equal(current_grid,new_grid)):
            self.sim_not_stuck = False
            
        self.grid = new_grid

    #printing grid in a more readable form
    def print_grid(self, step):
        current_grid = self.grid
        states = self.states
        print_grid = np.empty((current_grid.shape[0], current_grid.shape[1]), dtype=object)

        for row, col in np.ndindex(current_grid.shape):
            print_grid[row, col] = states[current_grid[row, col]]
        print("Simulation`s Schritt: " + str(step))
        print(print_grid)

        
    #running the model
    def run(self):
        i = 1
        while self.sim_not_stuck:
            self.steps += 1
            self.print_grid(i)
            i += 1
            self.update()
