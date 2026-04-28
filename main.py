import pygame as pg
import sys

def main():
    pg.init()

    screen = pg.display.set_mode((720, 360))

    test_image = pg.image.load("./data/art/player.png")

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    test_image = pg.transform.flip(test_image, False, True)

        screen.fill((255, 255, 255))

        # Draw the test image!!
        screen.blit(
                test_image,
                (screen.width / 2, screen.height / 2),
        )

        pg.display.flip()

if __name__ == '__main__':
    main()
