from PyQt6.QtCore import QPoint, pyqtSignal
from PyQt6.QtGui import QPainter, QPen, QColor

from ba_trees.gui.imageview import ImageView
from ba_trees.gui.selection_widget import Image, SelectionInformation
from ba_trees.gui.selection_widget.SelectionInformation import Point


class SelectedImageWidget(ImageView):
    addPointSignal = pyqtSignal(Point)
    selectPointSignal = pyqtSignal(Point)
    
    def __init__(self, *args):
        super().__init__(*args)
        
        self.selectioninfo = None
        self.imageinfo = None
    
    def setImage2(self, selection: SelectionInformation, imageinfo: Image):
        self.selectioninfo = selection
        self.imageinfo = imageinfo
        self.setImage(self.imageinfo.image)
    
    def repaintImageOverride(self, painter: QPainter):
        size = 5
        
        pen: QPen = QPen()
        pen.setColor(QColor(255, 0, 0, 255))
        painter.setPen(pen)
        
        for points in self.imageinfo.get2DPoints():
            painter.drawEllipse(QPoint(int(points[0] * self.scale_factor), int(points[1] * self.scale_factor)), size, size)