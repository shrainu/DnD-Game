import pygame as pg
from pygame import image
pg.init()


# GLOBAL VARIABLES ---------------------------------------------------

# colors
_C_WHITE = (255, 255, 255)


# UI HANDLER ---------------------------------------------------------
class UI_Handler:

    # This object is necessary in order to draw the other ui elements
    # Its better having a different one for each scene

    def __init__(self):

        self.input_fields = []
        self.pickers = []
        self.buttons = []
        self.labels = []
    
    # Draw the ui elements
    def draw_ui(self, surface):

        # Draw the input fields
        for input_field in self.input_fields:
            input_field.draw_input_field(surface)

        # Draw the pickers
        for picker in self.pickers:
            picker.draw_picker(surface)

        # Draw the buttons
        for button in self.buttons:
            button.draw_button(surface)
        
        # Draw the labels
        for label in self.labels:
            label.draw_label(surface)
    
    def update(self, event_list):

        for input_field in self.input_fields:
            input_field.update(event_list)
        
        for button in self.buttons:
            button.update(event_list)


# LABEL --------------------------------------------------------------
class Label:

    _DEFAULT_FONT = pg.font.Font('fonts/Alkhemikal.ttf', 40)
    _DEFAULT_COLOR = _C_WHITE

    def __init__(self, ui_handler, pos, text, font = None, color = None):

        # Initialize self
        self.pos = ["x", "y"]
        self.pos[0] = pos[0]
        self.pos[1] = pos[1]
        self.text = text
        self.visible = True
        # initialize font
        if font is not None:
            self.font = font
        else:
            self.font = Label._DEFAULT_FONT
        # initialize color
        if color is not None:
            self.color = color
        else:
            self.color = Label._DEFAULT_COLOR

        # Add self to ui_handler labels list
        ui_handler.labels.append(self)

    # Get the height and width of the text    
    def get_text_size(self):

        text_width, text_height = self.font.size(self.text)
    
        return (text_width, text_height)

    # Draw the label -This functions is automaticly called by ui_handler-
    def draw_label(self, surface):

        if self.visible:

            surface.blit(self.font.render(self.text, 0, self.color), self.pos)

    def change_visiblity(self, value = None):

        if value is None:
            self.visible = not self.visible
        else:
            self.visible = value


# BUTTON -------------------------------------------------------------
class Button:

    DEFAULT_PATH = 'assets/ui/button_'

    def __init__(self, ui_handler, pos, on_click_event, size = "medium", image = None, text = None):

        # Initialize self
        # Load button image
        if image == None:
            self.image = pg.image.load((Button.DEFAULT_PATH + size + ".png"))
        else:
            self.image = pg.image.load(image)
        self.visible = True
        self.rect = pg.Rect(pos, (self.image.get_width(), self.image.get_height()))
        self.button_down = False
        self.on_click_event = on_click_event

        # Initialize children
        if text is not None:

            # Create the label
            self.label = Label(ui_handler, (self.rect.x, self.rect.y), text)
            # Center the label
            self.set_label_position()
        else:

            self.label = None

        # Add self to ui_handler buttons list
        ui_handler.buttons.append(self)

    # Draw the button -This functions is automaticly called by ui_handler-
    def draw_button(self, surface):

        # draw the button
        if self.visible:

            surface.blit(self.image, self.rect)

    def change_visiblity(self, value = None):

        if value is None:
            self.visible = not self.visible
        else:
            self.visible = value

        if self.label is not None:

            self.label.visible = self.visible

    def set_label_position(self):

        if self.label is not None:

            self.label_size = self.label.get_text_size()

            x_margin = (self.rect.width - self.label_size[0])
            y_margin = (self.rect.height - self.label_size[1])

            # Set the x position
            self.label.pos[0] = self.rect.x + ( x_margin / 2 )
            # Set the y position
            self.label.pos[1] = self.rect.y + ( y_margin / 2 )

    def mouse_on_click(self, event_list):

        for event in event_list:

            if event.type == pg.MOUSEBUTTONDOWN:

                x, y = event.pos
                if event.button == 1:
                    if self.rect.x < x < self.rect.x + self.rect.width:
                        if self.rect.y < y < self.rect.y + self.rect.height:

                            self.button_down = True
            elif event.type == pg.MOUSEBUTTONUP:

                x, y = event.pos
                if event.button == 1:
                    if self.rect.x < x < self.rect.x + self.rect.width:
                        if self.rect.y < y < self.rect.y + self.rect.height and self.button_down:

                            self.on_click_event()
                self.button_down = False

    # This functions is NOT automaticly called by ui handler
    def update(self, event_list):

        if self.visible:

            self.mouse_on_click(event_list)


