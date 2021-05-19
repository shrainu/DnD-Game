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
from src.scenes.dungeon import Dungeon
# import external modules
import sys
import pygame as pg


class Game:

    def __init__(self, screen, clock):

        # Pygame components
        self.clock = clock
        self.screen = screen
        self.event_list = None
        self.WIDTH, self.HEIGHT = self.screen.get_size()

        # Game variables
        # Set the Scene Manager variables
        # To determine which scene is currently active
        self.current_scene = SceneManager.Scene_Manager.get_current_scene()
        # To make it easier to switch scenes
        SceneManager.Scene_Manager.game_instance = self

        # Log Manager
        self.log_manager = Debugger.Log_Manager()

        # Game manager
        # Initialize the game only called once per user
        Game_Manager.initialize_game()

        # Timer Handler
        self.timer_handler = Time.Timer_Handler()
        Time.Timer.timer_handler = self.timer_handler

        # Scenes
        # Main Menu scene
        self.main_menu_scene = Main_Menu(self.screen, self.clock)

        # Dungeon Scene
        self.dungeon_scene = Dungeon(self.screen, self.clock, self.timer_handler)

    def run(self):

        self.playing = True

        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def events(self):

        # Events function of main menu scene
        if self.current_scene == SceneManager.Scenes.main_menu:

            self.main_menu_scene.events()
        # Events function of dungeon scene
        elif self.current_scene == SceneManager.Scenes.dungeon:

            self.dungeon_scene.events()

    def update(self):
        
        # Update function of main menu scene
        if self.current_scene == SceneManager.Scenes.main_menu:

            self.main_menu_scene.update()
        # Update function of dungeon scene
        elif self.current_scene == SceneManager.Scenes.dungeon:

            self.dungeon_scene.update()

    def draw(self):

        # Draw function of main menu scene
        if self.current_scene == SceneManager.Scenes.main_menu:

            self.main_menu_scene.draw()
        # Draw function of dungeon scene
        elif self.current_scene == SceneManager.Scenes.dungeon:

            self.dungeon_scene.draw()