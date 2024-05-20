import pygame
from typing import Union
from random import uniform

from settings import *
from container import Container
from particle import Particle

class Closed_System:
    def __init__(self, closed_system_render_position: Union[list, tuple], closed_system_background_color: Union[list, tuple] = (255,255,255), container_width: int = 800, container_height: int = 300, 
                 container_start_volume_meters: float = 1, container_min_volume_meters: float = 0, container_max_volume_meters: float = 3, container_color: Union[list, tuple] = (0,0,0), 
                 container_cap_color: Union[list, tuple] = (255,0,0)) -> None:
        
        self.closed_system_render_position: Union[list, tuple] = closed_system_render_position
        self.closed_system_background_color: Union[list, tuple] = closed_system_background_color
        self.render_surface: pygame.Surface = pygame.Surface(CLOSED_SYSTEM_RENDER_SURFACE_SIZE)

        # containers
        self.container: Container = Container(self.closed_system_render_position, width = container_width, height = container_height, start_volume_meters = container_start_volume_meters, 
                                   min_volume_meters = container_min_volume_meters, max_volume_meters = container_max_volume_meters, 
                                   container_color = container_color, cap_color = container_cap_color)

        # particles
        self.particles = []

    def add_particles(self, container: Container, temperature: float, number_of_particles: int = 10) -> None:
        bounds = container.get_container_bounds()

        for _ in range(number_of_particles):
            x = uniform(bounds["left"] + PARTICLE_RADIUS, bounds["right"] - PARTICLE_RADIUS)
            y = uniform(bounds["top"] + PARTICLE_RADIUS, bounds["bottom"] - PARTICLE_RADIUS)
            self.particles.append(Particle())

        print(bounds)
    
    def render(self, render_surface: pygame.Surface) -> None:
        self.render_surface.fill(self.closed_system_background_color)
        self.container.render(self.render_surface, offset=(-self.closed_system_render_position[0], -self.closed_system_render_position[1]))

        render_surface.blit(self.render_surface, self.closed_system_render_position)
    
    def update(self) -> None:
        self.container.update()

        print(self.container.get_container_bounds())
        