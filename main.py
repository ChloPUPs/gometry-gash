# TODO: add spikes observed counter

import pygame as pg
import sys
import random
from scripts.input import InputState
from scripts.space import Vector2
from scripts.utils import center_rot_blit, round_to_mult

class Player:
    def __init__(self, x_offset, y, ground_y):
        self.SPEED = 4.0
        self.JUMP_STRENGTH = 6.0

        self.rect = pg.FRect(0.0, y, 32.0, 32.0)
        self.x_offset = x_offset
        self.velocity = Vector2(0.0, 0.0)
        self.image = pg.image.load("./data/art/player.png")
        self.rotation = 0.0

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
                    )
                and self.on_floor
            ):
            self.velocity.y = -self.JUMP_STRENGTH

    def apply_velocity(self):
        self.x += self.velocity.x
        self.y += self.velocity.y

    def kill(self):
        print("oh no dead")

class Obstacle:
    def __init__(self, cx, y):
        self.draw_x = -1.0
        self.image = pg.transform.scale(
                pg.image.load("./data/art/spike.png"),
                (32, 32))
        self.rect = self.image.get_rect(w=24, center=(cx, y))

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

    def handle_collision(self, player):
        if self.rect.colliderect(player.rect):
            player.kill()

class ObstacleSpawner:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.spawned = []
        # Frames since last spawn
        self._frames = 0
        self._current_goal = random.randrange(20, 300)

        self.spawn()

    def spawn(self):
        self.spawned.append(Obstacle(self.x, self.y))
        print("Spike spawned")

    def handle_spawning(self):
        self._frames += 1
        if self._frames > self._current_goal:
            random.randrange(20, 300)
            self.spawn()
            self._current_goal = random.randrange(20, 300)
            self._frames = 0

    def remove_oob(self):
        """Remove all spikes off the screen to left."""
        for o in self.spawned:
            if o.draw_x + o.rect.w < 0.0:
                self.spawned.remove(o)

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

    pg.display.set_icon(player.image)
    pg.display.set_caption("Gometry Gash")

    spike_spawner = ObstacleSpawner(
            screen.width + 16 + player.x - player.x_offset,
            player.y + 6)

    while True:
        input_state.update_just_pressed()
        for event in pg.event.get():
            input_state.update_input(event)

        if input_state.events['quit'].just_pressed:
            pg.quit()
            sys.exit()

        # Update position of spike spawner to always be at screen end
        spike_spawner.x = screen.width + 16 + player.x - player.x_offset

        spike_spawner.remove_oob()
        spike_spawner.handle_spawning()

        player.update(input_state)
        player.apply_velocity()

        for s in spike_spawner.spawned:
            s.handle_collision(player)

        screen.fill((0, 200, 255))

        for s in spike_spawner.spawned:
            s.draw_x = s.x - player.x + player.x_offset
            screen.blit(s.image, (s.draw_x, s.y))

        center_rot_blit(screen,
                player.image,
                player.rotation,
                player.draw_dest)

        clock.tick(TARGET_FRAMERATE)
        pg.display.flip()

if __name__ == '__main__':
    main()
