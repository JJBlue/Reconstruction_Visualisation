from __future__ import annotations
from pathlib import Path

class Workspaces:
    __workspaces: list = []
    
    def __init__(self, file: Path):
        pass
    
    def addWorkspace(self):
        pass
    
    def removeWorkspace(self, workspace: Workspace):
        pass
    
    def getWorkspaces(self) -> list:
        pass
    
    @staticmethod
    def getAllWorkspaces() -> list:
        return Workspaces.__workspace
    
    @staticmethod
    def getOpenWorkspaces() -> list:
        pass
    

class Workspace:
    def __init__(self):
        self.loaded: bool = False
    
    def open(self) -> bool:
        raise NotImplementedError
    
    def close(self) -> bool:
        raise NotImplementedError