import pygame
from strategy import Strategy
from logger import Logger

class Item(pygame.sprite.Sprite):

    
    def __init__(self, scenario, position=(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.scenario = scenario
        self.position = position
        self.strategy = None
        self.set_strategy(Strategy(self))
        self.animations = {}
        self.current_animation = None

    def set_scenario(scenario):
        self.scenario = scenario

    def update(self):
        self.strategy.update()
        self.current_animation.update()

    def get_x(self):
        return self.get_position()[0]

    def get_y(self):
        return self.get_position()[1]

    def move(self, dx, dy, force=False):
        return self.set_position((self.get_x() + dx, self.get_y() + dy), force)

    def set_position(self, position, force=False):
        if force or self.scenario.position_allowed(self, position):
            self.position = position
            self.rect.center = position
            return True
        else:
            Logger.log_debug(str(self) + " position not allowed " + str(position))
            return False

    def set_animation(self, name):
        self.current_animation = self.animations[name]
        self.animation_name = name
        self.current_animation.setup()
        self.set_position(self.position)
        self.play_animation()

    def add_animation(self, name, animation):
        self.animations[name] = animation
        if self.current_animation is None:
            self.current_animation = animation

    def get_animation(self):
        return self.current_animation

    def play_animation(self):
        self.current_animation.play()

    def pause_animation(self):
        self.current_animation.pause()

    def get_position(self):
        return self.position

    def set_strategy(self, strategy):
        if self.strategy != None:
            self.strategy.clear()
        self.strategy = strategy
        strategy.setup()

    def set_image(self, image):
        self.image = image 
        self.rect = image.get_rect()
        self.size = image.get_size()

    def get_size(self):
        return self.size

