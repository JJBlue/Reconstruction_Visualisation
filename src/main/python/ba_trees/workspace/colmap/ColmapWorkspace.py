from __future__ import annotations

from colmap_wrapper.colmap import COLMAP
from ba_trees import Workspace
from render.data import TextureData, ModelData, TextureFile, Pane
from render.data.GeometryO3D import GeometryO3DPointCloud


class ColmapWorkspace(Workspace):
    def __init__(self, folder: str):
        self.folder: str = folder
        
        self.loaded: bool = False
        self.reconstruction = None
    
    def open(self) -> bool:
        if self.loaded:
            return True
        
        self.reconstruction = COLMAP(
                                        project_path=self.folder,
                                        dense_pc='fused.ply',
                                        load_depth=False,
                                        image_resize=0.3
                                    )
        
        # Load Geometry
        self.model: ModelData = ModelData()
        self.model.addGeometry(GeometryO3DPointCloud(self.reconstruction.get_sparse()))
        self.model.addGeometry(GeometryO3DPointCloud(self.reconstruction.get_dense()))
        
        #camera = project.cameras
        #images = project.images
        #sparse = project.get_sparse()
        #dense = project.get_dense()
        
        # Load Cameras
        self.cameras: list = []
        for camera in self.reconstruction.cameras:
            #camera = Camera()
            #self.cameras.append(camera)
            break
        
        # Load Images
        self.images: list = []
        for image in self.reconstruction.images:
            break
            #image_file: str = self.folder_images.joinpath(image.name).absolute()
            #texture: TextureData = TextureFile(image_file)
            
            #model: ModelData = ModelData()
            #model.addGeometry(Pane())
            #model.addTexture(texture)
            # TODO Move ModelData
            
            #self.images.append(model)
        
        # Finished
        self.loaded = True
        return True
    
    def close(self) -> bool:
        if not self.loaded:
            return True
        
        self.reconstruction = None
        self.geometry = None
        self.cameras = None
        
        self.loaded = False
        return True
    
    def getColmapData(self) -> COLMAP:
        return self.reconstruction
    
    def getModel(self) -> ModelData:
        if not self.loaded:
            return None
        
        return self.model
    
    def getImages(self) -> list:
        return self.images
    