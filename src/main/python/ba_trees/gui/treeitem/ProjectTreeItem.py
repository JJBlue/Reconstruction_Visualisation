from pathlib import Path

from PyQt6 import QtCore

from ba_trees.gui.project_widget.ProjectWidget import ProjectWidget
from ba_trees.gui.treeitem import PathTreeItem, Event
from ba_trees.gui.treeitem.CustomTreeItem import CustomTreeItem
from ba_trees.workspace import Project

class Runnable_Open_Project(QtCore.QThread):
    __signal = QtCore.pyqtSignal(object)
    
    def __init__(self, project: Project, project_widget, event: Event):
        super().__init__()
        
        self.project = project
        self.project_widget = project_widget
        self.event = event
        
        self.__signal.connect(self.runLater)
        
    def run(self):
        self.project.open()
        self.project.load()
        self.__signal.emit(None)
    
    def runLater(self):
        self.project_widget.ui.opengl_widget.addProject(self.project)
        
        # TODO
        from ba_trees.gui.image_pixel_widget import PointInImageWidget
        test = PointInImageWidget()
        
        sub_project = self.project.getPyColmapProjects()[0]
        sub_project_my = self.project.getProjects()[0]
        
        for point3D_id, point3D in sub_project.points3D.items():
            for _, image in sub_project.images.items():
                if not image.has_point3D(point3D_id):
                    continue
                
                camera_id = image.camera_id
                
                camera = sub_project.cameras[camera_id]
                #uv = camera.world_to_image(image.project(point3D.xyz))
                #print(uv)
                
                test.addImage(sub_project_my, camera, image, point3D)
            
            break
        
        window = self.event.window
        window.ui.tabs.addTab(test, "Test")

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
        
        self.thread = Runnable_Open_Project(self.project, project_widget, event)
        self.thread.start()