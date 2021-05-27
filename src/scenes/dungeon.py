# import internal modules
from src.engine.game_manager import Game_Manager
from src.engine.mouse_handler import MouseHandler
import src.engine.ui.ui_elements as UIElements
import src.engine.debugger as Debugger
import src.engine.timer as Time
from src.engine.pathfinding import A_Star
from src.engine.tilemap import Tilemap
from src.player.player import Player
# import external modules
import sys
import os
import pygame as pg


class Dungeon:

    def __init__(self, screen, clock, timer_handler):
        
        # Scene varibles
        self.scene_name = "Dungeon"

        # Pygame components
        self.clock = clock
        self.screen = screen
        self.event_list = None
        self.WIDTH, self.HEIGHT = self.screen.get_size()

        # Timer Handler
        self.timer_handler = timer_handler

        # A* Pathfinder
        self.pathfinder = A_Star()

        # Set player
        self.player = Player((250, 100), None)

        # Mouse Handler
        self.mouse_handler = MouseHandler(self.pathfinder, self.player)

        # UI Handler
        self.ui_handler = UIElements.UI_Handler()

        # Debugger
        self.debugger = Debugger.Debugger(self.ui_handler)

        # Tilemap
        self.current_tilemap = Tilemap((50, 50), 50, ["assets/tileset/tile.png", "assets/tileset/wall.png"], matrix= "map")

        for tile in self.current_tilemap.tiles:

            if tile.rect.y == self.player.rect.y:
                if tile.rect.x == self.player.rect.x:

                    self.player.current_tile = tile

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

            # Update Timer Handler
            self.timer_handler.update()

            # Update Mouse Handler
            self.mouse_handler.update(self.event_list, self.current_tilemap)

            # Update UI Handler
            self.ui_handler.update(self.event_list)

            # Update player
            self.player.update()

    def draw(self):

        # Fill the screen with black
        self.screen.fill((0, 0, 0))

        # Draw the current tilemap
        self.current_tilemap.draw_tiles(self.screen)

        # Draw player
        self.player.draw_self(self.screen)

        # Draw UI Components
        self.ui_handler.draw_ui(self.screen)

        # Draw Debugger
        self.debugger.draw(self.clock)

        # Draw Mouse Handler
        self.mouse_handler.draw(self.screen)

        # Always at the bottom
        pg.display.flip()