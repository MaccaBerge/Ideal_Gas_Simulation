import pygame
import pygame_gui
from pygame import Vector2 as vector
from typing import Union, List, Tuple
import numpy as np

from settings import *
from container import Container
from particle import Particle
from ui.text import Text

class Closed_System:
    def __init__(self, closed_system_render_position: Union[list, tuple], closed_system_start_temperature: Union[float, int] = 200, closed_system_background_color: Union[list, tuple] = (255,255,255), 
                 container_width: int = 800, container_height: int = 300, container_start_volume_meters: float = 1, container_min_volume_meters: float = 0, container_max_volume_meters: float = 3, 
                 container_color: Union[list, tuple] = (0,0,0), 
                 container_cap_color: Union[list, tuple] = (255,0,0)) -> None:
        
        self.closed_system_render_position: Union[list, tuple] = closed_system_render_position
        self.closed_system_background_color: Union[list, tuple] = closed_system_background_color
        self.render_surface: pygame.Surface = pygame.Surface(CLOSED_SYSTEM_RENDER_SURFACE_SIZE)

        # containers
        self.container: Container = Container(self.closed_system_render_position, width = container_width, height = container_height, start_volume_meters = container_start_volume_meters, 
                                   min_volume_meters = container_min_volume_meters, max_volume_meters = container_max_volume_meters, 
                                   container_color = container_color, cap_color = container_cap_color)

        # particles
        self.particle_spawn_point = (self.container.position[0] + 30 - self.closed_system_render_position[0], self.container.position[1] + self.container.height - 30 - self.closed_system_render_position[0])
        self.particles = []

        # simulation
        self.temperature = closed_system_start_temperature
        self.previous_temperature = self.temperature

        self.volume = self.container.get_volume_meters()

        self.accurate_pressure = self.calculate_accurate_pressure()

        # ui
        self.volume_text = Text(f"Volume: {self.container.get_volume_meters()} m", 26, (50+50,320))
        self.pressure_text = Text(f"Pressure: {self.container.get_volume_meters()} Pa", 26, (250+50,320))
        self.temperature_text = Text(f"Temperature: {self.temperature} K", 26, (500+50,320))
    
    def calculate_velocities(self, temperature: Union[float, int], number_of_particles: int) -> List[Tuple[float, float]]:

        # Calculate average speed
        avg_speed = np.sqrt(3 * BOLTZMANNS_CONSTANT * temperature / PARTICLE_MASS)
        
        # Generate speeds from a Maxwell-Boltzmann distribution
        speeds = np.random.normal(loc=avg_speed, scale=0.1 * avg_speed, size=number_of_particles)
        
        # Generate random angles for each velocity
        angles = np.random.uniform(0, 2 * np.pi, number_of_particles)
        
        # Calculate velocity components based on speeds and angles
        velocities_x = speeds * np.cos(angles)
        velocities_y = speeds * np.sin(angles)
        
        # Combine velocity components into 2D velocities
        velocities = np.column_stack((velocities_x, velocities_y))

        # Adjust total kinetic energy
        current_kinetic_energy = 0.5 * PARTICLE_MASS * np.sum(velocities**2)
        target_kinetic_energy = number_of_particles * 0.5 * PARTICLE_MASS * avg_speed**2
        if current_kinetic_energy == 0:
            return [(0.0, 0.0) for _ in range(number_of_particles)]
        scaling_factor = np.sqrt(target_kinetic_energy / current_kinetic_energy)
        velocities *= scaling_factor

        # Adjust velocities to fit simulation
        velocities *= 0.2

        return list(map(tuple, velocities))
    
    def calculate_accurate_pressure(self) -> None:
        accurate_pressure = ((len(self.particles) / (AVOGADROS_CONSTANT)) * GAS_CONSTANT * self.temperature) / self.container.get_volume_meters()
        return f"{accurate_pressure:.{2}e}"

    def assign_velocity_to_particles(self, velocities: List[list]):
        for index, particle in enumerate(self.particles):
            particle.velocity = vector(velocities[index])

    def add_particles(self, number_of_particles: int = 10, color = (0,0,255)) -> None:
        velocities = self.calculate_velocities(self.temperature, number_of_particles)

        for i in range(number_of_particles):
            x = self.particle_spawn_point[0]
            y = self.particle_spawn_point[1]
            vx = velocities[i][0]
            vy = velocities[i][1]

            self.particles.append(Particle((x, y), (vx, vy), radius=PARTICLE_RADIUS, color=color))
    
    def update_particles(self, dt: float, update_particles_movement: bool = True) -> None:
        total_momentum_change = 0
        for particle in self.particles:
            particle_momentum_change = particle.update(self.container.get_container_bounds((-self.closed_system_render_position[0], -self.closed_system_render_position[1])), self.particles, dt, update_movement = update_particles_movement)
            total_momentum_change += particle_momentum_change
        return total_momentum_change
    
    def update_particle_temperature(self) -> None:
        if self.previous_temperature == 0:
            velocities = self.calculate_velocities(self.temperature, len(self.particles))
            self.assign_velocity_to_particles(velocities)
            return
        
        scaling = np.sqrt(self.temperature / self.previous_temperature) if self.temperature > 0 else 0

        for particle in self.particles:
            particle.velocity *= scaling
    
    def adjust_temperature(self, temperature_adjustment: Union[float, int]) -> None:
        self.previous_temperature = self.temperature
        self.temperature = max(0, self.previous_temperature + temperature_adjustment)
        self.update_particle_temperature()
    
    def set_temperature(self, new_temperature: Union[float, int]) -> None:
        self.previous_temperature = self.temperature
        self.temperature = max(0, min(new_temperature, MAX_TEMPERATURE))
        self.update_particle_temperature()

    def update_ui(self) -> None:
        self.volume_text.set_text(f"Volume: {self.volume} m")
        self.pressure_text.set_text(f"Pressure: {self.accurate_pressure} Pa")
        self.temperature_text.set_text(f"Temperature: {self.temperature} K")
    
    def render_ui(self, render_surface: pygame.Surface) -> None:
        self.volume_text.render(render_surface)
        self.pressure_text.render(render_surface)
        self.temperature_text.render(render_surface)

    def render(self, render_surface: pygame.Surface) -> None:
        self.render_surface.fill(self.closed_system_background_color)
        self.container.render(self.render_surface, offset=(-self.closed_system_render_position[0], -self.closed_system_render_position[1]))

        for particle in self.particles:
            particle.render(self.render_surface)
        
        self.render_ui(self.render_surface)
        render_surface.blit(self.render_surface, self.closed_system_render_position)

    def update(self, dt: float, update_particles_movement: bool = True) -> None:
        self.container.update()
        self.volume = self.container.get_volume_meters()

        momentum_change = self.update_particles(dt, update_particles_movement)

        self.accurate_pressure = self.calculate_accurate_pressure()

        self.update_ui()
        
        