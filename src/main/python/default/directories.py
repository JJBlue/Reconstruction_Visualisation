import os

class Directories:
    working_directory = ""
    config_folder = ""
    
    static_default_directories = None
    
    def __init__(self, working_dir: str):
        self.working_directory = working_dir
        self.config_folder = self.working_directory + "/config"
    
    def getWorkingDirectory(self):
        return self.working_directory
    
    def getConfigFolder(self):
        return self.config_folder
    
    @staticmethod
    def getDefaultDirectories():
        if(Directories.static_default_directories == None):
            work_dir: str = os.getcwd()
            Directories.static_default_directories = Directories(work_dir)
        return Directories.static_default_directories
        