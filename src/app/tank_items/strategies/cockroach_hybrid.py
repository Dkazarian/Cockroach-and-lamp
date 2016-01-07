import pygame
from core.strategy import Strategy
from core.logger import Logger
import cockroach_control
import cockroach_ai


class CockroachHybrid(Strategy):

    def setup(self):
        self.ai = cockroach_ai.CockroachAI(self.item)
        self.ai.setup()
        self.control =  cockroach_control.CockroachControl(self.item)
        self.control.setup()

    def update(self):
        self.ai.update()
        if not self.item.status == "PANIC":
            self.control.update()

    def clear(self):
        self.ai.clear()
        self.control.clear()
    
    def handle_collission(self):
        self.ai.handle_collission()    