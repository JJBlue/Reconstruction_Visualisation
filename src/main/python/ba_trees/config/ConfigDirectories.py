from __future__ import annotations
from pathlib import Path

from default.directories import Directories


class ConfigDirectories:
    __static_default_directories = None
    
    def __init__(self):
        self.shader_folder: Path = Path(self.getWorkingDirectory()).joinpath("shaders")
        self.workspace_folder: Path = Path(self.getWorkingDirectory()).joinpath("workspace")
    
    def getWorkingDirectory(self) -> str:
        dirs = Directories.getDirectories()
        return dirs.getWorkingDirectory()
    
    def getConfigFolder(self) -> str:
        dirs = Directories.getDirectories()
        return dirs.getConfigFolder()
    
    def getShaderFolder(self) -> Path:
        return self.shader_folder
    
    def getWorkspaceFolder(self) -> Path:
        return self.workspace_folder
    
    @staticmethod
    def getConfigDirectories() -> ConfigDirectories:
        if(ConfigDirectories.__static_default_directories == None):
            ConfigDirectories.__static_default_directories = ConfigDirectories()
        return ConfigDirectories.__static_default_directories
        