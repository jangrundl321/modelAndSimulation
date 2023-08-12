import math
import random

WINDOW_HEIGHT = 300
WINDOW_WIDTH = 300
MARGIN_FACTOR = 50
LEFTMARGIN = MARGIN_FACTOR
RIGHTMARGIN = WINDOW_WIDTH - MARGIN_FACTOR
BOTTOMMARGIN = MARGIN_FACTOR
UPPERMARGIN = WINDOW_HEIGHT - MARGIN_FACTOR


class Boid():
    def __init__(self, max_velocity):
        self.X = random.randint(LEFTMARGIN, RIGHTMARGIN)
        self.Y = random.randint(BOTTOMMARGIN, UPPERMARGIN)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.max_velocity = max_velocity
        self.vx = random.randint(1, self.max_velocity)
        self.vy = random.randint(1, self.max_velocity)


class BoidFlock():
    def __init__(self, boids: [Boid], separation_range, separation_factor, visible_range, alignment_factor,
                 cohesion_factor, turn_factor, minspeed, maxspeed):
        self.boids = boids
        self.separation_range = separation_range
        self.separation_factor = separation_factor
        self.visible_range = visible_range
        self.alignment_factor = alignment_factor
        self.cohesion_factor = cohesion_factor
        self.turn_factor = turn_factor
        self.minspeed = minspeed
        self.maxspeed = maxspeed

    def update(self):
        for boid in self.boids:

            xpos_avg = 0
            ypos_avg = 0
            xvel_avg = 0
            yvel_avg = 0
            neighboring_boids = 0
            close_dx = 0
            close_dy = 0

            for otherboid in self.boids:
                if boid == otherboid:
                    continue

                # Compute differences in x and y coordinates
                dx = boid.X - otherboid.X
                dy = boid.Y - otherboid.Y

                # Are both those differences less than the visual range?
                if (abs(dx) < self.visible_range and abs(dy) < self.visible_range):

                    # If so, calculate the squared distance
                    squared_distance = dx * dx + dy * dy

                    # Is squared distance less than the protected range?
                    if (squared_distance < self.separation_range):

                        # If so, calculate difference in x/y-coordinates to nearfield boid
                        close_dx += boid.X - otherboid.X
                        close_dy += boid.Y - otherboid.Y

                    # If not in protected range, is the boid in the visual range?
                    elif (squared_distance < self.visible_range * self.visible_range):

                        # Add other boid's x/y-coord and x/y vel to accumulator variables
                        xpos_avg += otherboid.X
                        ypos_avg += otherboid.Y
                        xvel_avg += otherboid.vx
                        yvel_avg += otherboid.vy

                        neighboring_boids += 1

            if (neighboring_boids > 0):

                xpos_avg = xpos_avg / neighboring_boids
                ypos_avg = ypos_avg / neighboring_boids
                xvel_avg = xvel_avg / neighboring_boids
                yvel_avg = yvel_avg / neighboring_boids

                boid.vx = (boid.vx +
                           (xpos_avg - boid.X) * self.cohesion_factor +
                           (xvel_avg - boid.vx) * self.alignment_factor)

                boid.vy = (boid.vy +
                           (ypos_avg - boid.Y) * self.cohesion_factor +
                           (yvel_avg - boid.vy) * self.alignment_factor)

            # Add the avoidance contribution to velocity
            boid.vx = boid.vx + (close_dx * self.separation_factor)
            boid.vy = boid.vy + (close_dy * self.separation_factor)

            # If the boid is near an edge, make it turn by turnfactor
            # (this describes a box, will vary based on boundary conditions)
            if boid.X < LEFTMARGIN:
                boid.vx = boid.vx + self.separation_factor
            if boid.X > RIGHTMARGIN:
                boid.vx = boid.vx - self.separation_factor
            if boid.Y > BOTTOMMARGIN:
                boid.vy = boid.vy - self.separation_factor
            if boid.Y < UPPERMARGIN:
                boid.vy = boid.vy + self.separation_factor

            speed = math.sqrt(boid.vx * boid.vx + boid.vy * boid.vy)


            if speed < self.minspeed:
                boid.vx = (boid.vx / speed) * self.minspeed
                boid.vy = (boid.vy / speed) * self.minspeed
            if speed > self.maxspeed:
                boid.vx = (boid.vx / speed) * self.maxspeed
                boid.vy = (boid.vy / speed) * self.maxspeed

            boid.X = boid.X + boid.vx
            boid.Y = boid.Y + boid.vy
