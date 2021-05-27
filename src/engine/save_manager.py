import os


class Save_Manager:

    path_to_game_data   = os.getenv('PATH_TO_SAVE')
    current_save_folder = None
    path_to_save_folder = path_to_game_data + current_save_folder

    def __init__(self):

        

        pass

    @classmethod
    def laod_character(cls):

        player_name     = None
        player_class    = None
        player_health   = None
        player_level    = None

        with open(cls.path_to_save_folder, 'w') as save_file:

            save_data = save_file.readlines()

            for line in save_data:

                if line.startswith("PLAYER_NAME="):

                    player_name = line[len("PLAYER_NAME="):-1]
                elif line.startswith("PLAYER_CLASS="):

                    player_class = line[len("PLAYER_CLASS="):-1]
                elif line.startswith("PLAYER_CLASS="):

                    player_health = line[len("PLAYER_CLASS="):-1]
                elif line.startswith("PLAYER_CLASS="):

                    player_level = line[len("PLAYER_CLASS="):-1]


        return 


class Dungeon_Saver:

    def __init__(self):
        pass

    def load_dungeon():

        pass

