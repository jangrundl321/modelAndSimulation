import sys

import numpy as np
import pygame

from helpers import Boid
from helpers import BoidFlock

WINDOW_HEIGHT = 300
WINDOW_WIDTH = 300

TURNFACTOR = 0.3
VISUALRANGE = 20
SEPARATIONRANGE = 8
ALIGNMENTFACTOR = 0.0005
SEPARATIONFACTOR = 0.20
COHESIONFACTOR = 0.02
MAXSPEED = 3
MINSPEED = 1
MAXVELOCITY = 25
BLOCK_SIZE = 1
BLACK = (0, 0, 0)
NUMBEROFBOIDSPERFLOCK = 100
NUMBEROFFLOCKS = 5

global SCREEN, CLOCK

# setting random seed
#np.random.seed(0)
flocks = []
for x in range(NUMBEROFFLOCKS):
    boids = []
    for x in range(NUMBEROFBOIDSPERFLOCK):
        boid = Boid(MAXVELOCITY)
        boids.append(boid)

    boidFlock = BoidFlock(boids, SEPARATIONRANGE, SEPARATIONFACTOR, VISUALRANGE, ALIGNMENTFACTOR, COHESIONFACTOR, TURNFACTOR, MINSPEED, MAXSPEED)
    flocks.append(boidFlock)
def draw():

    f = []
    for x in flocks:
        f += x.boids

    for boid in f:
        rect = pygame.Rect(boid.X, boid.Y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(SCREEN, boid.color, rect, 1)


def run():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Boids")
    CLOCK = pygame.time.Clock
    SCREEN.fill(BLACK)
    #pygame.time.wait(10000)
    while True:
        SCREEN.fill(BLACK)
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        for x in flocks:
            x.update()


run()