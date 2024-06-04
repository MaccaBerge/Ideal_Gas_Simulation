import pygame
from typing import Union

class Container:
    def __init__(self, position: Union[list, tuple], width: int = 800, height: int = 300, start_volume_meters: float = 1, min_volume_meters: float = 0, 
                 max_volume_meters: float = 3, container_color: Union[list, tuple] = (0,0,0), cap_color: Union[list, tuple] = (255,0,0)) -> None:
        
        self.position: Union[list, tuple] = position

        self.width: int = width
        self.height: int = height

        self.start_volume_meters: float = start_volume_meters
        self.volume_meters: float = self.start_volume_meters
        self.min_volume_meters: float = min_volume_meters
        self.max_volume_meters: float = max_volume_meters
        self.volume_meters_heigth: float = self.height / self.max_volume_meters

        self.volume_meters_pixel_ratio = self.width / self.max_volume_meters

        self.cap_hitbox_size: tuple = (50, self.height)
        self.cap_hitbox: pygame.Rect = pygame.Rect(self.position[0] + (self.volume_meters * self.volume_meters_pixel_ratio) - (self.cap_hitbox_size[0] / 2), 
                                                   self.position[1], self.cap_hitbox_size[0], self.cap_hitbox_size[1])
        self.mouse_to_cap_offset_x: int = 0
        self.drag_cap_active: bool = False

        self.container_color: Union[list, tuple] = container_color
        self.cap_color: Union[list, tuple] = cap_color

        self.last_left_mouse_button_state = False
        self.left_mouse_button_clicked = False
        self.left_mouse_button_holding = False
    
    def get_volume_meters(self) -> float:
        """ Returns the volume in meters (the length of the container). """
        return round(self.volume_meters, 2)
    
    def get_container_bounds(self, offset: Union[list, tuple] = (0,0)) -> dict:
        """ Returns the bounds of the container. """
        return {"top": self.position[1] + offset[1], "bottom": self.position[1] + self.height + offset[1], "left": self.position[0] + offset[0], "right": self.cap_hitbox.centerx + offset[0]}

    def render(self, render_surface: pygame.Surface, offset: Union[list, tuple] = (0,0)) -> None:
        """ Renders the container with all its components to a surface. """
        left_side_line_positions = ((self.position[0] + offset[0], self.position[1] + offset[1]), (self.position[0] + offset[0], self.position[1] + self.height + offset[1]))

        top_side_line_positions = ((self.position[0] + offset[0], self.position[1] + offset[1]), (self.position[0] + self.width + offset[0], self.position[1] + offset[1]))
        bottom_side_line_positions = ((self.position[0] + offset[0], self.position[1] + self.height + offset[1]), (self.position[0] + self.width + offset[0], self.position[1] + self.height + offset[1]))

        cap_line_positions = ((self.position[0] + int(self.volume_meters * self.volume_meters_pixel_ratio) + offset[0], self.position[1] + offset[1]), 
                              (self.position[0] + int(self.volume_meters * self.volume_meters_pixel_ratio) + offset[0], self.position[1] + self.height + offset[1]))
        
        #cap_hitbox_adjusted = pygame.Rect(self.cap_hitbox.left + offset[0], self.cap_hitbox.top + offset[1], self.cap_hitbox.width, self.cap_hitbox.height)

        pygame.draw.line(render_surface, self.container_color, left_side_line_positions[0], left_side_line_positions[1])
        pygame.draw.line(render_surface, self.container_color, top_side_line_positions[0], top_side_line_positions[1])
        pygame.draw.line(render_surface, self.container_color, bottom_side_line_positions[0], bottom_side_line_positions[1])

        #pygame.draw.rect(render_surface, (0,0,100), cap_hitbox_adjusted)
        pygame.draw.line(render_surface, self.cap_color, cap_line_positions[0], cap_line_positions[1])
    
    def _inputs(self) -> None:
        """ Updates the click and holding of the left mouse button. """
        mouse_buttons = pygame.mouse.get_pressed()
        left_mouse_button_state = mouse_buttons[0]

        self.left_mouse_button_clicked = True if (not self.last_left_mouse_button_state and left_mouse_button_state) else False
        
        self.left_mouse_button_holding = True if self.left_mouse_button_clicked else self.left_mouse_button_holding 
        self.left_mouse_button_holding = False if (not left_mouse_button_state and self.last_left_mouse_button_state) else self.left_mouse_button_holding
            
        self.last_left_mouse_button_state = left_mouse_button_state

    def _drag_cap_line(self) -> None:
        """ Handles the drag of the cap line. """
        mouse_position = pygame.mouse.get_pos()
        if self.left_mouse_button_clicked and self.cap_hitbox.collidepoint(mouse_position):
            self.drag_cap_active = True
            self.mouse_to_cap_offset_x = mouse_position[0] - self.cap_hitbox.centerx

        self.drag_cap_active = False if not self.left_mouse_button_holding else self.drag_cap_active
        
        if self.drag_cap_active:
            self.cap_hitbox.centerx = mouse_position[0] - self.mouse_to_cap_offset_x
        
        self.cap_hitbox.centerx = max(self.position[0] + (self.min_volume_meters * self.volume_meters_pixel_ratio), min(self.cap_hitbox.centerx, self.position[0] + self.max_volume_meters * self.volume_meters_pixel_ratio))

        self.volume_meters = (self.cap_hitbox.centerx - self.position[0]) / self.volume_meters_pixel_ratio

    def update(self) -> None:
        """ Updates the container. """
        self._inputs()
        self._drag_cap_line()

        #print(self.volume_meters)
        
