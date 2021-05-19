from typing import Type
from src.engine.debugger import Log_Manager
import os
import dotenv


class Game_Manager:

    game_name = 'UnnamedRogueLike'
    env_file = None

    @classmethod
    # Initialize env variables only called once per user
    def initialize_game(cls):

        # Check if the game data folder is created before 
        if not os.path.exists("C:/Users/" + os.getlogin() + "/AppData/LocalLow/" + Game_Manager.game_name):

            # Log message
            Log_Manager.add_to_log_file("Game data folder doesn't exist creating necessary files and directories.")

            # Create the game data folder if it's doesn't exists
            game_data_path = "C:/Users/" + os.getlogin() + "/AppData/LocalLow/" + Game_Manager.game_name
            os.makedirs(game_data_path)

            # Create save game folders
            for i in range(3):

                os.makedirs(game_data_path + "/saves/save_slot_" + str(i+1))

            # Do the same for the .env file
            with open("C:/Users/" + os.getlogin() + "/AppData/LocalLow/" + Game_Manager.game_name + "/.env", 'w') as envi_file:

                envi_file.write("INITIALIZED=False\nUSERNAME=None\nPATH_TO_SAVES=None\n")

        # Save the .env files file path
        Game_Manager.env_file = dotenv.find_dotenv("C:/Users/" + os.getlogin() + "/AppData/LocalLow/" + Game_Manager.game_name + "/.env")
        # Load the .env file
        dotenv.load_dotenv(Game_Manager.env_file)

        # Check if the game files initialized before
        initialized = os.getenv('INITIALIZED')

        if initialized != 'True':

            # Set the initialized to true
            os.environ['INITIALIZED'] = 'True'
            dotenv.set_key(Game_Manager.env_file, 'INITIALIZED', os.environ['INITIALIZED'])

            # Set the username to current user's username
            os.environ['USERNAME'] = os.getlogin()
            dotenv.set_key(Game_Manager.env_file, 'USERNAME', os.environ['USERNAME'])

            # Set the path to save files
            os.environ['PATH_TO_SAVES'] = 'C:/Users/' + os.getenv('USERNAME') + '/AppData/LocalLow/' + Game_Manager.game_name
            dotenv.set_key(Game_Manager.env_file, 'PATH_TO_SAVES', os.environ['PATH_TO_SAVES'])

            # Log message
            Log_Manager.add_to_log_file("Environment variable initialization compeleted.")
        else:

            # Log message
            Log_Manager.add_to_log_file("Environment variables are already initialized.")

    @classmethod
    # Set the value of a environment variable
    def set_environment_variables(cls, variable_name, value):

        exists = os.getenv(variable_name)

        if exists is not None:

            os.environ[variable_name] = value
            dotenv.set_key(Game_Manager.env_file, variable_name, os.environ[variable_name])

            # Log message
            Log_Manager.add_to_log_file("Environment variable '" + variable_name + "' value has been changed to: " + value)
        else:

            # Log message
            Log_Manager.add_to_log_file("There is none environment variable exists with the name: " + variable_name)