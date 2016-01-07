import pygame
from app.tank import Tank

pygame.init()
FPS = 30
clock = pygame.time.Clock()
tank = Tank()

while True:
    tank.update()
    tank.render()
    clock.tick(FPS)
