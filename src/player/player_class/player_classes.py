import src.engine.ui.ui_elements as UIElements
from src.engine.ui.ui_alternative import FightingStylePicker

import src.player.fighting_styles as FightingStyles

import pygame as pg

class Fighter:

    CLASS_NAME              = "Fighter"
    CLASS_PLAYER_IMAGE      = "assets/entities/player_fighter.png"
    CLASS_BANNER_IMAGE      = "assets/ui/special/character_creation/player_fighter_banner.png"

    def __init__(self, player):

        # Owner reference
        self.player = player

        # Base class stats
        self.player.player_class       = Fighter
        self.player.level              = 1
        self.player.hit_dice           = 10
        self.player.image              = pg.image.load(Fighter.CLASS_PLAYER_IMAGE)
        self.sub_class                 = None

        # Fighter class params
        self.fighting_styles = []

    def _level_up_char_01(self, ui_handler, canvas):

        fighting_style_picker = FightingStylePicker(ui_handler, (250, 100), FightingStyles._AVALIBLE_FIGHTING_STYLES, button_margin=10)

        back_button = UIElements.Button(ui_handler, (250, 200), lambda: ("ERROR"), text="Back")

        proceed_button = UIElements.Button(ui_handler, (250, 300), lambda: ("ERROR"), text="Create Character")

        level_01_canvas = UIElements.Canvas(ui_handler, (0,0), [fighting_style_picker, back_button, proceed_button], visible=True)

        back_button.on_click_event = lambda: (level_01_canvas.destroy_canvas(), canvas.change_visiblity())


class Wizard:

    CLASS_NAME              = "Wizard"
    CLASS_PLAYER_IMAGE      = "assets/entities/player_wizard.png"
    CLASS_BANNER_IMAGE      = "assets/ui/special/character_creation/player_wizard_banner.png"

    def __init__(self, player):

        # Owner reference
        self.player = player

        # Base class stats
        self.player.player_class       = Wizard
        self.player.level              = 1
        self.player.hit_dice           = 6
        self.player.image              = pg.image.load(Wizard.CLASS_PLAYER_IMAGE)
        self.subclass                  = None


_AVALIBLE_CLASSES = [

    Fighter,
    Wizard
]
