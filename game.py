from asyncio.log import logger
import logging
import numpy as np
import pygame

import game_utils
import resources

# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


class Bar:
    def __init__(self, x):
        self.x = x
        self.y = SCREEN_HEIGHT * 0.9
        self.width = 20
        self.height = 5
        self.color = (255, 255, 255)
        self.thickness = 0

    def check_within_boundaries(self, left_corner):
        if left_corner + self.width >= SCREEN_WIDTH or left_corner <= 0:
            return False
        return True

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 20, 5))

    def move_x(self, dx):
        if not self.check_within_boundaries(self.x + dx):
            logging.debug("Reached screen width")
            return
        self.x += dx


class Ball:
    def __init__(self):
        self.radius = 5
        self.x = SCREEN_WIDTH / 2
        self.y = self.radius
        print("x", self.x)
        print("y", self.y)
        # initial x velocity, can be positive or negative not zero

        random_angle = np.random.uniform(0, 1) * np.pi
        print(random_angle)
        self.v_x = np.cos(random_angle) * 10
        # velocity y
        self.v_y = np.sin(random_angle) * 10
        print("vx", self.v_x)
        print("vy", self.v_y)
        self.color = (255, 255, 255)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, [self.x, self.y], self.radius)

    def should_restart(self, try_y):
        if try_y > SCREEN_HEIGHT * 0.9:
            logging.debug("Ball at boundary y")
            return True
        return False

    def move(self):
        try_x = self.x + self.v_x
        try_y = self.y + self.v_y
        # check if not within boundaries
        # then reverse velocity and do not update position for now
        if should_bounce(try_x, try_y):
            try:
                normal = get_walls_normal(try_x, try_y)
                # turn normal pi/2 clockwise
                parallel = np.array([-normal[1], normal[0]])
            except Exception as exc:
                logger.critical("cannot find normal")
                raise
            orthogonal_component = (
                -np.dot(normal, np.array([self.v_x, self.v_y])) * normal
            )
            print("orthogonal", orthogonal_component)

            dot_product = np.dot(parallel, np.array([self.v_x, self.v_y]))
            parallel_component = dot_product * parallel
            print("parallel", parallel_component)

            self.v_x = orthogonal_component[0] + parallel_component[0]
            self.v_y = orthogonal_component[1] + parallel_component[1]
            print("new vx", self.v_x)
            print("new vy", self.v_y)
        elif self.should_restart(try_y):
            self.__init__()
            return
        self.x = try_x
        self.y = try_y


# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
run = True

bar = Bar(SCREEN_WIDTH * 0.5)  # initial bar position
ball = Ball()

last_event = ""
while run:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            print(pygame.key.name(event.key))
            if event.key == pygame.K_ESCAPE:
                run = False

            if event.key == pygame.K_RIGHT:
                last_event = "down_right"
            elif event.key == pygame.K_LEFT:
                last_event = "down_left"
        elif event.type == pygame.KEYUP:
            last_event = "up"

    if last_event == "down_right":
        bar.move_x(10)
    elif last_event == "down_left":
        bar.move_x(-10)

    screen.fill((0, 0, 0))
    ball.move()
    ball.draw(screen)
    bar.draw(screen)

    pygame.display.update()
