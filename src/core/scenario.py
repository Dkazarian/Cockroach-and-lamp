import pygame
import sys
from logger import Logger
from event_manager import EventManager


class Scenario:


    def __init__(self, background=None):
        
        if background!=None:
            self.set_background(background)

        self.event_manager = EventManager()
        self.subscribe(pygame.QUIT, "quit", self)

        self.items = pygame.sprite.Group()


    def set_background(self, background):
        self.background = pygame.image.load(background)
        self.size = self.background.get_size()
        self.surface = pygame.display.set_mode(self.size)
        self.backgroundRect = self.background.get_rect()
        self.set_limits( (0, 0, self.size[0], self.size[1]))


    def set_limits(self, limits):
        self.limits = limits

    def add(self, item):
        self.items.add(item)
        Logger.log_debug("Added "+ str(item))

    def remove(self, item):
        self.items.remove(item)
        Logger.log_debug("Removed "+ str(item))

    def render(self):
        self.surface.blit(self.background, self.backgroundRect)
        self.items.draw(self.surface)
        pygame.display.flip()

    def subscribe(self, event, action, handler):
        self.event_manager.add(event, action, handler)
        Logger.log_debug("Event "+str(event)+" subscribed "+str(handler)+"#"+str(action))


    def unsubscribe(self, event, action, handler):
        self.event_manager.remove(event, action, handler)
        Logger.log_debug("Event "+str(event)+" unsubscribed "+str(handler)+"#"+str(action))

    def post_event(self, code, info):
        pygame.event.post(pygame.event.Event(code, info))
        
    def update(self):
        self.event_manager.handle(pygame.event.get())
        self.items.update()

    def quit(self, event):
        pygame.quit()
        sys.exit()

    def position_allowed(self, item, position):
        half_size = (item.get_size()[0]/2, item.get_size()[1]/2)
        if position[0] - half_size[0] < self.limits[0]:
            return False
        if position[1] - half_size[0] < self.limits[1]:
            return False
        if position[0] + half_size[0] > self.limits[2]:
            return False
        if position[1] + half_size[1] > self.limits[3]:
            return False
        return True