from pathlib import Path

from ba_trees.gui.project_widget.ProjectWidget import ProjectWidget
from ba_trees.gui.treeitem import PathTreeItem, Event
from ba_trees.gui.treeitem.CustomTreeItem import CustomTreeItem
from ba_trees.workspace import Project


class ProjectTreeItem(CustomTreeItem):
    def __init__(self, project: Project):
        super().__init__()
        
        self.project: Project = project
        
        project_folder: Path = project.getProjectFolder()
        
        self.setEditable(False)
        self.setText(project_folder.parts[-1])
        
        self.loaded_childs: bool = False
    
    def doubleClickedEvent(self, event: Event):
        if not self.loaded_childs:
            self.loaded_childs = True
            
            files = self.project.getProjectFolder().iterdir()
            for f in files:
                child_item = PathTreeItem(f)
                self.appendRow(child_item)
        
        # self.project.open()
        
        window = event.window
        window.ui.tabs.addTab(ProjectWidget(), "Project")