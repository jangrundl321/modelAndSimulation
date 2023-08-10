# simple CA: Game of Life; visualised with Pygame
import sys
import pygame
import numpy as np


###########################################################################################################
# CA: Game of Life

# defining Cellular Automatons broadly as Class
class GameOfLife:
    def __init__(self, grid):
        self.grid = grid
        self.steps = 0

    # defining Moore neighborhood as function
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

    # update grid after every step by rules
    def update(self):
        current_grid = self.grid
        new_grid = np.zeros((current_grid.shape[0], current_grid.shape[1]))

        for row, col in np.ndindex(current_grid.shape):
            neighborhood = self.moore_neighborhood(row, col)
            counter_alive_cells_in_neighborhood = 0

            for x in neighborhood:
                if current_grid[x] == 1:
                    counter_alive_cells_in_neighborhood += 1

            if current_grid[row, col] == 1 and (
                    counter_alive_cells_in_neighborhood == 2 or counter_alive_cells_in_neighborhood == 3):
                new_grid[row, col] = 1
            elif current_grid[row, col] == 1 and counter_alive_cells_in_neighborhood <= 2:
                new_grid[row, col] = 0
            elif current_grid[row, col] == 1 and counter_alive_cells_in_neighborhood > 3:
                new_grid[row, col] = 0
            elif current_grid[row, col] == 0 and counter_alive_cells_in_neighborhood == 3:
                new_grid[row, col] = 1
            else:
                new_grid[row, col] = 0

        self.grid = new_grid
        self.steps += 1

        return self.grid


############################################################################################################


global SCREEN, CLOCK
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)

WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400
BLOCK_SIZE = 1
NUMBER_OF_INITIAL_ALIVE_TILES = 100000

# setting random seed
np.random.seed(0)

grid = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH))

for i in range(NUMBER_OF_INITIAL_ALIVE_TILES):
    random_col = np.random.randint(0, WINDOW_WIDTH)
    random_row = np.random.randint(0, WINDOW_HEIGHT)

    if grid[random_row, random_col] == 0:
        grid[random_row, random_col] = 1

GAME_OF_LIFE = GameOfLife(grid)


def draw():
    grid_used_for_drawing = GAME_OF_LIFE.grid
    my_font = pygame.font.SysFont("Comic Sans MS", 10000)
    text_surface = my_font.render("Generation: " + str(GAME_OF_LIFE.steps), False, (200, 200, 200), (0, 0, 0))
    SCREEN.blit(text_surface, [50, 50])

    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            if grid_used_for_drawing[x, y] == 1:
                pygame.draw.rect(SCREEN, BLACK, rect, 1)
            else:
                pygame.draw.rect(SCREEN, WHITE, rect, 1)

    my_font = pygame.font.SysFont(None, 50)
    text_surface = my_font.render("Generation: " + str(GAME_OF_LIFE.steps), False, (200, 200, 200), (0, 0, 0))
    SCREEN.blit(text_surface, [0, 0])


def run():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Game Of Life")
    CLOCK = pygame.time.Clock
    SCREEN.fill(WHITE)
    pygame.time.wait(10000)
    while True:
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        GAME_OF_LIFE.update()


run()
