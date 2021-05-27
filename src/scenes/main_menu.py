# import internal modules
from src.engine.game_manager import Game_Manager
import src.engine.scene_manager as SceneManager
from src.engine.mouse_handler import MouseHandler
import src.engine.ui.ui_elements as UIElements
import src.engine.ui.ui_alternative as UIAlternatives
import src.engine.debugger as Debugger
import src.engine.timer as Time
from src.engine.pathfinding import A_Star
from src.engine.tilemap import Tilemap
from src.player.player import Player
# import external modules
import sys
import pygame as pg


class Main_Menu:

    def __init__(self, screen, clock):
        
        # Scene varibles
        self.scene_name = "Main Menu"

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

        # Main menu background
        self.main_menu_background = UIElements.Canvas(self.ui_handler, (0,0), [], True, image='assets/ui/main_menu_background.png')

        ######################## Enterence ########################
        # Labels
        self.game_title = UIElements.Label(self.ui_handler, (480, 120), "Unnamed Rogue-Like")

        # Buttons
        self.start_button = UIElements.Button(self.ui_handler, (520, 290), lambda: (self.enterence_canvas.change_visiblity(), self.save_load_canvas.change_visiblity()), text="Start")
        self.options_button = UIElements.Button(self.ui_handler, (520, 360), lambda: print("To be added..."), text="Options")
        self.quit_button = UIElements.Button(self.ui_handler, (520, 430), self.quit_game, text="Quit")

        # Canvas
        self.enterence_canvas = UIElements.Canvas(self.ui_handler, (0, 0), [self.game_title, self.start_button, self.options_button, self.quit_button], True)

        ######################## Save-load ########################
        # Save Slots
        self.save_slot_1 = UIAlternatives.SaveSlot(self.ui_handler, (450, 60), 1)
        self.save_slot_2 = UIAlternatives.SaveSlot(self.ui_handler, (450, 230), 2)
        self.save_slot_3 = UIAlternatives.SaveSlot(self.ui_handler, (450, 400), 3)

        # Buttons
        self.save_load_back_button = UIElements.Button(self.ui_handler, (520, 580), lambda: (self.enterence_canvas.change_visiblity(), self.save_load_canvas.change_visiblity()), text="Back")

        # Canvas
        self.save_load_canvas = UIElements.Canvas(self.ui_handler, (0, 0), [self.save_slot_1, self.save_slot_2, self.save_slot_3, self.save_load_back_button])

        ######################## Character-Creation ########################

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
                pg.quit()
                sys.exit()

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
