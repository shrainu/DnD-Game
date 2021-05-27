# Mechanic related imports
from src.engine.timer import Timer
import src.engine.debugger as Debugger
# System related imports
from src.player.player_entity import PlayerEntity
import src.player.player_class.player_classes as PlayerClass
import src.player.player_race.player_races as PlayerRace
# External imports
import pygame as pg


class Player(PlayerEntity):

    PLAYER_SPRITE = "assets/entities/player_fighter.png"

    def __init__(self, pos, current_tile):

        # Mechanic related variables -----------------------------------------
        self.rect   = pg.Rect(pos, (50, 50))
        self.image  = pg.image.load(Player.PLAYER_SPRITE)

        self.my_turn = True
    
        self.path           = []
        self.current_tile   = current_tile
        self.movement_left  = 5
        self.movement_timer = None
        self.moving         = False

        # System related variables -------------------------------------------

        # Initialize parent system class
        super().__init__()

        self.player_class_handler = None
        self.player_race_handler  = None
    
    '''################################ GAME PLAY RELATED FUNCTIONS ################################'''

    def draw_self(self, surface):

        surface.blit(self.image, self.rect)

    def move_to_tile(self, tile):

        self.rect.x, self.rect.y = tile.rect.x, tile.rect.y

        self.current_tile.occupier = None
        self.current_tile = tile
        self.current_tile.occupier = self

        self.moving = False

        # Log message
        Debugger.Log_Manager.add_to_log_file("Player has moved to tile: " + str(self.current_tile.tilemap_pos))

    def move(self):

        if self.moving == False:

            next_tile = self.path.pop(0)

            self.movement_timer = Timer(0.25, False, lambda: self.move_to_tile(next_tile))

            self.moving = True

    def set_path(self, path):

        # Log message
        Debugger.Log_Manager.add_to_log_file("A new path for the player has been created")

        if self.path == [] and path != None:

            self.path = path

    def update(self):

        if self.my_turn and self.movement_left > 0  and len(self.path) > 0:

            self.move()

    '''################################ SYSTEM RELATED FUNCTIONS ###################################'''

    '''################################ SAVE LOAD RELATED FUNCTIONS ################################'''

    def load_character(self, filepath):

        # Log message
        Debugger.Log_Manager.add_to_log_file("Loading player character's data from save file.")

        # Load character stats from file
        with open(filepath, 'r') as save_file:

            save_data = save_file.readlines()

            for line in save_data:

                # Initialize name
                if line.startswith('player_name = '):

                    temp = line[len('player_name = '):-1]

                    self.player_name = temp
                # Initialize race
                elif line.startswith('player_race    = '):

                    temp = eval(line[len('player_race    = '):-1])

                    self.player_race = temp(self)
                # Initialize class
                elif line.startswith('player_class   = '):

                    temp = eval(line[len('player_class   = '):-1])

                    self.player_class = temp(self)
    


