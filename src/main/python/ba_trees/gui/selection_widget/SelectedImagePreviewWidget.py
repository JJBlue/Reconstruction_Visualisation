from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QPainter, QPen, QColor

from ba_trees.gui.imageview import ImageView
from ba_trees.gui.selection_widget import Image


class SelectedImagePreviewWidget(ImageView):
    def __init__(self, *args):
        super().__init__(*args)
        
        self.selectioninfo = None
        self.imageinfo = None
    
    def setImage2(self, imageinfo: Image):
        self.selectioninfo = imageinfo.selectionInformation
        self.imageinfo = imageinfo
        self.setImage(self.imageinfo.image)
    
    def repaintImageOverride(self, painter: QPainter):
        size = 5
        
        pen: QPen = QPen()
        pen.setColor(QColor(255, 0, 0, 255))
        painter.setPen(pen)
        
        for points in self.imageinfo.get2DPoints():
            painter.drawEllipse(QPoint(int(points[0] * self.scale_factor), int(points[1] * self.scale_factor)), size, size)
        
        
        pen.setColor(QColor(255, 255, 0, 255))
        painter.setPen(pen)
        
        for points in self.imageinfo.getSelected2DPoints():
            painter.drawEllipse(QPoint(int(points[0] * self.scale_factor), int(points[1] * self.scale_factor)), size, size)