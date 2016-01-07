import pygame
from core.strategy import Strategy
from core.logger import Logger
import cockroach_hybrid
import cockroach_ai

class CockroachControl(Strategy):

    def setup(self):
        Logger.log_debug("Cockroach manual control")
        self.item.get_tank().subscribe(pygame.KEYDOWN, "key_down", self)

    def update(self):
        self.check_key_pressed()

    def clear(self):
        self.item.get_tank().unsubscribe(pygame.KEYDOWN, "key_down", self)
  
    def check_key_pressed(self):
        dx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.item.look_left()
            self.item.run()
        elif keys[pygame.K_d]:
            self.item.look_right()
            self.item.run()


    def key_down(self, event):
        if event.key == pygame.K_q:
            self.item.set_strategy(cockroach_ai.CockroachAI(self.item))
        elif event.key == pygame.K_h:
            self.item.set_strategy(cockroach_hybrid.CockroachHybrid(self.item))