# TEXT PICKER --------------------------------------------------------
class TextPicker():

    DEFAULT_PATH = 'assets/ui/input_field_'

    def __init__(self, ui_handler, pos, text_list, size = "medium", left_button_text="<", right_button_text=">", button_margin = 0):

        # Initialize self
        self.image = pg.image.load(TextPicker.DEFAULT_PATH + size + ".png")
        self.visible = True
        self.rect = pg.Rect(pos, (self.image.get_width(), self.image.get_height()))
        self.text_list = text_list
        self.counter = 0
        # Add self to ui_handler pickers list
        ui_handler.pickers.append(self)

        # Initialize childs
        # Initialize label
        self.label = Label(
            ui_handler  = ui_handler,
            pos         = (self.rect.x, self.rect.y),
            text        = self.text_list[self.counter],
            font        = None, # This will use default
            color       = None  # This will use default
        )
        self.label_size = None
        self.set_label_position()
        # Initialize left button
        buttom_image_path = "assets/ui/text_picker_button.png"
        self.left_button = Button(
            ui_handler      = ui_handler,
            pos             = (self.rect.x - 40 - button_margin, self.rect.y),
            image           = buttom_image_path,
            on_click_event  = self.past_label,
            text            = left_button_text
        )
        # Initialize right button
        self.right_button = Button(
            ui_handler      = ui_handler,
            pos             = (self.rect.x + self.rect.width + button_margin, self.rect.y),
            image           = buttom_image_path,
            on_click_event  = self.next_label,
            text            = right_button_text
        )

    # Draw the text picker -This functions is automaticly called by ui_handler-
    def draw_picker(self, surface):

        if self.visible:

            surface.blit(self.image, self.rect)

    def change_visiblity(self, value = None):

        if value is None:
            self.visible = not self.visible
        else:
            self.visible = value

        self.label.visible = self.visible
        self.left_button.visible = self.visible
        self.right_button.visible = self.visible

    # Return the current text in the label
    def return_label(self):

        return self.text_list[self.counter]

    # Get the next text
    def next_label(self):

        self.counter += 1

        if self.counter == len(self.text_list):
            self.counter = 0
        
        self.update_label()

    # Get the previous text
    def past_label(self):

        self.counter -= 1

        if self.counter == -1:
            self.counter = len(self.text_list) - 1
        
        self.update_label()
    
    # Update the text label to show new text
    def update_label(self):

        self.label.text = self.text_list[self.counter]

        self.set_label_position()
    
    def set_label_position(self):

        self.label_size = self.label.get_text_size()

        x_margin = (self.rect.width - self.label_size[0])
        y_margin = (self.rect.height - self.label_size[1])

        # Set the x position
        self.label.pos[0] = self.rect.x + ( x_margin / 2 )
        # Set the y position
        self.label.pos[1] = self.rect.y + ( y_margin / 2 )


# INPUT FIELD --------------------------------------------------------
class InputField:

    valid_keys = [
        "q", "w", "e", "r", "t", "y", "u", "i", "o", "p",
        "a", "s", "d", "f", "g", "h", "j", "k", "l", "'",
        "z", "x", "c", "v", "b", "n", "m",
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"
    ]

    DEFAULT_PATH = "assets/ui/input_field_"

    def __init__(self, ui_handler, pos, size = "medium", text = "", text_limit=16):

        # Initialize self
        self.image = pg.image.load((InputField.DEFAULT_PATH + size + ".png"))
        self.visible = True
        self.rect = pg.Rect(pos, (self.image.get_width(), self.image.get_height()))
        self.text = ""
        self.text_limit = text_limit
        self.in_focus = False
        self.keys_pressed = []
        self.uppercase = False

        # Initialize children
        self.label = Label(ui_handler, pos, text)
        self.set_label_position()

        # Add self to ui_handlers childs
        ui_handler.input_fields.append(self)

    # Draw the input fields borders
    def draw_input_field(self, surface):

        if self.visible:

            surface.blit(self.image, self.rect)

    def change_visiblity(self, value = None):

        if value is None:
            self.visible = not self.visible
        else:
            self.visible = value

        self.label.visible = self.visible

    # Get the keys pressed and manage them
    def get_keys_pressed(self, event_list):
        
        for event in event_list:

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_BACKSPACE:

                    self.text = self.text[:-1]
                    self.update_label()
                elif event.key == pg.K_CAPSLOCK:

                    self.uppercase = not self.uppercase
                elif event.key == pg.K_SPACE:

                    self.text += " "
                    self.update_label()
                else:

                    key_pressed = pg.key.name(event.key)
                    
                    if len(self.text) < self.text_limit:

                        for valid_key in InputField.valid_keys:

                            if key_pressed == valid_key:

                                if self.uppercase:
                                    self.text += key_pressed.upper()
                                else:
                                    self.text += key_pressed 

                                self.update_label()

    # Detect if user presed the input field
    def mouse_on_click(self, event_list):

        for event in event_list:

            if event.type == pg.MOUSEBUTTONDOWN:

                x,y = event.pos

                if self.rect.x < x < self.rect.x + self.rect.width:
                    if self.rect.y < y < self.rect.y + self.rect.height:

                        self.in_focus = True
                    else:
                        self.in_focus = False
                else:
                    self.in_focus = False

    # Update the text label to show new text
    def update_label(self):

        self.label.text = self.text

        self.set_label_position()
    
    # Set the position of the label
    def set_label_position(self):

        self.label_size = self.label.get_text_size()

        x_margin = (self.rect.width - self.label_size[0])
        y_margin = (self.rect.height - self.label_size[1])

        # Set the x position
        self.label.pos[0] = self.rect.x + ( x_margin / 2 )
        # Set the y position
        self.label.pos[1] = self.rect.y + ( y_margin / 2 )

    # This function is called automaticly by ui_handler
    def update(self, event_list):

        if self.visible:

            self.mouse_on_click(event_list)

            if self.in_focus:
                self.get_keys_pressed(event_list)


class Canvas:

    
    def __init__(self, pos, size, childs, visible=False):

        self.rect = pg.Rect(pos, size)
        self.visible = visible

        self.childs = childs
        self.set_children_visiblity()
    
    def change_visiblity(self, value = None):

        if value is None:
            self.visible = not self.visible
        else:
            self.visible = value

        self.set_children_visiblity()

    def set_children_visiblity(self):

        for child in self.childs:

            child.change_visiblity(self.visible)