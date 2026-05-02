import pygame as pg
from .space import Vector2

def center_rot_blit(surface, source, angle, topleft):
    rotated = pg.transform.rotate(source, angle)
    dest = rotated.get_rect(center=source.get_rect(topleft=topleft).center)
    surface.blit(rotated, dest)

def round_to_mult(num, mult):
    return mult * round(num / mult)

def display_text(
        screen,
        text, pos,
        font_path,
        size=32,
        color=(255, 0, 0)):
    """Creates font, renders it with your choices, and displays it."""
    font = pg.font.Font(font_path, size)
    render = font.render(text, True, color)
    screen.blit(render, (int(pos.x), int(pos.y)))
