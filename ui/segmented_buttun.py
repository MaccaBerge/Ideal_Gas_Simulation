import pygame
import pygame_gui
from typing import Union

class Segmented_Button:
    def __init__(self, manager: pygame_gui.UIManager, position: Union[list, tuple], values: Union[list, tuple], buttons_width: int = 100, buttons_height: int = 50, 
                 buttons_col_separation: int = 10, buttons_row_separation: int = 10, number_of_columns: int = 2, row_offset: int = 75, object_id: str = "segmented_button"):
        self.manager = manager
        self.position = position
        self.values = values
        self.buttons_width = buttons_width
        self.buttons_height = buttons_height
        self.buttons_col_separation = buttons_col_separation
        self.buttons_row_separation = buttons_row_separation
        self.number_of_columns = number_of_columns
        self.row_offset = row_offset
        self.object_id = object_id

        self.buttons = self._create_buttons(self.values)
    
        self.selected_button = self.buttons[0]
        self.selected_button.select()
        self.selected_value = self._get_selected_value()
    
    def _get_selected_value(self) -> str:
        return self.selected_button.text
    
    def _create_buttons(self, values: list) -> list:
        buttons = []
        for index, value in enumerate(values):
            row = index // self.number_of_columns
            col = index % self.number_of_columns
            button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((self.position[0] + (self.buttons_width + self.buttons_col_separation) * col +(row*self.row_offset), self.position[1] + (self.buttons_height + self.buttons_row_separation) * row), 
                                                    (self.buttons_width, self.buttons_height))), text=str(value), manager=self.manager, object_id=self.object_id)
            buttons.append(button)
        return buttons

    def handle_events(self, event: pygame.Event) -> None:
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            self.process_selected_button(event.ui_element)
    
    def process_selected_button(self, pressed_button) -> None:
        if pressed_button not in self.buttons:
            return
        
        for button in self.buttons:
            if button == pressed_button:
                self.selected_button = button
                self.selected_button.select()
                self.selected_value = self._get_selected_value()
            else:
                button.unselect()

