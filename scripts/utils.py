import pygame as pg

def center_rot_blit(surface, source, angle, topleft):
    rotated = pg.transform.rotate(source, angle)
    dest = rotated.get_rect(center=source.get_rect(topleft=topleft).center)
    surface.blit(rotated, dest)
