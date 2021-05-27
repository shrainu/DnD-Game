from enum import Enum
import src.engine.debugger as Debugger


class Scenes(Enum):

    main_menu           = 0
    character_creation  = 1
    hub                 = 2
    dungeon             = 3


class Scene_Manager:

    current_scene   = Scenes.main_menu
    game_instance   = None
    scenes          = []

    @classmethod
    # Change the current scene
    def change_scene(cls, scene_name):

        # Check if previous scene needs to do a cleanup
        if callable(getattr(cls.scenes[cls.current_scene.value], "cleanup_scene", None)):

            cls.scenes[cls.current_scene.value].cleanup_scene()

        # Log message
        Debugger.Log_Manager.add_to_log_file("Changing scene: " + cls.scenes[cls.current_scene.value].scene_name + " -> " + cls.scenes[scene_name.value].scene_name)

        # Check if next scene needs to do a preparation
        if callable(getattr(cls.scenes[scene_name.value], "prepare_scene", None)):

            cls.scenes[scene_name.value].prepare_scene()

        # Change the current scene to scene given
        cls.current_scene = scene_name
    
    @classmethod
    # Return the current scene
    def get_current_scene(cls):

        return cls.current_scene

    @classmethod
    # Call the event for current scene
    def events(cls):

        cls.scenes[cls.current_scene.value].events()

    @classmethod
    # Call the update for current scene
    def update(cls):

        cls.scenes[cls.current_scene.value].update()

    @classmethod
    # Call the draw for current scene
    def draw(cls):

        cls.scenes[cls.current_scene.value].draw()
