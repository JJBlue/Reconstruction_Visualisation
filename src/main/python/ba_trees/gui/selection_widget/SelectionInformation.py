from PIL import Image as Img
from PyQt6.QtGui import QPixmap, QImage
from colmap_wrapper.colmap.camera import ImageInformation


class PointImageCoord:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Point: # TODO
    def __init__(self):
        self.point3D = None
        self.points: dict = {} # Image: PointImageCoord

class Image:
    def __init__(self, image: ImageInformation, pixmap: QPixmap):
        self.image: ImageInformation = image
        self.pixmap: QPixmap = pixmap
        self.points: [] # Point

class SelectionInformation:
    def __init__(self, sub_project):
        self.sub_project = sub_project
        self.points: list = [] # Point
        self.images: list = [] # Image
        
        reconstruction = sub_project.reconstruction
        
        for image_idx in reconstruction.images.keys():
            image: ImageInformation = reconstruction.images[image_idx]
                
            with Img.open(image.path) as img:
                img2 = img.convert("RGBA")
                data = img2.tobytes("raw", "BGRA")
                qimg = QImage(data, img2.width, img2.height, QImage.Format.Format_ARGB32)
                pixmap = QPixmap(qimg)
                
                self.images.append(Image(image, pixmap))