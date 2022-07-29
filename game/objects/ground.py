from pygame import Surface
from game.config import Images, Ground_config
from game.objects.abstract_object import GameObject


class Ground(GameObject):
    def __init__(self, x_start_position, y_start_position) -> None:
        self.x = x_start_position
        self.y = y_start_position
        self.ground_width = Images.GROUND.value.get_width()

    def move(self) -> None:
        self.x -= Ground_config.SPEED.value

        if self.x + self.ground_width < 0:
            self.x += self.ground_width * 2

    def draw(self, surface: Surface) -> None:
        surface.blit(
            source=Images.GROUND.value,
            dest=(self.x, self.y)
        )
