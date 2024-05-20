import pygame
from pygame import Vector2 as vector
from typing import Union

class Particle:
    def __init__(self, position: Union[vector, list, tuple], velocity: Union[vector, list, tuple], mass: float = 5, radius: int = 10, color: Union[list, tuple] = (0,0,180)) -> None:
        self.position: vector = vector(position)
        self.velocity: vector = vector(velocity)
        self.mass: float = mass
        self.radius: int = radius

        self.color: Union[list, tuple] = color

        self.image = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.image.set_colorkey((0,0,0))

    def render(self, render_surface: pygame.Surface) -> None:
        render_surface.blit(self.image, self.position)

    def update(self) -> None:
        pass