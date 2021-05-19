import os
import pygame as pg


class Tilemap:


    def __init__(self, pos, tile_size, images,  size = None, matrix = None):

        self.pos = pos
        self.rect = None
        self.tile_images = images
        self.tile_size = tile_size
        self.tilemap_size = size
        
        self.tiles = []

        if matrix is None and size is not None:
            self.create_tilemap()
        elif matrix is not None:
            self.create_tilemap_from_matrix(matrix)
        else:
            print("Error no matrix and tile map size given!")
        
        self.set_tile_neighbours()

    def draw_tiles(self, surface):

        for tile in self.tiles:

            tile.draw_self(surface)

    def create_tilemap(self):

        for y in range(self.tilemap_size[1]):
            for x in range(self.tilemap_size[0]):

                t = Grid((self.pos[0] + (self.tile_size * x), self.pos[1] + (self.tile_size * y)), (x, y), self.tile_images[0])
                self.tiles.append(t)

    def create_tilemap_from_matrix(self, filepath):

        matrix_file = open(filepath, 'r')

        matrix = matrix_file.read()
        matrix = eval(matrix)

        self.tilemap_size = (len(matrix[0]), len(matrix))

        for y in range(len(matrix)):
            for x in range(len(matrix[0])):

                if matrix[y][x] == 0:

                    t = Grid((self.pos[0] + (self.tile_size * x), self.pos[1] + (self.tile_size * y)), (x, y), self.tile_images[matrix[y][x]])
                    self.tiles.append(t)
                if matrix[y][x] == 1:

                    t = Grid((self.pos[0] + (self.tile_size * x), self.pos[1] + (self.tile_size * y)), (x, y), self.tile_images[matrix[y][x]])
                    t.obstacle = True
                    self.tiles.append(t)
        
        self.rect = pg.Rect(self.pos, (len(matrix[0]) * self.tile_size, len(matrix) * self.tile_size))

    def set_tile_neighbours(self):

        if len(self.tiles) > 0:
            for tile in self.tiles:

                neighbour_tiles = []
                current_tile_pos = [tile.tilemap_pos[0], tile.tilemap_pos[1]]

                for n_tile in self.tiles:

                    if   (current_tile_pos[0] - 1, current_tile_pos[1] - 1) == n_tile.tilemap_pos:
                        neighbour_tiles.append(n_tile)
                    elif (current_tile_pos[0] + 0, current_tile_pos[1] - 1) == n_tile.tilemap_pos:
                        neighbour_tiles.append(n_tile)
                    elif (current_tile_pos[0] + 1, current_tile_pos[1] - 1) == n_tile.tilemap_pos:
                        neighbour_tiles.append(n_tile)
                    
                    elif (current_tile_pos[0] - 1, current_tile_pos[1] + 0) == n_tile.tilemap_pos:
                        neighbour_tiles.append(n_tile)
                    elif (current_tile_pos[0] + 0, current_tile_pos[1] + 0) == n_tile.tilemap_pos:
                        continue
                    elif (current_tile_pos[0] + 1, current_tile_pos[1] + 0) == n_tile.tilemap_pos:
                        neighbour_tiles.append(n_tile)
                    
                    elif (current_tile_pos[0] - 1, current_tile_pos[1] + 1) == n_tile.tilemap_pos:
                        neighbour_tiles.append(n_tile)
                    elif (current_tile_pos[0] + 0, current_tile_pos[1] + 1) == n_tile.tilemap_pos:
                        neighbour_tiles.append(n_tile)
                    elif (current_tile_pos[0] + 1, current_tile_pos[1] + 1) == n_tile.tilemap_pos:
                        neighbour_tiles.append(n_tile)
                
                tile.neighbour_tiles = neighbour_tiles


class Grid:

    def __init__(self, pos, tilemap_pos, image):

        self.image = pg.image.load(image)
        self.rect = pg.Rect(pos, (self.image.get_width(), self.image.get_height()))
        self.tilemap_pos = tilemap_pos
        self.neighbour_tiles = []
        
        self.obstacle = False
        self.occupier = None

        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = 0
        self.parent_tile = None
    
    def reset_tile_costs(self):

        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = 0
        self.parent_tile = None

    def draw_self(self, surface):

        surface.blit(self.image, self.rect)