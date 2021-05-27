import src.player.player as Player
import src.engine.debugger as Debugger
import src.player.player_race.player_races as PlayerRaces
import src.player.player_class.player_classes as PlayerClass
import src.engine.scene_manager as SceneManager
from src.engine.game_manager import Game_Manager
import src.engine.ui.ui_elements as UIElements

import dotenv
import pygame as pg
import os


# STAT PICKER MENU ---------------------------------------------------
class StatPickerMenu:

    # This is necessary for character creation screen

    def __init__(self, ui_handler, pos, race_list, class_list, y_margin=50, x_margin=160):

        # Self variables
        self.ui_handler         = ui_handler
        self.pos                = pos
        self.y_margin           = y_margin
        self.x_margin           = x_margin
        self.points             = 27
        self.points_label_text  = "Points Remaining: "
        self.points_label_numb  = str(self.points)
        self.race_list          = race_list
        self.class_list         = class_list

        # Set childrens
        self.player = None
        # Character creation menu background
        self.creation_menu_background   = UIElements.Canvas(ui_handler, (0,0), [], True, image='assets/ui/main_menu_background.png')
        # Set labels
        self.points_label   = UIElements.ImageLabel(ui_handler, self.pos, (self.points_label_text + self.points_label_numb), image='assets/ui/special/character_creation/label_background_point_label.png')
        self.race_label     = UIElements.ImageLabel(ui_handler, (self.pos[0], self.pos[1] - (self.y_margin * 2)), "Race", size="short")
        self.class_label    = UIElements.ImageLabel(ui_handler, (self.pos[0], self.pos[1] - (self.y_margin * 1)), "Class", size="short")
        # Set pickers
        self.race_picker    = RacePicker(ui_handler, self, (self.pos[0] + (self.x_margin * 1 + 20), self.pos[1] - (self.y_margin * 2)), self.race_list, button_margin = 5)
        self.class_picker   = ClassPicker(ui_handler, self, (self.pos[0] + (self.x_margin * 1 + 20), self.pos[1] - (self.y_margin * 1)), self.class_list, button_margin = 5)
        # Stat labels
        self.stat_labels    = []
        # Stat pickers
        self.pickers        = []
        # Input Fields
        self.name_label     = UIElements.ImageLabel(ui_handler, (self.pos[0] + (((-self.x_margin) * 4) + 60), self.pos[1] + (self.y_margin * 7.5)), "Name")
        self.name_field     = UIElements.InputField(ui_handler, (self.pos[0] + ((-self.x_margin) * 4), self.pos[1] + (self.y_margin * 8.5)), size="long", text="Nameless Hero")
        # Buttons
        self.create_button  = UIElements.Button(ui_handler, (self.pos[0] + (225), self.pos[1] + (self.y_margin * 8)), self.create_character, text="Next")
        self.back_button    = UIElements.Button(ui_handler, (self.pos[0] + (self.x_margin * 0), self.pos[1] + (self.y_margin * 8)), lambda: SceneManager.Scene_Manager.change_scene(SceneManager.Scenes.main_menu), size="short", text="Back")
        # Character Image
        self.character_image = UIElements.Canvas(ui_handler, (self.pos[0] + ((-self.x_margin) * 3.80), self.pos[1] - 30), [], visible=True, size=None, image=self.class_picker.return_label().CLASS_BANNER_IMAGE)
        # Setup the children list for canvas
        self.children_list = [
            self.creation_menu_background,
            self.points_label,
            self.race_label,
            self.class_label,
            self.race_picker,
            self.class_picker,
            self.name_label,
            self.name_field,
            self.create_button,
            self.back_button,
            self.character_image
            ]
        # Set stat labels and add them to children list
        self.set_labels(ui_handler)
        # Set stat pickers and add them to children list
        self.set_pickers(ui_handler)
        # Setup the canvas
        self.character_creation_canvas = UIElements.Canvas(ui_handler, (0, 0), self.children_list, visible=True)
        # Update stat picker bonuses
        self.update_picker_bonus()

    def create_character(self):

        # If this function doesn't work properly try to use a while loop when changing visibility

        self.player = Player.Player((-50, -50), None)

        self.player.player_class = self.class_picker.return_label()(self.player)
        self.player.player_race  = self.race_picker.return_label()(self.player)
        
        self.player.stat_str += self.pickers[0].return_label()
        self.player.stat_dex += self.pickers[1].return_label()
        self.player.stat_con += self.pickers[2].return_label()
        self.player.stat_int += self.pickers[3].return_label()
        self.player.stat_wis += self.pickers[4].return_label()
        self.player.stat_cha += self.pickers[5].return_label()

        self.character_creation_canvas.change_visiblity(False)

        self.player.player_class._level_up_char_01(self.ui_handler, self.character_creation_canvas)

    def delete_creation_menu(self):

        self.character_creation_canvas.destroy_canvas()

    # Set the stat pickers
    def set_pickers(self, ui_handler):

        for i in range(6):

            t = StatPicker(ui_handler, self, (self.pos[0] + (self.x_margin * 1 + 20), self.pos[1] + (self.y_margin * (i + 1))), button_margin=5)
            self.children_list.append(t)
            self.pickers.append(t)

    def set_labels(self, ui_handler):

        text_list = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]

        for i in range(6):

            t = UIElements.ImageLabel(ui_handler, (self.pos[0], self.pos[1] + (self.y_margin * (i + 1))), text_list[i], size="short")
            self.children_list.append(t)
            self.stat_labels.append(t)

    # Update pickers bonuses
    def update_picker_bonus(self):

        # Set all the pickers bonuses to zero
        for picker in self.pickers:

            picker.racial_bonus = 0

    # Update the points label
    def update_points_label(self):

        self.points_label_numb = str(self.points)
        self.points_label.label.text = (self.points_label_text + self.points_label_numb)


