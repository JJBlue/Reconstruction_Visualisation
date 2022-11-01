import os

from __future__ import annotations


class Directories:
    static_default_directories = None
    
    def __init__(self, working_dir: str):
        self.working_directory: str = working_dir
        self.config_folder: str = os.path.join(self.working_directory, "config")
    
    def getWorkingDirectory(self) -> str:
        return self.working_directory
    
    def getConfigFolder(self) -> str:
        return self.config_folder
    
    @staticmethod
    def getDefaultDirectories() -> Directories:
        if(Directories.static_default_directories == None):
            work_dir: str = os.getcwd()
            Directories.static_default_directories = Directories(work_dir)
        return Directories.static_default_directories
        