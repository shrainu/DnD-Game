# import internal modules
from src.engine.game_manager import Game_Manager
import src.engine.scene_manager as SceneManager
from src.engine.mouse_handler import MouseHandler
import src.engine.ui.ui_elements as UIElements
import src.engine.ui.ui_alternative as UIAlternatives
import src.engine.debugger as Debugger
import src.engine.timer as Time
import src.player.player_class.player_classes as PlayerClass
import src.player.player_race.player_races as PlayerRace
# import external modules
import sys
import pygame as pg


class Character_Creation:

    def __init__(self, screen, clock):

        # Scene varibles
        self.scene_name = "Character Creation"

        # Pygame components
        self.clock = clock
        self.screen = screen
        self.event_list = None
        self.WIDTH, self.HEIGHT = self.screen.get_size()

        # Mouse Handler
        self.mouse_handler = MouseHandler()

        # UI Handler
        self.ui_handler = UIElements.UI_Handler()

        # Debugger
        self.debugger = Debugger.Debugger(self.ui_handler)

        # Character creation panel
        self.character_creation_panel = None # Will be created at scene preparation


    ################################ SCENE CLEANUP ################################
    def destroy_creation_panel(self):

        self.character_creation_panel.delete_creation_menu()
    
    def cleanup_scene(self):

        # Log message
        Debugger.Log_Manager.add_to_log_file("Scene cleanup has been started: Scene - " + self.scene_name)

        # Creation panel
        self.destroy_creation_panel()

        # Log message
        Debugger.Log_Manager.add_to_log_file("Scene cleanup complete")


    ################################ SCENE PREPARATION ################################
    def create_new_creation_panel(self):

        self.character_creation_panel = None
        self.character_creation_panel = UIAlternatives.StatPickerMenu(self.ui_handler, (720, 180), PlayerRace._AVALIBLE_RACES, PlayerClass._AVALIBLE_CLASSES)

    def prepare_scene(self):

        # Log message
        Debugger.Log_Manager.add_to_log_file("Scene preparation has been started: Scene - " + self.scene_name)

        # Creation panel
        self.create_new_creation_panel()

        # Log message
        Debugger.Log_Manager.add_to_log_file("Scene preparation complete")


    ################################ SCENE FUNCTIONS ################################
    def quit_game(self):

        # Log message
        Debugger.Log_Manager.add_to_log_file("Quiting the game.")

        pg.quit()
        sys.exit()

    def events(self):

        # Update the eventlist
        self.event_list = pg.event.get()

        # Check events
        for event in self.event_list:
            if event.type == pg.QUIT:
                
                self.quit_game()

    def update(self):
        
        if self.event_list != None:

            # Update Mouse Handler
            self.mouse_handler.update(self.event_list, None)

            # Update UI Handler
            self.ui_handler.update(self.event_list)

    def draw(self):

        # Fill the screen with black
        self.screen.fill((0, 0, 0))

        # Draw UI Components
        self.ui_handler.draw_ui(self.screen)

        # Debugger
        self.debugger.draw(self.clock)

        # Draw Mouse Handler
        self.mouse_handler.draw(self.screen)

        # Always at the bottom
        pg.display.flip()
