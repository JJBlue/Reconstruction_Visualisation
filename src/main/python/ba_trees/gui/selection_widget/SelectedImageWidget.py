from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QPainter, QPen, QColor

from ba_trees.gui.imageview import ImageView


class SelectedImageWidget(ImageView):
    def __init__(self, *args):
        super().__init__(*args)
        
        self.list_points = []
    
    def repaintImageOverride(self, painter: QPainter):
        size = 5
        
        pen: QPen = QPen()
        pen.setColor(QColor(255, 0, 0, 255))
        painter.setPen(pen)
        
        for points in self.list_points:
            painter.drawEllipse(QPoint(int(points[0] * self.scale_factor), int(points[1] * self.scale_factor)), size, size)
    
    def mouseDoubleClickEvent(self, event):
        if self.image == None:
            return
        
        pos = event.pos()
        x = pos.x() / self.scale_factor
        y = pos.y() / self.scale_factor
        
        if x < 0 or x > self.image.width():
            return
        
        if y < 0 or y > self.image.height():
            return
        
        self.list_points.append([x, y])
        self.repaintImage()
    
    def mouseReleaseEvent(self, event):
        if self.image == None:
            return
        
        pos = event.pos()
        x = pos.x() / self.scale_factor
        y = pos.y() / self.scale_factor
        
        if x < 0 or x > self.image.width():
            return
        
        if y < 0 or y > self.image.height():
            return
        
        
        
        
        pass