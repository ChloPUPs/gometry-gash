import pygame as pg
import sys
from scripts.input import InputState
from scripts.space import Vector2

class Player:
    def __init__(self, x_offset, y, ground_y):
        self.SPEED = 4.0
        self.JUMP_STRENGTH = 6.0

        self.rect = pg.FRect(0.0, y, 32.0, 32.0)
        self.x_offset = x_offset
        self.velocity = Vector2(0.0, 0.0)
        self.image = pg.image.load("./data/art/player.png")
        self._ground_y = ground_y

    @property
    def draw_dest(self):
        return (self.x_offset, self.rect.y)
    
    @property
    def in_floor(self):
        return self.rect.y + self.rect.h >= self._ground_y
    
    @property
    def on_floor(self):
        return self.rect.y + self.rect.h + 1.0 >= self._ground_y

    def update(self, input_state):
        self.velocity.x = self.SPEED

        # Gravity
        self.velocity.y += 0.3

        # Ground Collision
        if self.in_floor:
            self.velocity.y = 0.0
            self.rect.y = self._ground_y - self.rect.h

        assert input_state.__class__.__name__ == "InputState", "oops"

        if input_state.events['space'].just_pressed and self.on_floor:
            self.velocity.y = -self.JUMP_STRENGTH

    def apply_velocity(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

def main():
    pg.init()

    # Important thing things
    screen = pg.display.set_mode((720, 360))
    clock = pg.Clock()
    TARGET_FRAMERATE = 60

    # Game stuff
    input_state = InputState()

    player = Player(x_offset=200,
            y=screen.height - 142,
            ground_y=screen.height - 120)

    while True:
        input_state.update_just_pressed()
        for event in pg.event.get():
            input_state.update_input(event)

        if input_state.events['quit'].just_pressed:
            pg.quit()
            sys.exit()

        player.update(input_state)
        player.apply_velocity()

        screen.fill((255, 255, 255))

        screen.blit(player.image, player.draw_dest)

        clock.tick(TARGET_FRAMERATE)
        pg.display.flip()

if __name__ == '__main__':
    main()
