import pygame
from app.tank_item import TankItem
from core.animation import Animation
from strategies.cockroach_ai import CockroachAI
from strategies.cockroach_control import CockroachControl
from strategies.cockroach_hybrid import CockroachHybrid
from core.logger import Logger
import random

class Cockroach(TankItem):

    RIGHT = 0
    LEFT = 1
    SPEED_MOD = [1, -1]

    def __init__(self, tank, position):
        TankItem.__init__(self, tank, position)
        self.load_settings(tank.settings)
        self.set_direction(Cockroach.RIGHT)
        random.seed()

    def load_settings(self, settings):
        self.run_directions = {Cockroach.RIGHT: 'run_right', Cockroach.LEFT: 'run_left'}
        picture_1 = pygame.image.load(settings.get('cockroach', 'image_1'))
        picture_1_l = pygame.transform.flip(picture_1, True, False)
        picture_2 = pygame.image.load(settings.get('cockroach', 'image_2'))
        picture_2_l = pygame.transform.flip(picture_2, True, False)
        self.add_animation(self.run_directions[Cockroach.LEFT], Animation(self, [picture_1_l, picture_2_l], False))
        self.add_animation(self.run_directions[Cockroach.RIGHT], Animation(self, [picture_1, picture_2], False))
        self.SPEED = settings.getint('cockroach', 'speed')
        self.FORGETFULLNESS = settings.getint('cockroach', 'forgetfullness')
        self.RANDOM_THOUGHTS = settings.get('cockroach', 'thoughts').split('||')
        self.thoughts = None
        self.thoughts_time = 0
        self.idle_time = 0
        self.status = None

        if settings.get('cockroach', 'hybrid') == "1":
            self.set_strategy(CockroachHybrid(self))
        else:
            self.set_strategy(CockroachAI(self))

    def set_direction(self, direction):
        self.direction = direction
        self.set_animation(self.run_directions[direction])

    def toggle_direction(self):
        Logger.log_debug("Changed direction")
        if self.direction == Cockroach.RIGHT:
            self.set_direction(Cockroach.LEFT)
        else:
            self.set_direction(Cockroach.RIGHT)

    def run(self):
        if not self.move(self.traslation(), 0):
            self.strategy.handle_collission()
        self.play_animation()

    def look_left(self):
        self.set_direction(Cockroach.LEFT)

    def look_right(self):
        self.set_direction(Cockroach.RIGHT)

    def traslation(self):
        return self.SPEED*self.SPEED_MOD[self.direction]

    def speak(self, message):
        print("COCKROACH: " + message)

    def think(self):
        if self.thoughts is None:
            self.idle_time = self.idle_time + 1
            if self.idle_time > random.randrange(400, 8000, 1):
                self.thoughts = random.choice(self.RANDOM_THOUGHTS)
                self.idle_time = 0
        else:
            if self.thoughts_time == 0:
                self.speak(self.thoughts)
            self.thoughts_time = self.thoughts_time + 1
            if self.thoughts_time > self.FORGETFULLNESS:
                self.thoughts_time = 0
                self.thoughts = None 

    def update(self):
        TankItem.update(self)        

    def set_status(self, status):
        if self.status is None or self.status != status:
            self.status = status
            Logger.log_debug("Status: " + status)
