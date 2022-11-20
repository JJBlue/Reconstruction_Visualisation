from __future__ import annotations

import numpy as np

from pathlib import Path

from ba_trees import Workspace
from render.render import Geometry, Primitves, GeometryData, PrimitiveType


try:
    import pycolmap
except ImportError:
    print("pycolmap not found")

class ColmapWorkspace(Workspace):
    def __init__(self, folder: str):
        self.folder: str = folder
        self.folder_sparse: str = Path(folder).joinpath("sparse").absolute()
        self.folder_images: str = Path(folder).joinpath("images").absolute()
        self.folder_stereo: str = Path(folder).joinpath("stereo").absolute()
        
        self.loaded: bool = False
        self.reconstruction = None
    
    def open(self) -> bool:
        if self.loaded:
            return True
        
        self.reconstruction = pycolmap.Reconstruction(self.folder_sparse)
        print(self.reconstruction.summary())
        # uv = camera.world_to_image(image.project(point3D.xyz))
        
        # Load Geometry
        self.geometry: Geometry = ColmapGeometry(self)
        self.geometry.load()
        
        self.cameras: list = []
        for _, camera in self.reconstruction.cameras.items(): # model, width, height
            #camera = Camera()
            #self.cameras.append(camera)
            break
        
        for _, _ in self.reconstruction.images.items(): # image_id, camera_id, name, triangulated
            break
        
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
    
    def getGeometry(self) -> ColmapGeometry:
        if not self.loaded:
            return None
        
        return self.geometry

class ColmapGeometry(Geometry):
    def __init__(self, workspace: ColmapWorkspace):
        super().__init__()
        
        self.workspace = workspace
    
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