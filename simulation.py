import pygame
import pygame_gui
from sys import exit
from typing import Union

import pygame_gui.ui_manager

from settings import *
from closed_system import Closed_System
from ui.segmented_buttun import Segmented_Button
from ui.text import Text

class Simulation:
    def __init__(self) -> None:
        self.display = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        self.paused = False
        self.update_particle_movement = True

        self.top_system = Closed_System((40,75), container_min_volume_meters=1.5, container_max_volume_meters=10, container_start_volume_meters=10, closed_system_start_temperature=800)

        self.top_system.add_particles(number_of_particles=NUMBER_OF_PARTICLES)
        self.top_system.add_particles(number_of_particles=1, color=(255,0,0))
        
        self.bottom_system = Closed_System((40,425), container_min_volume_meters=1.5, container_max_volume_meters=10, container_start_volume_meters=10, closed_system_start_temperature=800)

        self.bottom_system.add_particles(number_of_particles=NUMBER_OF_PARTICLES)
        self.bottom_system.add_particles(number_of_particles=1, color=(255,0,0))

        # ui
        self.ui_manager = pygame_gui.UIManager(self.display.get_size(), UI_THEME_PATH)

        # system switch
        self.system_switch = Segmented_Button(self.ui_manager, (910, 100), ["Top System", "Bottom System", "Both Systems"], buttons_width=140)
        self.selected_system = self.system_switch.selected_value
        self.last_selected_system = self.selected_system

        self.system_switch_text = Text("Select System", 30, (988, 80))

        self.top_system_update_particle_movement = True
        self.bottom_system_update_particle_movement = True

        self.top_system_skip_frame = False
        self.bottom_system_skip_frame = False

        self.top_system_paused = False
        self.bottom_system_paused = False

        # change temperature
        self.change_temperature_text = Text("Change Temperature", 30, (950, 280))

        self.decrease_temperature_button = pygame_gui.elements.UIButton(pygame.Rect((995-40, 300), (50, 50)), "-", self.ui_manager, object_id="temperature_button")
        self.increase_temperature_button = pygame_gui.elements.UIButton(pygame.Rect((1100+5, 300), (50, 50)), "+", self.ui_manager, object_id="temperature_button")

        self.temperature_entry_line = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((1065-60, 300), (100, 49)), manager=self.ui_manager, object_id="text_entry_line")
        self.temperature_entry_line.set_text(str(self.top_system.temperature))

        # frame skips
        self.frame_skip_text = Text("Skip Frames", 30, (992, 415))
        self.frame_skip_button = pygame_gui.elements.UIButton(pygame.Rect((1030, 435), (50, 50)), ">>", self.ui_manager, object_id="frame_skip_button")
        
        # play / pause
        self.play_pause_text = Text("Play/Pause", 30, (1000, 540))
        self.play_pause_button = pygame_gui.elements.UIButton(pygame.Rect((997, 560), (120, 50)), "Play/Pause", self.ui_manager, object_id="frame_skip_button")

        self.made_by_text = Text("A Proud Macca® Production.", 30, (920, 720), color=(100,100,100,100))

    def adjust_temperature(self, temperature_adjustment: Union[float, int]) -> None:
        if self.selected_system == "Top System" or self.selected_system == "Both Systems":
            self.top_system.adjust_temperature(temperature_adjustment)
            self.temperature_entry_line.set_text(str(self.top_system.temperature))
        if self.selected_system == "Bottom System" or self.selected_system == "Both Systems":
            self.bottom_system.adjust_temperature(temperature_adjustment)
            self.temperature_entry_line.set_text(str(self.bottom_system.temperature))
    
    def set_temperature(self, new_temperature: Union[float, int]) -> None:
        if self.selected_system == "Top System" or self.selected_system == "Both Systems":
            self.top_system.set_temperature(new_temperature)
        if self.selected_system == "Bottom System" or self.selected_system == "Both Systems":
            self.bottom_system.set_temperature(new_temperature)
    
    def pause_resume(self) -> None:
        if self.selected_system == "Top System" or self.selected_system == "Both Systems":
            self.top_system_paused = not self.top_system_paused
        if self.selected_system == "Bottom System" or self.selected_system == "Both Systems":
            self.bottom_system_paused = not self.bottom_system_paused
    
    def frame_skipping(self) -> None:
        if (self.selected_system == "Top System" or self.selected_system == "Both Systems") and self.top_system_paused:
            self.top_system_skip_frame = True
        else:
            self.top_system_skip_frame = False
        
        if (self.selected_system == "Bottom System" or self.selected_system == "Both Systems") and self.bottom_system_paused:
            self.bottom_system_skip_frame = True
        else:
            self.bottom_system_skip_frame = False
        
        self.top_system_update_particle_movement = self.top_system_skip_frame
        self.bottom_system_update_particle_movement = self.bottom_system_skip_frame
    
    def draw_text(self) -> None:
        self.system_switch_text.render(self.display)
        self.change_temperature_text.render(self.display)
        self.frame_skip_text.render(self.display)
        self.play_pause_text.render(self.display)
        self.made_by_text.render(self.display)
    
    def handle_temperature_ui(self) -> None:
        temperature_text = self.temperature_entry_line.get_text()

        if not temperature_text.isnumeric() or len(temperature_text) == 0:
            return
        
        if self.selected_system != self.last_selected_system:
            if self.selected_system == "Top System":
                self.temperature_entry_line.set_text(str(self.top_system.temperature))
            if self.selected_system == "Bottom System":
                self.temperature_entry_line.set_text(str(self.bottom_system.temperature))
        
        if float(temperature_text) > MAX_TEMPERATURE:
            self.temperature_entry_line.set_text(str(MAX_TEMPERATURE))
        
        temperature = min(max(0, float(temperature_text)), MAX_TEMPERATURE)

        
        self.set_temperature(temperature)
    
    def run(self) -> None:
        
        while True:
            dt = self.clock.tick(TARGET_FPS) / 1000
            self.last_selected_system = self.selected_system
            self.selected_system = self.system_switch.selected_value

            self.top_system_update_particle_movement = False if self.top_system_paused else True
            self.bottom_system_update_particle_movement = False if self.bottom_system_paused else True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit() 
                        exit()
                    if event.key == pygame.K_SPACE:
                        self.pause_resume()
                    if event.key == pygame.K_RIGHT:
                        self.frame_skipping()
                    if event.key == pygame.K_UP:
                        self.adjust_temperature(TEMPERATURE_ADJUSTMENT)
                    if event.key == pygame.K_DOWN:
                        self.adjust_temperature(-TEMPERATURE_ADJUSTMENT)
                
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    pressed_button = event.ui_element
                    if pressed_button == self.decrease_temperature_button:
                        self.adjust_temperature(-TEMPERATURE_ADJUSTMENT)
                    if pressed_button == self.increase_temperature_button:
                        self.adjust_temperature(TEMPERATURE_ADJUSTMENT)
                    if pressed_button == self.frame_skip_button:
                        self.frame_skipping()
                    if pressed_button == self.play_pause_button:
                        self.pause_resume()
                
                # ui
                self.system_switch.handle_events(event)
                
                self.ui_manager.process_events(event)

            self.display.fill(BACKGROUND_COLOR)

            dt = 0.007 if self.paused else dt

            self.top_system.update(dt, update_particles_movement=self.top_system_update_particle_movement)
            self.top_system.render(self.display)

            self.bottom_system.update(dt, update_particles_movement=self.bottom_system_update_particle_movement)
            self.bottom_system.render(self.display)

            self.handle_temperature_ui()

            # ui
            self.ui_manager.update(dt)
            self.ui_manager.draw_ui(self.display)

            self.draw_text()

            pygame.display.update()
