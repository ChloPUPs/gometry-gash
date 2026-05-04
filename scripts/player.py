import pygame as pg
from .space import Vector2
from .utils import round_to_mult

class Player:
    def __init__(self, x_offset, y, ground_y):
        self.SPEED = 4.0
        self.JUMP_STRENGTH = 6.0

        self.rect = pg.FRect(0.0, y, 32.0, 32.0)
        self.x_offset = x_offset
        self.velocity = Vector2(0.0, 0.0)
        self.image = pg.image.load("./data/art/player.png")
        self.rotation = 0.0
        self.alive = True

        self._ground_y = ground_y

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, val):
        self.rect.x = val

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, val):
        self.rect.y = val

    @property
    def w(self):
        return self.rect.w

    @property
    def h(self):
        return self.rect.h

    @property
    def draw_dest(self):
        return (self.x_offset, self.y)

    @property
    def in_floor(self):
        return self.y + self.h >= self._ground_y

    @property
    def on_floor(self):
        return self.y + self.h + 1.0 >= self._ground_y

    def update(self, input_state):
        self.velocity.x = self.SPEED

        # Gravity
        self.velocity.y += 0.3

        # Ground Collision
        if self.in_floor:
            self.velocity.y = 0.0
            self.y = self._ground_y - self.h
            self.rotation = round_to_mult(self.rotation, 90)
        else:
            self.rotation -= 4.4

        assert input_state.__class__.__name__ == "InputState", "oops"

        # Jump
        if (
                (
                    input_state.events['space'].held
                    or input_state.events['up'].held
                    or input_state.events['mouse1'].held
                    )
                and self.on_floor
            ):
            self.velocity.y = -self.JUMP_STRENGTH

    def apply_velocity(self):
        self.x += self.velocity.x
        self.y += self.velocity.y
