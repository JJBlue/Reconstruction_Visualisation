from __future__ import annotations

from pathlib import Path

from colmap_wrapper.colmap import COLMAP

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
        
        self.reconstruction = COLMAP(
                                        project_path=self.folder.absolute(),
                                        load_images=True,
                                        image_resize=0.3
                                    )
        
        self.opened = True
        return True
    
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
    
    def getProjects(self):
        return self.reconstruction.projects
    
    def getProjectType(self) -> str:
        return "colmap"
    