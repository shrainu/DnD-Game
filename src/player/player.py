from src.engine.timer import Timer
import src.engine.debugger as Debugger
import pygame as pg


class Player:

    PLAYER_SPRITE = "assets/entities/player_fighter.png"

    def __init__(self, pos, current_tile):

        self.rect = pg.Rect(pos, (50, 50))
        self.image = pg.image.load(Player.PLAYER_SPRITE)

        self.my_turn = True
    
        self.path = []
        self.current_tile = current_tile
        self.movement_left = 5
        self.movement_timer = None
        self.moving = False
    
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
    


