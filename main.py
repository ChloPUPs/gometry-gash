import pygame as pg
import sys
from scripts.input import InputState
from scripts.space import Vector2

class Player:
    def __init__(self, x, y):
        self.SPEED = 4

        self.rect = pg.FRect(x, y, 32.0, 32.0)
        self.direction = Vector2(0.0, 0.0)
        self.velocity = Vector2(0.0, 0.0)
        self.image = pg.image.load("./data/art/player.png")

    def update(self, input_state):
        self.direction.x = (
            -input_state.events['left'].held
            + input_state.events['right'].held
            )

        self.direction.y = (
            -input_state.events['up'].held
            + input_state.events['down'].held
            )
        
        self.velocity.x = self.direction.x * self.SPEED
        self.velocity.y = self.direction.y * self.SPEED

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

    player = Player(30, screen.height * (1 / 3))

    while True:
        for event in pg.event.get():
            input_state.update_input(event)

        if input_state.events['quit'].just_pressed:
            pg.quit()
            sys.exit()

        player.update(input_state)
        player.apply_velocity()

        screen.fill((255, 255, 255))

        screen.blit(player.image, player.rect)

        clock.tick(TARGET_FRAMERATE)
        pg.display.flip()

if __name__ == '__main__':
    main()
