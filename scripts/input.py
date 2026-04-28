import pygame as pg

class InputState:
    class EventInfo:
        def __init__(self, eventtype, key=True) -> None:
            self.held = False
            self.just_pressed = False
            self.just_released = False
            self.eventtype = eventtype

    def __init__(self):
        self.events = {
            'quit': self.EventInfo(pg.QUIT, False),
            'left': self.EventInfo(pg.K_LEFT),
            'right': self.EventInfo(pg.K_RIGHT),
            'down': self.EventInfo(pg.K_DOWN),
            'up': self.EventInfo(pg.K_UP),
            'space': self.EventInfo(pg.K_SPACE),
        }
    
    def update_just_pressed(self):
        """Makes just_pressed and just_released things just pressed."""
        for ekey in self.events:
            # Make sure just_pressed things are JUST pressed
            if self.events[ekey].just_pressed:
                self.events[ekey].just_pressed = False
            if self.events[ekey].just_released:
                self.events[ekey].just_released = False

    def update_input(self, event):
        for ekey in self.events:
            # Check event stuff for every non key thing in the thing
            if event.type == self.events[ekey].eventtype:
                self.events[ekey].just_pressed = True

            # Do the keys
            if event.type == pg.KEYDOWN:
                if event.key == self.events[ekey].eventtype:
                    self.events[ekey].held = True
                    self.events[ekey].just_pressed = True
            if event.type == pg.KEYUP:
                if event.key == self.events[ekey].eventtype:
                    self.events[ekey].held = False
                    self.events[ekey].just_released = True
