import pygame
from typing import Union

class Text:
    def __init__(self, text: str, size: int, position: Union[list, tuple], font: Union[str, None] = None, color: Union[list, tuple] = (0,0,0)) -> None:
        self.text = str(text)
        self.size = size
        self.font = font
        self.color = color
        self.position = position

        self.font = pygame.font.Font(self.font, self.size)
        self.rendered_text = self.font.render(self.text, True, self.color)
        self.rect = self.rendered_text.get_rect(midleft = self.position)
    
    def set_text(self, new_text: str) -> None:
        self.text = str(new_text)
        self.rendered_text = self.font.render(self.text, True, self.color)
        self.rect = self.rendered_text.get_rect(midleft = self.position)

    def render(self, display_surface: pygame.Surface) -> None:
        display_surface.blit(self.rendered_text, self.rect)