from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image as Img
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QImageReader
from colmap_wrapper.colmap.camera import ImageInformation


class Point:
    def __init__(self, point3D_id, point3D):
        self.selectionInformation = None
        self.point3D_id = point3D_id
        self.point3D = point3D
        self.points: dict = {} # Image: [uv1, uv2]
    
    def add2DPoint(self, image, uv):
        self.points[image] = uv
        image.points.append(self)

class Image:
    def __init__(self, imageinfo: ImageInformation, pyimage, path: Path):
        self.selectionInformation = None
        self.imageinfo: ImageInformation = imageinfo
        self.pyimage = pyimage
        
        #reader: QImageReader = QImageReader(str(path))
        #image = reader.read()
        
        self.path: Path = path
        self.width = 0
        self.height = 0
        self.image: QImage = None
        self.preview: QImage = None
        #self.image: QImage = image
        #self.preview: QImage = image.scaled(1920, 1080, Qt.AspectRatioMode.KeepAspectRatio)
        
        self.points: list = [] # Point
    
    def getImage(self):
        if self.image == None:
            self.image = QImage(str(self.path))
        return self.image
    
    def getPreviewImage(self):
        if self.preview == None:
            with Img.open(self.path) as img:
                width, height = img.size
                
                self.width = width
                self.height = height
                
                img.thumbnail([1920, 1080])
                img2 = img.convert("RGBA")
                data = img2.tobytes("raw", "BGRA")
                self.preview = QImage(data, img2.width, img2.height, QImage.Format.Format_ARGB32)
        
        return self.preview
    
    def getWidth(self):
        if self.width <= 0:
            self.getPreviewImage()
        return self.width
    
    def getHeight(self):
        if self.width <= 0:
            self.getPreviewImage()
        return self.height
    
    def get2DPoints(self):
        ps = [p.points[self] for p in self.points]
        #ps = [item for sublist in ps for item in sublist] # https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists
        return ps
    
    def getSelected2DPoints(self):
        ps = [p.points[self] for p in self.points if p.point3D_id in self.selectionInformation.selected_points]
        return ps

class SelectionInformation:
    def __init__(self, sub_project):
        self.sub_project = sub_project
        self.points: dict = {} # Point
        self.images: list = [] # Image
        
        self.selected_points: dict = {}
        
        
        reconstruction = sub_project.reconstruction
        
        executor = ThreadPoolExecutor(max_workers=5) # os.cpu_count()
        
        for image_idx in reconstruction.images.keys():
            def run(sub_project = sub_project, reconstruction = reconstruction, image_idx = image_idx):
                imageinfo: ImageInformation = reconstruction.images[image_idx]
                
                pyimage = sub_project.pycolmap.images[image_idx]
                
                image_info = Image(imageinfo, pyimage, imageinfo.path)
                image_info.getPreviewImage()
                image_info.selectionInformation = self
                
                self.images.append(image_info)
            
            executor.submit(run)
        
        executor.shutdown(wait=True)
    
    def selectPoint(self, *points):
        self.selected_points.clear()
        
        for point in points:
            if not (point.point3D_id in self.points):
                return
            
            self.selected_points[point.point3D_id] = point
    
    def addPoint(self, point: Point, evaluate = True):
        if point.point3D_id in self.points:
            return
        
        point.selectionInformation = self
        
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
    
    def removePoint(self, point: Point):
        del self.points[point.point3D_id]
        
        for image in point.points.keys():
            image.points.remove(point)