# import internal modules
from src.engine.game_manager import Game_Manager
import src.engine.scene_manager as SceneManager
from src.engine.mouse_handler import MouseHandler
import src.engine.ui.ui_elements as UIElements
import src.engine.debugger as Debugger
import src.engine.timer as Time
from src.engine.pathfinding import A_Star
from src.engine.tilemap import Tilemap
from src.player.player import Player
# Import Scenes
from src.scenes.main_menu import Main_Menu
from src.scenes.character_creation import Character_Creation
from src.scenes.main_hub import Main_Hub
from src.scenes.dungeon import Dungeon
# import external modules
import pygame as pg


class Game:

    def __init__(self, screen, clock):

        # Pygame components
        self.clock = clock
        self.screen = screen
        self.event_list = None
        self.WIDTH, self.HEIGHT = self.screen.get_size()

        # Game variables
        Debugger.Debugger.debug_mode(True)

        # Log Manager
        self.log_manager = Debugger.Log_Manager()

        # Game manager
        # Initialize the game only called once per user
        Game_Manager.initialize_game()

        # Timer Handler
        self.timer_handler = Time.Timer_Handler()
        Time.Timer.timer_handler = self.timer_handler

        # Create Scenes
        # Main Menu scene
        self.main_menu_scene = Main_Menu(self.screen, self.clock)
        # Character Creation
        self.character_creation_scene = Character_Creation(self.screen, self.clock)
        # Hub Scene
        self.main_hub_scene = Main_Hub(self.screen, self.clock, self.timer_handler)
        # Dungeon Scene
        self.dungeon_scene = Dungeon(self.screen, self.clock, self.timer_handler)

        # Add all a reference of all the scenes to scene manager
        SceneManager.Scene_Manager.scenes.append(self.main_menu_scene)              # Scene number: 0
        SceneManager.Scene_Manager.scenes.append(self.character_creation_scene)     # Scene number: 1
        SceneManager.Scene_Manager.scenes.append(self.main_hub_scene)               # Scene number: 2
        SceneManager.Scene_Manager.scenes.append(self.dungeon_scene)                # Scene number: 3

    def run(self):

        self.playing = True

        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def events(self):

        # Call the events function of current scene
        SceneManager.Scene_Manager.events()

    def update(self):
        
        # Call the update function of current scene
        SceneManager.Scene_Manager.update()

    def draw(self):

        # Call the draw function of current scene
        SceneManager.Scene_Manager.draw()