import os
from datetime import datetime


class Log_Manager:

    session_dir = ""
    log_file_path = ""

    def __init__(self):

        self.session_dir = "log/" + datetime.now().strftime("%d.%m.%Y") + "/"
        self.log_file_name = "log_" + datetime.now().strftime("%d.%m.%Y_%H.%M") + ".txt"

        # Add log file path and folder path to Log Manager class variables
        Log_Manager.session_dir = self.session_dir
        Log_Manager.log_file_path = self.session_dir + self.log_file_name

        # Create today's session lof folder if that doesn't exists
        if not os.path.exists(self.session_dir):

            os.makedirs(self.session_dir)        

        # Write the first log entries
        with open(Log_Manager.log_file_path, 'w') as log_file:

            log_file.write(Log_Manager.return_current_time() + "Game has started." + "\n")
            log_file.write(Log_Manager.return_current_time() + "Session log folder has been created." + "\n")

    @classmethod
    # Return the current time to make it easier to write
    def return_current_time(cls):

        return datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " -\t"

    @classmethod
    # Add a new entry to log
    def add_to_log_file(cls, text):

        with open(cls.log_file_path, 'a') as log_file:

            log_file.write(cls.return_current_time() + text + "\n")