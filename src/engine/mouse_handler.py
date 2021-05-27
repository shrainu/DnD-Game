from src.engine.timer import Timer
import pygame as pg


class MouseHandler:

    DEFAULT_CURSOR = 'assets/ui/cursor.png'

    TILE_HIGHLIGHT = 'assets/ui/tile_highlight.png'
    TILE_HIGHLIGHT_ALERT = 'assets/ui/tile_highlight_alert.png'
    TILE_HIGHLIGHT_SUCCESS = 'assets/ui/tile_highlight_success.png'
    TILE_HIGHLIGHT_IMAGE = pg.image.load(TILE_HIGHLIGHT)

    def __init__(self, pathfinder = None, player = None):

        pg.mouse.set_visible(False)

        self.cursor_image = pg.image.load(MouseHandler.DEFAULT_CURSOR)
        self.rect = pg.Rect((0, 0), (self.cursor_image.get_width(), self.cursor_image.get_height()))

        self.mouse_in_window = True

        self.pathfinder = pathfinder
        self.player_ref = player

        self.over_ui = False

        self.over_tilemap = False
        self.hovered_tile_pos = None
    
    def draw(self, surface):

        if self.mouse_in_window:

            self.draw_tile_highlight(surface)
            self.draw_cursor(surface)

    def draw_cursor(self, surface):

        surface.blit(self.cursor_image, self.rect)
    
    def draw_tile_highlight(self, surface):

        if self.over_tilemap and not self.over_ui:

            surface.blit(MouseHandler.TILE_HIGHLIGHT_IMAGE, self.hovered_tile_pos)

    def set_default_tile_highlight(self):

        MouseHandler.TILE_HIGHLIGHT_IMAGE = pg.image.load(MouseHandler.TILE_HIGHLIGHT)

    def update_tile_highlight(self, mouse_pos, current_tilemap):

        if current_tilemap.rect.y < mouse_pos[1] < current_tilemap.rect.y + current_tilemap.rect.height:
            if current_tilemap.rect.x < mouse_pos[0] < current_tilemap.rect.x + current_tilemap.rect.width:

                self.over_tilemap = True
            else:

                self.over_tilemap = False
        else:
            self.over_tilemap = False

        if self.over_tilemap and not self.over_ui:

            for tile in current_tilemap.tiles:

                if tile.rect.y < mouse_pos[1] < tile.rect.y + tile.rect.height:
                    if tile.rect.x < mouse_pos[0] < tile.rect.x + tile.rect.width:

                        self.hovered_tile_pos = (tile.rect.x, tile.rect.y)

    def update_cursor_pos(self, mouse_pos):

        self.rect.x, self.rect.y = mouse_pos
        
    def detect_mouse_in_window(self):

        if pg.mouse.get_focused() == 0:

            self.mouse_in_window = False
        else:

            self.mouse_in_window = True

    def handle_mouse_events(self, event_list, current_tilemap):

        mouse_pos = pg.mouse.get_pos()

        # Update cursors
        self.update_cursor_pos(mouse_pos)
        if current_tilemap is not None:
            self.update_tile_highlight(mouse_pos, current_tilemap)

        for event in event_list:

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.over_ui:

                    x, y = event.pos

                    if current_tilemap is not None:
                        for tile in current_tilemap.tiles:

                            if tile.rect.y < y < tile.rect.y + tile.rect.height:
                                if tile.rect.x < x < tile.rect.x + tile.rect.width:
                                    
                                    if self.player_ref.my_turn and self.player_ref.movement_left > 0 and tile.occupier is None and not tile.obstacle:

                                        path = self.pathfinder.find_path(self.player_ref.current_tile, tile)

                                        self.player_ref.set_path(path)

                                        MouseHandler.TILE_HIGHLIGHT_IMAGE = pg.image.load(MouseHandler.TILE_HIGHLIGHT_SUCCESS)
                                        Timer(0.25, False, self.set_default_tile_highlight)

                                    elif self.player_ref.my_turn and self.player_ref.movement_left > 0 and (tile.occupier is not None or tile.obstacle):

                                        MouseHandler.TILE_HIGHLIGHT_IMAGE = pg.image.load(MouseHandler.TILE_HIGHLIGHT_ALERT)
                                        Timer(0.25, False, self.set_default_tile_highlight)

    def update(self, event_list, current_tilemap):

        self.detect_mouse_in_window()
        
        if self.mouse_in_window:

            self.handle_mouse_events(event_list, current_tilemap)


