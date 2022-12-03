from pathlib import Path

from PyQt6 import QtGui
from PyQt6.QtCore import QRunnable, QThreadPool

from ba_trees.gui.project_widget.ProjectWidget import ProjectWidget
from ba_trees.gui.treeitem import PathTreeItem, Event
from ba_trees.gui.treeitem.CustomTreeItem import CustomTreeItem
from ba_trees.workspace import Project


class Runnable_Open_Project(QRunnable):
    def __init__(self, project: Project, project_widget, event: Event):
        super().__init__()
        self.project = project
        self.project_widget = project_widget
        self.event = event
        
    def run(self):
        #QtGui.QOpenGLContext.makeCurrent(surface)
        #QtGui.QOpenGLContext.currentContext().functions()
        self.project.open()
        self.project.load()
        self.project_widget.ui.opengl_widget.addProject(self.project)

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
        
        project_widget = ProjectWidget()
        
        window = event.window
        window.ui.tabs.addTab(project_widget, "Project")
        
        #QThreadPool.globalInstance().start(Runnable_Open_Project(self.project, project_widget, event))
        #Runnable_Open_Project(self.project, project_widget, event).run()