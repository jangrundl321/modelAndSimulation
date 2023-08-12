import random
import random
import sys
import pygame
import numpy as np

class Particle():
    def __init__(self, X, Y, max_velocity, min_lifespan, max_lifespan, downward_acc):
        self.X = X
        self.Y = Y
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-2, 0)
        self.downward_acc = downward_acc
        self.lifespan = random.randint(min_lifespan, max_lifespan)
        self.alive = True

    def update(self):
        self.vy += self.downward_acc
        self.X += self.vx
        self.Y += self.vy
        self.lifespan -= 10.0

        if self.lifespan < 0:
            self.alive = False

class ParticleSystem():
    def __init__(self, X, Y, max_velocity, min_lifespan, max_lifespan, downward_acc):
        self.X = X
        self.Y = Y
        self.max_velocity = max_velocity
        self.min_lifespan = min_lifespan
        self.max_lifespan = max_lifespan
        self.downward_acc = downward_acc
        self.particles = []
        self.stop_spawning = False

    def addParticles(self):
        self.particles.append(Particle(self.X, self.Y, self.max_velocity, self.min_lifespan, self.max_lifespan, self.downward_acc))

    def removeParticles(self):
        for x in self.particles:
            if not x.alive:
                self.particles.remove(x)

    def update(self):
        for p in self.particles:
            p.update()

global SCREEN, CLOCK

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600
BLACK = (0, 0, 0)
MAXVELOCITY = 0
MINLIFESPAN = 5
MAXLIFESPAN = 10
DOWNWARDACC = 0.05
RADIUS = 2
SPAWN_CHANCE = 0.02

systems = []

# setting random seed
np.random.seed(0)
def draw():
    if systems is not []:
        for s in systems:
            for p in s.particles:
                pygame.draw.circle(SCREEN, p.color, (p.X, p.Y), RADIUS)

def run():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("SimpleParticle SIm")
    CLOCK = pygame.time.Clock
    #pygame.time.wait(10000)
    while True:
        SCREEN.fill(BLACK)
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0]:
                X = pygame.mouse.get_pos()[0]
                Y = pygame.mouse.get_pos()[1]

                particleSystem = ParticleSystem(X, Y, MAXVELOCITY, MINLIFESPAN, MAXLIFESPAN, DOWNWARDACC)
                systems.append(particleSystem)

        for s in systems:
            s.update()
            if random.random() < SPAWN_CHANCE:
                s.addParticles()

        pygame.display.update()

run()