from __future__ import annotations

from pathlib import Path

from ba_trees import Workspace

import numpy as np

from render.data import TextureData, ModelData, GeometryData, TextureFile, Pane
from render.data.Geometry import Geometry
from render.render import Primitves, PrimitiveType


try:
    import pycolmap
except ImportError:
    print("pycolmap not found")

class ColmapWorkspace(Workspace):
    def __init__(self, folder: str):
        self.folder: str = folder
        self.folder_sparse: Path = Path(folder).joinpath("sparse")
        self.folder_images: Path = Path(folder).joinpath("images")
        self.folder_stereo: Path = Path(folder).joinpath("stereo")
        
        self.loaded: bool = False
        self.reconstruction = None
    
    def open(self) -> bool:
        if self.loaded:
            return True
        
        self.reconstruction = pycolmap.Reconstruction(self.folder_sparse.absolute())
        print(self.reconstruction.summary())
        # uv = camera.world_to_image(image.project(point3D.xyz))
        
        # Load Geometry
        self.model: ModelData = ModelData()
        self.model.addGeometry(ColmapGeometry(self))
        
        model_matrix = self.model.getModelMatrix()
        model_matrix.setYaw(3.2)
        
        # Load Cameras
        self.cameras: list = []
        for _, camera in self.reconstruction.cameras.items(): # model, width, height
            #camera = Camera()
            #self.cameras.append(camera)
            break
        
        # Load Images
        self.images: list = []
        for _, image in self.reconstruction.images.items(): # image_id, camera_id, name, triangulated
            image_file: str = self.folder_images.joinpath(image.name).absolute()
            texture: TextureData = TextureFile(image_file)
            
            model: ModelData = ModelData()
            model.addGeometry(Pane())
            model.addTexture(texture)
            # TODO Move ModelData
            
            self.images.append(model)
        
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
    
    def getModel(self) -> ModelData:
        if not self.loaded:
            return None
        
        return self.model
    
    def getImages(self) -> list:
        return self.images

class ColmapGeometry(Geometry):
    def __init__(self, workspace: ColmapWorkspace):
        super().__init__()
        
        self.workspace = workspace
        self.load()
    
    def load(self):
        vertices: list = []
        normals: list = []
        colors: list = []
        
        for _, point3d in self.workspace.reconstruction.points3D.items():
            vertices.extend(point3d.xyz)
            normals.extend([0.0, 0.0, 0.0])
            colors.extend(point3d.color / 255)
        
        self.primtive = Primitves.POINTS
        
        self.vertices = GeometryData(3, np.array(vertices, np.float32), PrimitiveType.FLOAT)
        self.all_vertices.append(self.vertices)
        
        self.normals = GeometryData(3, np.array(normals, np.float32), PrimitiveType.FLOAT)
        self.all_vertices.append(self.normals)
        
        self.colors = GeometryData(3, np.array(colors, np.float32), PrimitiveType.FLOAT)
        self.all_vertices.append(self.colors)