import pygame as pg
import sys
import random
from scripts.input import InputState
from scripts.utils import center_rot_blit, display_text
from scripts.space import Vector2
from scripts.obstacle import ObstacleSpawner
from scripts.player import Player

def main():
    pg.init()

    # Important thing things
    screen = pg.display.set_mode((720, 360))
    clock = pg.Clock()
    TARGET_FRAMERATE = 60

    # Game stuff
    input_state = InputState()

    GROUND_Y = float(screen.height - 120)

    player = Player(x_offset=200,
            y=GROUND_Y - 32,
            ground_y=GROUND_Y)

    pg.display.set_icon(player.image)
    pg.display.set_caption("Gometry Gash")

    spike_spawner = ObstacleSpawner(
            screen.width + 16 + player.x - player.x_offset,
            GROUND_Y - 16)

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

        for s in spike_spawner.alive:
            s.handle_collision(player)

        screen.fill((0, 200, 255))

        for s in spike_spawner.alive:
            s.draw_x = s.x - player.x + player.x_offset
            screen.blit(s.image, (s.draw_x, s.y))

        center_rot_blit(screen,
                player.image,
                player.rotation,
                player.draw_dest)

        pg.draw.rect(screen,
                (0, 200, 0),
                pg.Rect(0, GROUND_Y, screen.width, screen.height - GROUND_Y))

        display_text(screen,
                f"Spikes Observed: {spike_spawner.total_spawned}",
                Vector2(10, 10),
                "./data/font/inter.ttf",
                16,
                (0, 0, 0))

        clock.tick(TARGET_FRAMERATE)
        pg.display.flip()

if __name__ == '__main__':
    main()
