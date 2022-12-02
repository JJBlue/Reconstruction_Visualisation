from __future__ import annotations

from pathlib import Path

from ba_trees.config.Config import Config
from ba_trees.workspace import Project


class Workspaces:
    __workspace: Workspace = None
    
    @staticmethod
    def setWorkspace(workspace: Workspace):
        if Workspaces.__workspace != None:
            print(f"Close Workspace {workspace}")
            Workspaces.__workspace.close()
        
        Workspaces.__workspace = workspace
        
        if Workspaces.__workspace != None:
            print(f"Open Workspace {workspace}")
            Workspaces.__workspace.open()
        
        config: Config = Config.getConfig()
        config.set("latest_workspace", str(workspace.workspace))
        config.save()
    
    @staticmethod
    def getWorkspace() -> Workspace:
        return Workspaces.__workspace

class Workspace:
    def __init__(self, file: Path):
        self.workspace: Path = file
        
        self.opened: bool = False
        self.projects: list = []
    
    def isOpend(self) -> bool:
        return self.opened
    
    def open(self) -> bool:
        if self.opened:
            return True
        
        self.opened = True
        return True
    
    def close(self) -> bool:
        if not self.opened:
            return True
        
        self.projects = None
        
        self.opened = False
        return True
    
    def save(self):
        if not self.opened:
            return
        
        from ba_trees.workspace.dataformat.JSONFile import WorkspaceJSONFile
        WorkspaceJSONFile.saveWorkspace(self)
    
    def addProject(self, project: Project):
        if not self.opened:
            return
        
        self.projects.append(project)
    
    def removeProject(self, project: Project):
        if not self.opened:
            return
        
        self.projects.remove(project)
    
    def getProjects(self) -> list:
        return self.projects