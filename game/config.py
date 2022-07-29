from enum import Enum
import pygame
from os.path import join


class Config(Enum):
    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 700

    pygame.font.init()
    POINTS_FONT = pygame.font.SysFont(
        name='arial',
        size=50,
        bold=True
    )
    POINTS_RGB = (250, 250, 250)
    POINTS_POSITION = (15, 15)

    BIRD_START_POSITION = dict(x=230, y=350)
    GROUND_START_HEIGHT = 650
    PIPE_START_X_POSITION = 800
    NEW_PIPES_X_POSITION = 600



class Images(Enum):
    def _load_image(image_name: str):
        return pygame.transform.scale2x(pygame.image.load(join('game/imgs', image_name)))

    BIRD_UP = _load_image('bird1.png')
    BIRD_MIDDLE = _load_image('bird2.png')
    BIRD_DOWN = _load_image('bird3.png')

    PIPE = _load_image('pipe.png')

    GROUND = _load_image('base.png')

    BACKGROUND = _load_image('bg.png')


class Bird_config(Enum):
    MAX_ROTATION = 15
    MIN_ROTATION = -60
    ROTATION_SPEED = 10
    ANIMATION_TIME = 5

    SPEED = 10.5


class Pipe_config(Enum):
    DISTANCE = dict(max=200, min=199)
    SPEED = 5


class Ground_config(Enum):
    SPEED = 5


if __name__ == "__main__":
    print("OK!")
