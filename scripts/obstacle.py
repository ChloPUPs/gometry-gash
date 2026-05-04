import pygame as pg
import random

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
            player.alive = False

class ObstacleSpawner:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.alive = []
        self.total_spawned = 0
        # Frames since last spawn
        self._frames = 0
        self._current_goal = random.randrange(20, 300)

        self.spawn()

    def spawn(self):
        self.alive.append(Obstacle(self.x, self.y))
        self.total_spawned += 1
        print("Spike spawned")

    def handle_spawning(self):
        self._frames += 1
        if self._frames > self._current_goal:
            self.spawn()
            self._current_goal = random.randrange(40, 300)
            self._frames = 0

    def remove_oob(self):
        """Remove all spikes off the screen to left."""
        for o in self.alive:
            if o.draw_x + o.rect.w < 0.0:
                self.alive.remove(o)
