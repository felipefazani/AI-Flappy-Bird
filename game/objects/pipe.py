import pygame
from random import randrange
from game.config import Images, Pipe_config
from game.objects.bird import Bird


class Pipe:
   def __init__(self, x_start_position) -> None:
      self.x = x_start_position
      self.top_pipe = pygame.transform.flip(
         surface=Images.PIPE.value, 
         flip_x=False, 
         flip_y= True
      )
      self.ground_pipe = Images.PIPE.value
      self.left_screen = False

      self.height = randrange(start=25, stop=475)
      self.top_position = self.height - self.top_pipe.get_height()

      max_value = Pipe_config.DISTANCE.value['max']
      min_value = Pipe_config.DISTANCE.value['min']
      self.ground_position = self.height + randrange(start=min_value, stop=max_value)

   def move(self) -> None:
      self.x -= Pipe_config.SPEED.value

   def draw(self, surface : pygame.Surface) -> None:
      surface.blit(source=self.top_pipe, dest=(self.x, self.top_position))
      surface.blit(source=self.ground_pipe, dest=(self.x, self.ground_position))

   def colision(self, bird : Bird) -> bool:
      bird_mask = bird.get_mask()
      top_mask = pygame.mask.from_surface(surface=self.top_pipe)
      ground_mask = pygame.mask.from_surface(surface=self.ground_pipe)

      x_distance = self.x - bird.x
      top_colision = bird_mask.overlap(
         top_mask, 
         (x_distance, self.top_position - bird.y)
      )
      ground_colision = bird_mask.overlap(
         ground_mask, 
         (x_distance, self.ground_position - bird.y)
      )

      if ground_colision or top_colision:
         return True
      else:
         return False

