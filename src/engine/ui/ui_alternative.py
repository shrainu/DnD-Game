from pygame.draw import line
from pygame.image import load
import src.player.player_race.player_races as PlayerRaces
import src.engine.ui.ui_elements as UIElements
import pygame as pg
import os


# STAT PICKER MENU ---------------------------------------------------
class StatPickerMenu:

    # This is necessary for character creation screen 

    def __init__(self, ui_handler, pos, y_margin=50, x_margin=160):

        # Self variables
        self.pos = pos
        self.y_margin = y_margin
        self.x_margin = x_margin
        self.points = 27
        self.points_label_text = "Points Remaining: "
        self.points_label_numb = str(self.points)

        # Set childrens
        # Set labels
        self.points_label = UIElements.Label(ui_handler, self.pos, (self.points_label_text + self.points_label_numb))
        self.race_label = UIElements.Label(ui_handler, (self.pos[0], self.pos[1] - (self.y_margin * 2)), "Race")
        self.class_label = UIElements.Label(ui_handler, (self.pos[0], self.pos[1] - (self.y_margin * 1)), "Class")
        # Stat labels
        self.str_label = UIElements.Label(ui_handler, (self.pos[0], self.pos[1] + (self.y_margin * 1)), "STR")
        self.dex_label = UIElements.Label(ui_handler, (self.pos[0], self.pos[1] + (self.y_margin * 2)), "DEX")
        self.con_label = UIElements.Label(ui_handler, (self.pos[0], self.pos[1] + (self.y_margin * 3)), "CON")
        self.int_label = UIElements.Label(ui_handler, (self.pos[0], self.pos[1] + (self.y_margin * 4)), "INT")
        self.wis_label = UIElements.Label(ui_handler, (self.pos[0], self.pos[1] + (self.y_margin * 5)), "WIS")
        self.cha_label = UIElements.Label(ui_handler, (self.pos[0], self.pos[1] + (self.y_margin * 6)), "CHA")
        # Set pickers
        self.race_picker = RacePicker(ui_handler, self, (680, 95), (180, 40), PlayerRaces.Race_RaceData.race_names_list, button_margin = 5)
        self.class_picker = UIElements.TextPicker(ui_handler, (680, 145), (180, 40), ["Wizard", "Cleric", "Figter"], button_margin = 5)
        # Stat pickers
        self.pickers = []
        self.set_pickers(ui_handler)
        # Update stat picker bonuses
        self.update_picker_bonus()
    
    # Set the stat pickers
    def set_pickers(self, ui_handler):

        for i in range(6):

            t = StatPicker(ui_handler, self, (self.pos[0] + (self.x_margin * 1), self.pos[1] + (self.y_margin * (i + 1))), (180, 40), button_margin=5)
            self.pickers.append(t)

    # Update pickers bonuses
    def update_picker_bonus(self):

        # Set all the pickers bonuses to zero
        for picker in self.pickers:

            picker.racial_bonus = 0
        
        # Check every race currently avalible
        for race in PlayerRaces.Race_RaceData.race_list:

            # if you find a match with what is currently showing in the self.race picker
            if race.race_name == self.race_picker.text_list[self.race_picker.counter]:

                # Set the bonus of all the pickers 
                for i in range(len(race.racial_stat_bonuses)):

                    self.pickers[i].racial_bonus = race.racial_stat_bonuses[i]
                    self.pickers[i].update_label()

    # Update the points label
    def update_points_label(self):

        self.points_label_numb = str(self.points)
        self.points_label.text = (self.points_label_text + self.points_label_numb)


# RACE PICKER --------------------------------------------------------
class RacePicker(UIElements.TextPicker):

    # Almost the same with Text Picker just calls a function when the text is changed

    def __init__(self, ui_handler, parent, pos, size, text_list, button_size=(40, 40), left_button_text="<", right_button_text=">", button_margin = 0):

        # initalizze parent
        super().__init__(ui_handler, pos, size, text_list, button_size=button_size, left_button_text=left_button_text, right_button_text=right_button_text, button_margin=button_margin)

        # initialize self
        self.parent = parent

    # Get the previous text
    def next_label(self):

        self.counter += 1

        if self.counter == len(self.text_list):
            self.counter = 0
        
        # Update the pickers racial bonuses
        self.parent.update_picker_bonus()

        self.update_label()

    # Get the previous text
    def past_label(self):

        self.counter -= 1

        if self.counter == -1:
            self.counter = len(self.text_list) - 1

        # Update the pickers racial bonuses
        self.parent.update_picker_bonus()

        self.update_label() 


# STAT PICKER --------------------------------------------------------
class StatPicker(UIElements.TextPicker):

    # An alternative to text picker in order to use to pick stats while creating characters

    def __init__(self, ui_handler, parent, pos, size, button_size=(40, 40), left_button_text="-", right_button_text="+", button_margin = 0):

        # Initialize parent class
        super().__init__(ui_handler, pos, size, text_list=["0"], button_size=button_size, left_button_text=left_button_text, right_button_text=right_button_text, button_margin=button_margin)

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

        super().__init__(ui_handler, pos, on_click_event = lambda: print("AAAA"), size = "medium", image=SaveSlot.SAVE_SLOT_EMPTY_IMAGE, text="")

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

                if line.startswith("PLAYER_NAME = "):

                    self.name_label.text = line[len("PLAYER_NAME = "):-1]
                elif line.startswith("PLAYER_CLASS = "):

                    self.class_label.text = line[len("PLAYER_CLASS = "):-1]
                elif line.startswith("PLAYER_HEALTH = "):

                    self.health_label.text = line[len("PLAYER_HEALTH = "):-1]
                elif line.startswith("PLAYER_LEVEL = "):

                    self.level_label.text = line[len("PLAYER_LEVEL = "):-1]
        
        

