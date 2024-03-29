from __future__ import annotations

from pathlib import Path
from typing import Callable

from default.Synchronization import synchronized


class Projects:
    __types: dict = {}
    
    @staticmethod
    def addTypeProject(type_name: str, project_construct_function: Callable) -> bool:
        if type in Projects.__types:
            return False
        
        Projects.__types[type_name] = project_construct_function
        return True
    
    @staticmethod
    def removeTypeProject(type_name: str) -> bool:
        del Projects.__types[type_name]
        return True
    
    @staticmethod
    def createProject(type_name: str, folder: Path):
        return Projects.__types[type_name](folder)

class Project:
    def __init__(self, folder: Path):
        self.folder = folder
        self.name = self.getProjectFolder().name
        self.opened: bool = False
    
    def isOpened(self) -> bool:
        return self.opened
    
    @synchronized
    def open(self) -> bool:
        if self.opened or self.opening:
            return True
        
        self.opened = True
        return True
    
    @synchronized
    def close(self) -> bool:
        if not self.opened:
            return True
        
        self.opening = False
        self.opened = False
        return True
    
    def getProjectFolder(self) -> Path:
        return self.folder
    
    def getProjectName(self) -> str:
        return self.name
    
    def setProjectName(self, value: str):
        self.name = value
    
    def getProjectType(self) -> str:
        return None