# RACE PICKER --------------------------------------------------------
class RacePicker(UIElements.TextPicker):

    # Almost the same with Text Picker just calls a function when the text is changed

    def __init__(self, ui_handler, parent, pos, race_list, size="medium", left_button_text="<", right_button_text=">", button_margin=0):

        # initalizze parent
        super().__init__(ui_handler, pos, text_list=[""], size=size, left_button_text=left_button_text, right_button_text=right_button_text, button_margin=button_margin)

        # initialize self
        self.parent = parent
        self.race_list = race_list

        self.update_label()

    # Get the previous text
    def next_label(self):

        self.counter += 1

        if self.counter == len(self.race_list):
            self.counter = 0
        
        # Update the pickers racial bonuses
        self.parent.update_picker_bonus()

        self.update_label()

    # Get the previous text
    def past_label(self):

        self.counter -= 1

        if self.counter == -1:
            self.counter = len(self.race_list) - 1

        # Update the pickers racial bonuses
        self.parent.update_picker_bonus()

        self.update_label() 

    def return_label(self):
        
        return self.race_list[self.counter]

    def update_label(self):

        self.label.text = self.race_list[self.counter].RACE_NAME

        super().set_label_position()


# RACE PICKER --------------------------------------------------------
class ClassPicker(RacePicker):

    def __init__(self, ui_handler, parent, pos, class_list, size="medium", left_button_text="<", right_button_text=">", button_margin=0):

        # Initialize self
        self.parent = parent
        self.class_list = class_list

        # Initialize parent       
        super().__init__(ui_handler, parent, pos, class_list, size, left_button_text, right_button_text, button_margin)

    # Get the previous text
    def next_label(self):

        self.counter += 1

        if self.counter == len(self.class_list):
            self.counter = 0

        # Change character image shown
        self.parent.character_image.image = pg.image.load(self.return_label().CLASS_BANNER_IMAGE)

        self.update_label()

    # Get the previous text
    def past_label(self):

        self.counter -= 1

        if self.counter == -1:
            self.counter = len(self.class_list) - 1

        # Change character image shown
        self.parent.character_image.image = pg.image.load(self.return_label().CLASS_BANNER_IMAGE)

        self.update_label()

    def return_label(self):
        
        return self.class_list[self.counter] 

    def update_label(self):

        self.label.text = self.class_list[self.counter].CLASS_NAME

        super().set_label_position()


