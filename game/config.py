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


class Images(Enum):
   def _load_image(image_name : str):
      return pygame.transform.scale2x(pygame.image.load(join('game/imgs', image_name)))

   BIRD_UP = _load_image('bird1.png')
   BIRD_MIDDLE = _load_image('bird2.png')
   BIRD_DOWN = _load_image('bird3.png')

   PIPE = _load_image('pipe.png')

   GROUND = _load_image('base.png')

   BACKGROUND = _load_image('bg.png')


if __name__ == "__main__":
   print("OK!")
   