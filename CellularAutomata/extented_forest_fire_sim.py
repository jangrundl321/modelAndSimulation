import random
import sys
import pygame
import numpy as np

# CA: Forest Fire
# defining Cellular Automatons broadly as Class

STREET = 0
YOUNG_TREE = 1
GROWING_TREE = 2
TREE = 3
WEAK_FIRE = 4
BURNING_FIRE = 5
NEW_FIRE = 6

ALPHA = 0.01
BETA = 0.3
DELTA = 0.000005


class ForestFireCA:

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
            counter_fire_in_neighborhood = 0

            for x in neighborhood:
                if current_grid[x] == NEW_FIRE or current_grid[x] == WEAK_FIRE or current_grid[x] == BURNING_FIRE:
                    counter_fire_in_neighborhood += 1

            if current_grid[row, col] == STREET:
                new_grid[row, col] = STREET
            elif current_grid[row, col] == YOUNG_TREE:
                if random.random() <= ALPHA:
                    new_grid[row, col] = GROWING_TREE
                else:
                    new_grid[row, col] = YOUNG_TREE
            elif current_grid[row, col] == GROWING_TREE:
                if random.random() <= ALPHA:
                    new_grid[row, col] = TREE
                elif counter_fire_in_neighborhood > 0 and random.random() <= BETA:
                    new_grid[row, col] = NEW_FIRE
                elif random.random() <= DELTA:
                    new_grid[row, col] = NEW_FIRE
                else:
                    new_grid[row, col] = GROWING_TREE
            elif current_grid[row, col] == TREE:
                if counter_fire_in_neighborhood > 0 and random.random() <= BETA:
                    new_grid[row, col] = NEW_FIRE
                elif random.random() <= DELTA:
                    new_grid[row, col] = NEW_FIRE
                else:
                    new_grid[row, col] = TREE
            elif current_grid[row, col] == WEAK_FIRE:
                new_grid[row, col] = YOUNG_TREE
            elif current_grid[row, col] == BURNING_FIRE:
                new_grid[row, col] = WEAK_FIRE
            elif new_grid[row, col] == NEW_FIRE:
                new_grid[row, col] = BURNING_FIRE

        self.grid = new_grid
        self.steps += 1

        return self.grid


#######################################################################################################

global SCREEN, CLOCK
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREY = (211, 211, 211)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BROWN = (255,248,220)
GREEN = (0, 255, 0)
LIGHT_GREEN = (144, 238, 144)
DARK_GREEN = (0, 100, 0)

WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400
BLOCK_SIZE = 1
NUMBER_OF_TREE_TILES = 10000
NUMBER_OF_STREET_TILES = 200
NUMBER_OF_NEW_FIRE_TILES = 1000

# setting random seed
np.random.seed(0)

grid = np.ones((WINDOW_HEIGHT, WINDOW_WIDTH))

for i in range(NUMBER_OF_NEW_FIRE_TILES):
    random_col = np.random.randint(0, WINDOW_WIDTH)
    random_row = np.random.randint(0, WINDOW_HEIGHT)
    grid[random_row, random_col] = NEW_FIRE

for i in range(NUMBER_OF_STREET_TILES):
    random_col = np.random.randint(0, WINDOW_WIDTH)
    random_row = np.random.randint(0, WINDOW_HEIGHT)
    grid[random_row, random_col] = STREET

for i in range(NUMBER_OF_TREE_TILES):
    random_col = np.random.randint(0, WINDOW_WIDTH)
    random_row = np.random.randint(0, WINDOW_HEIGHT)
    grid[random_row, random_col] = TREE

ForestFireCA = ForestFireCA(grid)


def draw():
    grid_used_for_drawing = ForestFireCA.grid

    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            if grid_used_for_drawing[x, y] == STREET:
                pygame.draw.rect(SCREEN, GREY, rect, 1)
            elif grid_used_for_drawing[x, y] == TREE:
                pygame.draw.rect(SCREEN, DARK_GREEN, rect, 1)
            elif grid_used_for_drawing[x, y] == GROWING_TREE:
                pygame.draw.rect(SCREEN, GREEN, rect, 1)
            elif grid_used_for_drawing[x, y] == WEAK_FIRE:
                pygame.draw.rect(SCREEN, YELLOW, rect, 1)
            elif grid_used_for_drawing[x, y] == NEW_FIRE:
                pygame.draw.rect(SCREEN, RED, rect, 1)
            elif grid_used_for_drawing[x, y] == BURNING_FIRE:
                pygame.draw.rect(SCREEN, ORANGE, rect, 1)
            elif grid_used_for_drawing[x, y] == YOUNG_TREE:
                pygame.draw.rect(SCREEN, LIGHT_GREEN, rect, 1)

    my_font = pygame.font.SysFont(None, 50)
    text_surface = my_font.render("Generation: " + str(ForestFireCA.steps), False, (200, 200, 200), (0, 0, 0))
    SCREEN.blit(text_surface, [0, 0])


def run():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Forest Fire CA")
    CLOCK = pygame.time.Clock
    SCREEN.fill(BROWN)
    pygame.time.wait(10000)
    while True:
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        ForestFireCA.update()


run()
