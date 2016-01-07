from core.strategy import Strategy
from core.logger import Logger
import cockroach_hybrid
import cockroach_control
import pygame
import math
import random

class CockroachAI(Strategy):

    def setup(self):
        Logger.log_debug("Cockroach AI")
        self.item.get_tank().subscribe(self.item.get_settings().getint('events', 'lights_on'), "light_detected", self)
        self.item.get_tank().subscribe(self.item.get_settings().getint('events', 'lights_off'), "safe", self)
        self.LIGHT_TOLERANCE = self.item.get_settings().getint('cockroach', 'light_tolerance')
        self.LIGHT_COMMENTS = self.item.get_settings().get('cockroach', 'thoughts_light').split('||')
        self.COLLISION_INERCE = self.item.get_settings().getint('cockroach', 'direction_lock_duration')
        self.THOUGHTS_LIGHT = self.item.get_settings().get('cockroach', 'thoughts_light').split('||')
        self.item.get_tank().subscribe(pygame.KEYDOWN, "key_down", self)
        self.direction_lock = 0
        random.seed()

    def update(self):
        self.item.think()

    def clear(self):
        self.item.get_tank().unsubscribe(self.item.get_settings().getint('events', 'lights_on'), "light_detected", self)
        self.item.get_tank().unsubscribe(self.item.get_settings().getint('events', 'lights_off'), "light_detected", self)
        self.item.get_tank().unsubscribe(pygame.KEYDOWN, "key_down", self)
   
    def light_detected(self, event):
        
        if math.fabs(event.pos[0]-self.item.get_x()) < self.safe_distance():
            self.item.thoughts = random.choice(self.THOUGHTS_LIGHT)
            self.run_away(event)
            self.item.set_status("PANIC")
        else:
            self.item.set_status("")

    def safe_distance(self):
        safe_distance = self.LIGHT_TOLERANCE        
        if self.item.status == "PANIC":
            safe_distance = safe_distance*1.3
        return safe_distance

    def safe(self, event):
        self.item.set_status("OK")

    def run_away(self, event):
        if not self.direction_locked():
            self.decide_direction(event)
        else:
            self.update_direction_lock()
        self.item.run()

    def decide_direction(self, event):
        distance = event.pos[0]-self.item.get_x()
        if math.fabs(distance) > self.item.SPEED:
            if distance > 0:
                self.item.set_direction(self.item.LEFT)
            else:
                self.item.set_direction(self.item.RIGHT)

    def handle_collission(self):
        self.item.toggle_direction()
        self.lock_direction()
        self.item.run()
    
    def lock_direction(self):
        Logger.log_debug("Direction locked")
        self.direction_lock = self.COLLISION_INERCE

    def direction_locked(self):
        return self.direction_lock > 0

    def update_direction_lock(self):
        self.direction_lock = self.direction_lock - self.item.SPEED
        if self.direction_lock < 0:
            Logger.log_debug("Direction unlocked") 

    def key_down(self, event):
        if event.key == pygame.K_q:
            self.item.set_strategy(cockroach_control.CockroachControl(self.item))
        elif event.key == pygame.K_h:
            self.item.set_strategy(cockroach_hybrid.CockroachHybrid(self.item))