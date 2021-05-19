from enum import Enum


class Scenes(Enum):

    main_menu   = 0
    hub         = 1
    dungeon     = 2


class Scene_Manager:

    current_scene = Scenes.main_menu
    game_instance = None

    @classmethod
    # Change the current scene
    def change_scene(cls, scene_name):

        # Change the current scene to scene given
        cls.current_scene = scene_name
        # Make the same changes for the game class too
        cls.game_instance.current_scene = cls.current_scene
    
    @classmethod
    # Return the current scene
    def get_current_scene(cls):

        return cls.current_scene