# STAT PICKER --------------------------------------------------------
class StatPicker(UIElements.TextPicker):

    # An alternative to text picker in order to use to pick stats while creating characters

    def __init__(self, ui_handler, parent, pos, size="medium", left_button_text="-", right_button_text="+", button_margin=0):

        # Initialize parent class
        super().__init__(ui_handler, pos, text_list=[""], size=size, left_button_text=left_button_text, right_button_text=right_button_text, button_margin=button_margin)

        # Initialze self component
        self.stat_counter = 8
        self.racial_bonus = 0
        self.parent = parent

        # Initialize childrens
        # Initialize Label
        self.label.text = str(self.stat_counter + self.racial_bonus)
        # Initialize buttons
        self.left_button.on_click_event = self.past_label
        self.right_button.on_click_event = self.next_label

        self.update_label()

    # Get the previous text
    def past_label(self):

        if self.stat_counter > 13:

            self.stat_counter -= 1
            self.parent.points += 2
        else:

            if self.stat_counter > 8:

                self.stat_counter -= 1
                self.parent.points += 1

        self.update_label()
        self.parent.update_points_label()

    # Get the next text
    def next_label(self):

        if self.parent.points < 1:
            return
        
        if self.stat_counter >= 13:

            if self.stat_counter < 16:
                self.stat_counter += 1
                self.parent.points -= 2
        else:

            self.stat_counter += 1
            self.parent.points -= 1

        self.update_label()
        self.parent.update_points_label()

    # Return the value currently shown in the picker
    def return_label(self):

        return (self.stat_counter)

    # Update the text label to show new text
    def update_label(self):

        self.label.text = str(self.stat_counter + self.racial_bonus)

        self.set_label_position()


