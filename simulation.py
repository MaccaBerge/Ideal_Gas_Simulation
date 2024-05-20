import pygame
from sys import exit

from settings import *
from container import Container
from closed_system import Closed_System

class Simulation:
    def __init__(self) -> None:
        self.display = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        self.closed_system = Closed_System((200,200), container_min_volume_meters=0.5)
    
    def run(self) -> None:
        
        while True:
            dt = self.clock.tick(TARGET_FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.display.fill((255,255,255))

            self.closed_system.update()
            self.closed_system.render(self.display)

            pygame.display.update()
