from concurrent.futures import ThreadPoolExecutor
from colmap_wrapper.colmap.camera import ImageInformation
from PyQt6.QtGui import QImage


class Point:
    def __init__(self, point3D_id, point3D):
        self.point3D_id = point3D_id
        self.point3D = point3D
        self.points: dict = {} # Image: [uv1, uv2]
    
    def add2DPoint(self, image, uv):
        if not (image in self.points):
            self.points[image] = []
        self.points[image].append(uv)
        
        image.points.append(self)

class Image:
    def __init__(self, imageinfo: ImageInformation, pyimage, image: QImage):
        self.imageinfo: ImageInformation = imageinfo
        self.pyimage = pyimage
        self.image: QImage = image
        self.points: list = [] # Point
    
    def get2DPoints(self):
        ps = [p.points[self] for p in self.points]
        ps = [item for sublist in ps for item in sublist] # https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists
        return ps

class SelectionInformation:
    def __init__(self, sub_project):
        self.sub_project = sub_project
        self.points: dict = {} # Point
        self.images: list = [] # Image
        
        reconstruction = sub_project.reconstruction
        
        executor = ThreadPoolExecutor(max_workers=5)
        
        for image_idx in reconstruction.images.keys():
            def run(sub_project = sub_project, reconstruction = reconstruction, image_idx = image_idx):
                imageinfo: ImageInformation = reconstruction.images[image_idx]
                pyimage = sub_project.pycolmap.images[image_idx]
                image = QImage(str(imageinfo.path))
                #print(image_idx)
                
                self.images.append(Image(imageinfo, pyimage, image))
            
            executor.submit(run)
        
        executor.shutdown(wait=True)
    
    def addPoint(self, point: Point, evaluate = True):
        if point.point3D_id in self.points:
            return
        
        if evaluate:
            point3D_id = point.point3D_id
            point3D = point.point3D
            
            for image in self.images:
                pyimage = image.pyimage
                
                if not pyimage.has_point3D(point3D_id):
                    continue
                
                camera_id = pyimage.camera_id
                pycolmap_camera = self.sub_project.pycolmap.cameras[camera_id]
                
                x, y = pycolmap_camera.world_to_image(pyimage.project(point3D.xyz))
                point.add2DPoint(image, [x, y])
                
        else:
            for image, _ in point.points.items():
                image.points.append(point)
        
        self.points[point.point3D_id] = point