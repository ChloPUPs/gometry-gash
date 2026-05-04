import pygame as pg
import sys
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
    input_state = InputState()

    # Game stuff
    game_state = 'gameplay'
    highscore = 0

    # Get highscore from save file
    try:
        with open('./data/save.txt', 'r') as f:
            content = f.read()
            try:
                highscore = int(content[content.index('hs:') + 3:])
            except ValueError, IndexError:
                ...
    except FileNotFoundError:
        ...

    GROUND_Y = float(screen.height - 120)

    player = Player(x_offset=200,
            y=GROUND_Y - 32,
            ground_y=GROUND_Y)

    pg.display.set_icon(player.image)
    pg.display.set_caption("Gometry Gash")

    spike_spawner = ObstacleSpawner(
            screen.width + 16 + player.x - player.x_offset,
            GROUND_Y - 16)

    death_timer = 0

    while True:
        input_state.update_just_pressed()
        for event in pg.event.get():
            input_state.update_input(event)

        if input_state.events['quit'].just_pressed:
            pg.quit()
            sys.exit()

        if game_state == 'gameplay':
            # Update position of spike spawner to always be at screen end
            spike_spawner.x = screen.width + 16 + player.x - player.x_offset

            spike_spawner.remove_oob()
            spike_spawner.handle_spawning()

            player.update(input_state)
            player.apply_velocity()

            for s in spike_spawner.alive:
                s.handle_collision(player)

            if not player.alive:
                game_state = 'death'
                with open('./data/save.txt', 'w') as f:
                    if spike_spawner.total_spawned > highscore:
                        highscore = spike_spawner.total_spawned
                        f.write(f'hs:{spike_spawner.total_spawned}')

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
                    f"Spikes Observed: {spike_spawner.total_spawned}\nLocal Record: {highscore}",
                    Vector2(10, 10),
                    "./data/font/inter.ttf",
                    16,
                    (0, 0, 0))
        elif game_state == 'death':
            screen.fill('white')
            display_text(screen, f"dieded\nscore: {spike_spawner.total_spawned}",
                    Vector2(screen.width / 2, screen.height / 2),
                    "./data/font/inter.ttf")

            player.x = 0.0
            player.y = GROUND_Y - 32
            spike_spawner.x = screen.width + 16 + player.x - player.x_offset
            player.rotation = 0.0
            spike_spawner.alive = []

            death_timer += 1
            if death_timer >= 120:
                death_timer = 0
                player.alive = True
                spike_spawner.total_spawned = 0
                game_state = 'gameplay'
                spike_spawner.spawn()

        clock.tick(TARGET_FRAMERATE)
        pg.display.flip()

if __name__ == '__main__':
    main()
