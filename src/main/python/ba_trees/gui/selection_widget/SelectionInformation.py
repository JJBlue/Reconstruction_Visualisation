from PyQt6.QtGui import QPixmap


class PointImageCoord: # TODO
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class ImagePoint:
    def __init__(self, pixmap: QPixmap):
        self.image: QPixmap = pixmap
        self.points: []

class Point: # TODO
    def __init__(self):
        self.point3D = None
        

class SelectionInformation: # TODO
    def __init__(self):
        self.points: list = [] # Point
    
    def addImage(self, pixmap: QPixmap):
        self.images.append(Point(pixmap))