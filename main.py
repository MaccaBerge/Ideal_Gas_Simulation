import pygame

from settings import *
from simulation import Simulation


class Main:
    def __init__(self) -> None:
        pygame.init()
        self.display_width, self.display_height = DISPLAY_WIDTH, DISPLAY_HEIGHT
        self.display = pygame.display.set_mode((self.display_width, self.display_height))#, pygame.FULLSCREEN)
        pygame.display.set_caption("Ideal Gas Simulation")

        self.simulation = Simulation()
    
    def run(self) -> None:
        self.simulation.run()


if __name__ == "__main__":
    main = Main()
    main.run()