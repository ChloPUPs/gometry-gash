import pygame as pg
import sys
from scripts.input import InputState
from scripts.space import Vector2

class Player:
    def __init__(self, x_offset, y):
        self.SPEED = 4.0
        self.JUMP_STRENGTH = 6.0

        self.rect = pg.FRect(0.0, y, 32.0, 32.0)
        self.x_offset = x_offset
        self.velocity = Vector2(0.0, 0.0)
        self.image = pg.image.load("./data/art/player.png")

    @property
    def draw_dest(self):
        return (self.x_offset, self.rect.y)

    def update(self, input_state):
        self.velocity.x = self.SPEED

        assert input_state.__class__.__name__ == "InputState", "oops"

        #print(input_state.events['space'].just_pressed)

        if input_state.events['space'].just_pressed:
            self.velocity.y = -self.JUMP_STRENGTH

        # Gravity
        self.velocity.y += 0.3

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

    player = Player(x_offset=200, y=screen.height - 140)

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
