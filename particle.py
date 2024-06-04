import pygame
from pygame import Vector2 as vector
from typing import Union

from settings import *

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

        self.rect: pygame.Rect = self.image.get_rect(center = self.position)

    def render(self, render_surface: pygame.Surface) -> None:
        pygame.draw.circle(render_surface, self.color, self.rect.center, self.radius)

    def move(self, dt: float):
        self.position += self.velocity * dt
        self.rect.center = self.position
    
    def collision(self, container_bounds: dict, other: Union[list, tuple], exchange_velocities: bool = True) -> None:

        for particle in other:
            if particle is not self:
                distance_vector = self.position - particle.position
                distance = distance_vector.length()
                min_distance = self.radius + particle.radius

                if distance < min_distance and distance > 0:
                    # Move particles apart so they don't overlap
                    overlap = min_distance - distance
                    move_vector = distance_vector.normalize() * (overlap / 2)
                    self.position += move_vector
                    particle.position -= move_vector

                    # Update rect centers to new positions
                    self.rect.center = self.position
                    particle.rect.center = particle.position

                    # Elastic collision: exchange velocities
                    if exchange_velocities:
                        normal = distance_vector.normalize()
                        relative_velocity = self.velocity - particle.velocity
                        velocity_along_normal = relative_velocity.dot(normal)

                        restitution = 1 # For a perfectly elastic collision
                        impulse_magnitude = -(1 + restitution) * velocity_along_normal / (1 / self.mass + 1 / particle.mass)

                        impulse = impulse_magnitude * normal
                        self.velocity += impulse / self.mass
                        particle.velocity -= impulse / particle.mass
        
        momentum_change_x = 0
        momentum_change_y = 0
        
        if self.rect.left < container_bounds["left"]:
            momentum_change_x += 2 * self.mass * abs(self.velocity.x)
            self.rect.left = container_bounds["left"]
            self.position.x = self.rect.centerx
            self.velocity.x *= -1
        if self.rect.right > container_bounds["right"]:
            momentum_change_x += 2 * self.mass * abs(self.velocity.x)
            self.rect.right = container_bounds["right"]
            self.position.x = self.rect.centerx
            self.velocity.x *= -1
        if self.rect.top < container_bounds["top"]:
            momentum_change_y += 2 * self.mass * abs(self.velocity.y)
            self.rect.top = container_bounds["top"]
            self.position.y = self.rect.centery
            self.velocity.y *= -1
        if self.rect.bottom > container_bounds["bottom"]:
            momentum_change_y += 2 * self.mass * abs(self.velocity.y)
            self.rect.bottom = container_bounds["bottom"]
            self.position.y = self.rect.centery
            self.velocity.y *= -1
        
        total_momentum_change = momentum_change_x + momentum_change_y
        
        return total_momentum_change

    def color_lerping(self, value: Union[float, int], max_value: Union[float, int] = 600) -> None:
        # Clamp the value between 0 and max_value
        value = max(0, min(value, max_value))
        
        # Calculate the interpolation proportion
        proportion = value / max_value
        
        # Interpolate each color component
        start_color = (0, 0, 255)  # Blue
        end_color = (255, 0, 0)    # Red
        
        r = int(start_color[0] + (end_color[0] - start_color[0]) * proportion)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * proportion)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * proportion)
        
        return (r, g, b)

    def update(self, container_bounds: dict, other: Union[list, tuple], dt: float, update_movement: bool = True) -> None:
        if update_movement:
            self.move(dt)
        momentum_change = self.collision(container_bounds, other, update_movement)
        self.color = self.color_lerping(self.velocity.length())

        return momentum_change

