import pygame
from core.strategy import Strategy

class LampControl(Strategy):

    def setup(self):
        self.item.get_tank().subscribe(pygame.KEYDOWN, "key_down", self)

    def update(self):
        self.check_key_pressed()

    def clear(self):
        self.item.get_tank().unsubscribe(pygame.KEYDOWN, "key_down", self)
  
    def check_key_pressed(self):
        dx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            dx = -self.item.SPEED
        elif keys[pygame.K_RIGHT]:
            dx = self.item.SPEED
        self.item.move(dx, 0)
        if self.item.energy:
            self.item.get_tank().post_event(self.item.LIGHTS_ON_EVENT, {'pos': self.item.get_position()})


    def key_down(self, event):
        if event.key == pygame.K_SPACE:
            self.item.toogle_light()
