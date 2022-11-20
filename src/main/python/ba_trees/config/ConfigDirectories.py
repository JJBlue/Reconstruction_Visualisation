from __future__ import annotations
from pathlib import Path

from default.directories import Directories


class ConfigDirectories:
    __static_default_directories = None
    
    def __init__(self):
        self.shader_folder = Path(self.getWorkingDirectory()).joinpath("shaders")
        self.workspace_folder = Path(self.getWorkingDirectory()).joinpath("workspace")
    
    def getWorkingDirectory(self) -> str:
        dirs = Directories.getDefaultDirectories()
        return dirs.getWorkingDirectory()
    
    def getConfigFolder(self) -> str:
        dirs = Directories.getDefaultDirectories()
        return dirs.getConfigFolder()
    
    def getShaderFolder(self):
        return self.shader_folder
    
    def getWorkspaceFolder(self):
        return self.workspace_folder
    
    @staticmethod
    def getDefaultConfigDirectories() -> ConfigDirectories:
        if(ConfigDirectories.__static_default_directories == None):
            ConfigDirectories.__static_default_directories = ConfigDirectories()
        return ConfigDirectories.__static_default_directories
        