# SAVE SLOT ----------------------------------------------------------
class SaveSlot(UIElements.Button):

    SAVE_SLOT_USED_IMAGE = 'assets/ui/save_slot_used.png'
    SAVE_SLOT_EMPTY_IMAGE = 'assets/ui/save_slot_na.png'

    _SAVE_SLOT_FONT = pg.font.Font('fonts/Alkhemikal.ttf', 32)

    def __init__(self, ui_handler, pos, save_slot_number):

        super().__init__(ui_handler, pos, on_click_event = self.load_selected_character, size = "medium", image=SaveSlot.SAVE_SLOT_EMPTY_IMAGE, text="")

        # Initialize self
        self.visible = True
        self.used = False
        self.save_slot_number = save_slot_number

        # Initialize labels
        self.name_label     = UIElements.Label(ui_handler, (self.rect.x + 135, self.rect.y + (30 * 0) + (4 * 0) + 14), "Name", SaveSlot._SAVE_SLOT_FONT)
        self.class_label    = UIElements.Label(ui_handler, (self.rect.x + 135, self.rect.y + (30 * 1) + (4 * 1) + 14), "Class", SaveSlot._SAVE_SLOT_FONT)
        self.health_label   = UIElements.Label(ui_handler, (self.rect.x + 135, self.rect.y + (30 * 2) + (4 * 2) + 14), "Health", SaveSlot._SAVE_SLOT_FONT)
        self.level_label    = UIElements.Label(ui_handler, (self.rect.x + 135, self.rect.y + (30 * 3) + (4 * 3) + 14), "Level", SaveSlot._SAVE_SLOT_FONT)

        # Load save file
        self.load_character_info()

    def load_selected_character(self):

        if self.used:

            os.environ['PATH_TO_CURRENT_CHARACTER'] = os.getenv('PATH_TO_SAVES') + "/saves/save_slot_" + str(self.save_slot_number)

            dotenv.set_key(Game_Manager.env_file, 'PATH_TO_CURRENT_CHARACTER', os.environ['PATH_TO_CURRENT_CHARACTER'])

            # Log message
            Debugger.Log_Manager.add_to_log_file("PATH TO CURRENT CHARACTER is set to: " + os.getenv('PATH_TO_CURRENT_CHARACTER'))

            SceneManager.Scene_Manager.scenes[SceneManager.Scenes.dungeon.value].player.load_character(os.getenv('PATH_TO_CURRENT_CHARACTER') + "/player")

            SceneManager.Scene_Manager.change_scene(SceneManager.Scenes.hub)
        else:

            os.environ['PATH_TO_CURRENT_CHARACTER'] = os.getenv('PATH_TO_SAVES') + "/saves/save_slot_" + str(self.save_slot_number)

            dotenv.set_key(Game_Manager.env_file, 'PATH_TO_CURRENT_CHARACTER', os.environ['PATH_TO_CURRENT_CHARACTER'])

            # Log message
            Debugger.Log_Manager.add_to_log_file("PATH TO CURRENT CHARACTER is set to: " + os.getenv('PATH_TO_CURRENT_CHARACTER'))

            SceneManager.Scene_Manager.change_scene(SceneManager.Scenes.character_creation)

    def change_visiblity(self, value = None):

        if value is not None:

            self.visible = value
        else:
            
            self.visible = not self.visible

        self.name_label.change_visiblity(self.visible)
        self.class_label.change_visiblity(self.visible)
        self.health_label.change_visiblity(self.visible)
        self.level_label.change_visiblity(self.visible)

    def load_character_info(self):

        path_to_saves = os.getenv('PATH_TO_SAVES') + "/saves/save_slot_" + str(self.save_slot_number)

        if len(os.listdir(path_to_saves)) < 1:

            self.image = pg.image.load(SaveSlot.SAVE_SLOT_EMPTY_IMAGE)
            
            self.name_label.text    = ""
            self.class_label.text   = ""
            self.health_label.text  = ""
            self.level_label.text   = ""
            return
        else:

            self.used = True
            self.image = pg.image.load(SaveSlot.SAVE_SLOT_USED_IMAGE)

        with open(path_to_saves + "/player", 'r') as save_file:

            player_data = save_file.readlines()

            for line in player_data:

                if line.startswith("player_name = "):

                    self.name_label.text = line[len("player_name = "):-1]
                elif line.startswith("player_class   = "):

                    temp =  eval(line[len("player_class   = "):-1])

                    self.class_label.text = temp.CLASS_NAME
                elif line.startswith("current_heath  = "):

                    self.health_label.text = line[len("current_heath  = "):-1]
                elif line.startswith("level          = "):

                    self.level_label.text = line[len("level          = "):-1]
        
        

class FightingStylePicker(UIElements.TextPicker):

        # Almost the same with Text Picker just calls a function when the text is changed

    def __init__(self, ui_handler, pos, fighting_style_list, size="medium", left_button_text="<", right_button_text=">", button_margin=0):

        # initalizze parent
        super().__init__(ui_handler, pos, text_list=[""], size=size, left_button_text=left_button_text, right_button_text=right_button_text, button_margin=button_margin)

        # initialize self
        self.fighting_style_list = fighting_style_list

        self.update_label()

    # Get the previous text
    def next_label(self):

        self.counter += 1

        if self.counter == len(self.fighting_style_list):
            self.counter = 0

        self.update_label()

    # Get the previous text
    def past_label(self):

        self.counter -= 1

        if self.counter == -1:
            self.counter = len(self.fighting_style_list) - 1

        self.update_label() 

    def return_label(self):
        
        return self.fighting_style_list[self.counter]

    def update_label(self):

        self.label.text = self.fighting_style_list[self.counter]._FS_NAME

        super().set_label_position()

