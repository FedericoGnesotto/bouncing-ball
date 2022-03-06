import numpy as np

from resources.game_constants import *


def get_walls_normal(x, y):
    if x <= 0:
        return np.array([1, 0])
    elif x >= SCREEN_WIDTH:
        return np.array([-1, 0])
    elif y <= 0:
        return np.array([0, -1])
    raise Exception("Not at wall!")


def should_bounce(try_x, try_y):
    if try_x < SCREEN_WIDTH and try_x > 0 and try_y < SCREEN_HEIGHT:
        return False
    return True
