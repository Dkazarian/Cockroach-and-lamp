import pygame
from app.tank_item import TankItem
from strategies.lamp_control import LampControl
from core.animation import Animation


class Lamp(TankItem):

    

    def __init__(self, tank, position):
        TankItem.__init__(self, tank, position)
        self.load_settings(tank.settings)
        self.set_strategy(LampControl(self))
        self.set_animation("off")
        self.energy = False

    def load_settings(self, settings):
        self.LIGHTS_ON_EVENT = settings.getint('events','lights_on')
        self.LIGHTS_OFF_EVENT = settings.getint('events','lights_off')
        self.add_animation("off", Animation(self, [pygame.image.load(settings.get('lamp', 'image_1'))]))
        self.add_animation("on", Animation(self, [pygame.image.load(settings.get('lamp', 'image_2'))]))
        self.SPEED = settings.getint('lamp', 'speed')
     
    def toogle_light(self):
        self.set_energy(not self.energy)

    def set_energy(self, energy):
        if energy:
            self.set_animation("on")
            self.get_tank().post_event(self.LIGHTS_ON_EVENT, {'pos': self.get_position()})
            print("LIGHT: BZZZZZZZZ!!!")
        else:
            pygame.event.post(pygame.event.Event(self.LIGHTS_OFF_EVENT, {'pos':  self.get_position()}))
            self.set_animation("off")
        self.energy = energy
