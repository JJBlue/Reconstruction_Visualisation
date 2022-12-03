from __future__ import annotations

from pathlib import Path

from default.Synchronization import synchronized
from ba_trees.config.Config import Config
from ba_trees.workspace import Project


class Workspaces:
    __workspace: Workspace = None
    
    @staticmethod
    @synchronized
    def setWorkspace(workspace: Workspace, save: bool = True):
        if Workspaces.__workspace != None:
            print(f"Close Workspace {workspace.workspace}")
            Workspaces.__workspace.close()
        
        Workspaces.__workspace = workspace
        
        if Workspaces.__workspace != None:
            print(f"Open Workspace {workspace.workspace}")
            Workspaces.__workspace.open()
        
        config: Config = Config.getConfig()
        config.set("latest_workspace", str(workspace.workspace))
        if save:
            config.save()
    
    @staticmethod
    def reopenLastSession() -> Workspace:
        config: Config = Config.getConfig()
        file: Path = Path(config.get("latest_workspace"))
        return Workspaces.openWorkspace(file, True, False)
    
    @staticmethod
    def openWorkspace(file: Path, change_current_workspace = True, save = True) -> Workspace:
        from ba_trees.workspace.dataformat.JSONFile import WorkspaceJSONFile
        workspace: Workspace = WorkspaceJSONFile.readWorkspace(file)
        if change_current_workspace:
            Workspaces.setWorkspace(workspace, save)
        return workspace
    
    @staticmethod
    def getWorkspace() -> Workspace:
        return Workspaces.__workspace

class Workspace:
    def __init__(self, file: Path):
        self.workspace: Path = file
        
        self.opened: bool = False
        self.projects: list = None
    
    def isOpend(self) -> bool:
        return self.opened
    
    @synchronized
    def open(self) -> bool:
        if self.opened:
            return True
        
        self.projects: list = []
        
        self.opened = True
        return True
    
    @synchronized
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