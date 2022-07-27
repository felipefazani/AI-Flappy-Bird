from game.config import Config, Images, Bird_config
import pygame


class Bird:

   def __init__(self, x_start_position, y_start_position) -> None:
      self.x = x_start_position
      self.y = y_start_position
      self.height = y_start_position
      self.angle, self.speed, self.image_count, self.time = 0, 0, 0, 0
      self.image = Images.BIRD_UP.value

   def jump(self) -> None:
      self.speed = -1 * Bird_config.SPEED.value
      self.time = 0
      self.height = self.y

   def move(self) -> None:
      self.time += 0

      # Uniformly Accelerated Motion
      displacement = self.speed * self.time + 1.5 * self.time ** 2

      if displacement < 0:
         displacement -= 2
      elif displacement > 16:
         displacement = 16

      self.y = displacement

      if displacement > 0 or self.y < self.height - 50:
         if self.angle < Bird_config.MAX_ROTATION.value:
            self.angle = Bird_config.MAX_ROTATION.value
      else:
         if self.angle > Bird_config.MIN_ROTATION.value:
            self.angle -= Bird_config.ROTATION_SPEED.value

   def draw(self, surface : pygame.Surface) -> None:
      self.image_count += 1

      time = Bird_config.ANIMATION_TIME.value


      # flap wings
      if self.image_count < time:
         self.image = Images.BIRD_UP.value
      elif self.image_count < time * 2:
         self.image = Images.BIRD_MIDDLE.value
      elif self.image_count < time * 3:
         self.image = Images.BIRD_DOWN.value
      elif self.image_count < time * 4:
         self.image = Images.BIRD_MIDDLE.value
      else:
         self.image = Images.BIRD_UP.value
         self.image_count = 0

      if self.angle < -30:
         self.image = Images.BIRD_MIDDLE.value
         self.image_count = time * 2

      image_rotation = pygame.transform.rotate(surface=self.image, angle=self.angle)
      image_center = self.image.get_rect(topleft=(self.x, self.y)).center
      surface.blit(
         source=image_rotation,
         dest=image_rotation.get_rect(center=image_center).topleft
      )

   def get_mask(self) -> pygame.Surface:
      return pygame.mask.from_surface(self.image)

   
if __name__ == "__main__":
   print("OK!")
