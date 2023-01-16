from __future__ import annotations

import threading

from pathlib import Path

from colmap_wrapper.colmap import COLMAP, LoadElement

from ba_trees.status_information import StatusInformation, StatusInformationChild
from ba_trees.status_information.StatusInformation import StatusInformations, Status
from ba_trees.workspace import Project
from default.Synchronization import synchronized


class ColmapProject(Project):
    def __init__(self, folder: Path):
        super().__init__(folder)
        self.loaded: bool = False
        self.reconstruction = None
    
    @synchronized
    def open(self) -> bool:
        if self.opened:
            return True
        
        self.__status: dict = {}
        self.__status_child: dict = {}
        self.__lock = threading.Lock()
        
        status_project = StatusInformation()
        status_project.text = f"Open Project: {self.getProjectName()}"
        for data in LoadElement:
            child = StatusInformationChild()
            child.setStatus(Status.NOT_STARTED)
            status_project.add(child)
            self.__status_child[data] = child
        
        StatusInformations.addStatus(status_project)
        
        self.reconstruction = COLMAP(
                                        project_path=self.folder.absolute(),
                                        load_depth=True,
                                        image_resize=0.3,
                                        output_status_function=self.__outputFunction
                                    )
        
        self.projects_pycolmap: list = []
        self.projects: list = []
        try:
            import pycolmap
            
            for project in self.reconstruction.projects:
                pycolmap = pycolmap.Reconstruction(project._sparse_base_path)
                
                self.projects_pycolmap.append(pycolmap)
                self.projects.append(ColmapSubProject(project, pycolmap))
                
        except:
            pass
        
        StatusInformations.removeStatus(status_project)
        
        self.opened = True
        del self.__status # TODO: Maybe raise Condition, if __outputFunction is callable after opening (Currently Constructor COLMAP blocks until finished. So currently no problems)
        del self.__status_child
        
        
        return True
    
    def __outputFunction(self, event):
        if self.opened:
            return
        
        key_project = event.project
        key = event.element
        
        self.__lock.acquire()
        if not (key_project in self.__status):
            self.__status[key_project] = {}
        self.__lock.release()
        
        status_dict = self.__status[key_project]
        
        if key in [LoadElement.DEPTH_IMAGE, LoadElement.IMAGE_INFO]:
            if not event.isFinished():
                self.__lock.acquire() # Maybe for each dict a seperate Lock?
                if key in status_dict:
                    self.__lock.release()
                    return
                
                status = StatusInformation()
                status.text = f"Load {self.getProjectName()}: {key.name}"
                
                for _ in range(event.max_id):
                    child = StatusInformationChild()
                    status.add(child)
                    child.setStatus(Status.NOT_STARTED)
                
                status_dict[key] = status
                StatusInformations.addStatus(status)
                self.__lock.release()
                
            elif event.isFinished():
                if key in status_dict:
                    status = status_dict[key]
                    child = status.get(event.current_id)
                    child.setStatus(Status.FINISHED)
                    
                    if status.isFinished():
                        self.__status_child[key].setStatus(Status.FINISHED)
            
            return
        
        
        if not event.isFinished():
            status = StatusInformation()
            status.text = f"Load {self.getProjectName()}: {key.name}"
            
            child = StatusInformationChild()
            status.add(child)
            child.setStatus(Status.STARTED)
            
            status_dict[key] = child
            StatusInformations.addStatus(status)
            
        elif event.isFinished():
            if key in status_dict: 
                status_dict[key].setStatus(Status.FINISHED)
            
            if key in self.__status_child:
                self.__status_child[key].setStatus(Status.FINISHED)
    
    @synchronized
    def load(self) -> bool:
        if self.loaded:
            return True
        
        self.loaded = True
        return True
    
    @synchronized
    def close(self) -> bool:
        if not self.opened:
            return True
        
        self.reconstruction = None
        
        self.opened = False
        return True
    
    def getReconstruction(self) -> COLMAP:
        return self.reconstruction
    
    def getPyColmapProjects(self) -> list:
        return self.projects_pycolmap
    
    def getProjects(self) -> list:
        return self.projects
    
    def getProjectType(self) -> str:
        return "colmap"

class ColmapSubProject:
    def __init__(self, reconstruction = None, pycolmap = None):
        self.reconstruction = reconstruction
        self.pycolmap = pycolmap