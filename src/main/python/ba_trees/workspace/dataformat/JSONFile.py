import json
from pathlib import Path

from ba_trees.workspace import Project, Projects, Workspace


class WorkspaceJSONFile:
    """
        {
            'projects': [
                {
                    'type': 'colmap'
                    'folder': ''
                }
            ]
        }
    """
    
    @staticmethod
    def readWorkspace(file: Path = None) -> Workspace:
        data: dict = {}
        
        # Load from File
        if file.exists():
            with open(file, encoding="UTF-8") as f:
                data = json.load(f)
        
        return WorkspaceJSONFile.readWorkspaceFromJSONObject(file, data)
    
    @staticmethod
    def readWorkspaceFromJSONObject(file: Path = None, data: dict = {}) -> Workspace:
        workspace = Workspace(file)
        workspace.open()
        
        # Projects
        if "project" in data:
            for data_project in data["project"]:
                project: Project = ProjectJSONFile.readProjectFromJSONObject(data = data_project)
                workspace.addProject(project)
        
        return workspace
    
    @staticmethod
    def saveWorkspace(workspace: Workspace = None, file: Path = None):
        if file == None:
            file = workspace.workspace
        
        # Save to file
        with open(file, "w+", encoding="UTF-8") as f:
            json.dump(WorkspaceJSONFile.saveWorkspaceToJsonObject(workspace), f)
    
    @staticmethod
    def saveWorkspaceToJsonObject(workspace: Workspace) -> dict:
        data: dict = {}
        
        # Projects
        projects: list = []
        data["project"] = projects
        for project in workspace.getProjects():
            projects.append(ProjectJSONFile.saveProjectToJSONObject(project))
        
        return data
    
class ProjectJSONFile:
    @staticmethod
    def readProjectFromJSONObject(data: dict) -> Project:
        type_name: str = data["type"]
        folder: Path = Path(data["folder"])
        
        project: Project = Projects.createProject(type_name, folder)
        
        return project
    
    @staticmethod
    def saveProjectToJSONObject(project: Project = None) -> dict:
        data: dict = {}
        
        data["type"] = project.getProjectType()
        data["folder"] = str(project.getProjectFolder())
        
        return data