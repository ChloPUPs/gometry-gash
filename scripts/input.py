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
        }
    
    def update_input(self, event):
        for eventinfo in self.events.values():
            # Make sure just_pressed things are JUST pressed
            if eventinfo.just_pressed == True:
                eventinfo.just_pressed = False
            if eventinfo.just_released == True:
                eventinfo.just_released = False

            # Check event stuff for every non key thing in the thing
            if event.type == eventinfo.eventtype:
                eventinfo.just_pressed = True

            # Do the keys
            if event.type == pg.KEYDOWN:
                if event.key == eventinfo.eventtype:
                    eventinfo.held = True
                    eventinfo.just_pressed = True
            if event.type == pg.KEYUP:
                if event.key == eventinfo.eventtype:
                    eventinfo.held = False
                    eventinfo.just_released = True
