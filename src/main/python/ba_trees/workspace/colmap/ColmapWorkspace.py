from ba_trees.workspace import Workspace
from render.render import Geometry

try:
    import pycolmap
except ImportError:
    print("pycolmap not found")

class ColmapWorkspace(Workspace):
    def __init__(self, folder: str):
        self.folder: str = folder
        self.loaded: bool = False
        
        self.reconstruction = None
    
    def open(self) -> bool:
        if self.loaded:
            return True
        
        self.reconstruction = pycolmap.Reconstruction(self.folder)
        
        self.loaded = True
        return True
    
    def close(self) -> bool:
        if not self.loaded:
            return True
        
        self.reconstruction = None
        
        self.loaded = False
        return True
    
    def uselessMethodOnlyForTesting(self):
        print(self.reconstruction.summary())
        
        for image_id, image in self.reconstruction.images.items():
            print(image_id, image)
            
        for point3d_id, point3d in self.reconstruction.points3D.items():
            print(point3d_id, point3d)
        
        for camera_id, camera in self.reconstruction.cameras.items():
            print(camera_id, camera)
            
        # uv = camera.world_to_image(image.project(point3D.xyz))
    
    def getGeometry(self) -> Geometry:
        if not self.loaded:
            return None
        
        pass