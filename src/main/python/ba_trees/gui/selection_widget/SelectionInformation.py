from PyQt6.QtGui import QImage
from colmap_wrapper.colmap.camera import ImageInformation


class PointImageCoord:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Point:
    def __init__(self):
        self.point3D = None
        self.points: dict = {} # Image: PointImageCoord

class Image:
    def __init__(self, imageinfo: ImageInformation, image):
        self.image: ImageInformation = imageinfo
        self.image = image
        self.points: [] # Point

class SelectionInformation:
    def __init__(self, sub_project):
        self.sub_project = sub_project
        self.points: list = [] # Point
        self.images: list = [] # Image
        
        reconstruction = sub_project.reconstruction
        
        for image_idx in reconstruction.images.keys():
            imageinfo: ImageInformation = reconstruction.images[image_idx]
            image = QImage(str(imageinfo.path))
            #print(image_idx)
            
            self.images.append(Image(imageinfo, image))