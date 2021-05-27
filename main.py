# import internal modules
from src.game import Game
# import external modules
import pygame as pg


def main():

    running = True

    pg.init()
    WIDTH, HEIGHT = 1280, 720
    SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Rogue-like Game")
    clock = pg.time.Clock()

    game = Game(SCREEN, clock)

    while running:

        game.run()


if __name__ == "__main__":

    main()