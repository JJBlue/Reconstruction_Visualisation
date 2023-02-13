import glm

from sklearn.neighbors import KDTree
from PyQt6.QtCore import pyqtSignal, Qt

from ba_trees.gui.selection_widget import Point
from ba_trees.gui.selection_widget.SelectedImagePreviewWidget import SelectedImagePreviewWidget
from ba_trees.gui.selection_widget.SelectionInformation import Image


class SelectedImageWidget(SelectedImagePreviewWidget):
    addPointSignal = pyqtSignal(Point)
    removePointSignal = pyqtSignal(Point)
    selectPointSignal = pyqtSignal(Point)
    
    def __init__(self, *args):
        super().__init__(*args)
        
        self.tree_nearest_points_xy = None # TODO for more efficiency safe data in SelectionInformation.Image (self.imageinfo)
        self.tree_nearest_point = None # TODO for more efficiency safe data in SelectionInformation.Image (self.imageinfo)
    
    def setImage2(self, imageinfo: Image):
        self.tree_nearest_points_xy = None
        self.tree_nearest_point = None
        
        self.selectioninfo = imageinfo.selectionInformation
        self.imageinfo = imageinfo
        self.setImage(self.imageinfo.getImage())
    
    def keyReleaseEvent(self, event):
        key = event.key()
        
        if key == Qt.Key.Key_Delete or key == Qt.Key.Key_Backspace:
            for point in self.selectioninfo.selected_points.values():
                self.removePointSignal.emit(point)
                self.repaintImage()
    
    def __getXYZ(self, event):
        if self.image == None:
            return None
        
        pos = event.pos()
        x = int((self.horizontalScrollBar().value() + pos.x()) / self.scale_factor)
        y = int((self.verticalScrollBar().value() + pos.y()) / self.scale_factor)
        
        uv = glm.vec2(x, y)
        depth = self.imageinfo.getDepth(uv)
        if depth <= 0:
            return None
        
        return self.imageinfo.toXYZ(uv, depth)
    
    def __getNearestPoint(self, event):
        xyz = self.__getXYZ(event)
        
        if xyz != None:
            return xyz
        
        pos = event.pos()
        x = int((self.horizontalScrollBar().value() + pos.x()) / self.scale_factor)
        y = int((self.verticalScrollBar().value() + pos.y()) / self.scale_factor)
        
        if self.tree_nearest_point == None:
            self.tree_nearest_points_xy = []
            
            for u in range(self.imageinfo.getWidth()):
                for v in range(self.imageinfo.getHeight()):
                    uv = glm.vec2(u, v)
                    depth = self.imageinfo.getDepth(uv)
                    
                    if depth <= 0:
                        continue
                    
                    self.tree_nearest_points_xy.append([u, v])
            
            self.tree_nearest_point = KDTree(self.tree_nearest_points_xy, leaf_size=2)
        
        
        _, point_id_nearest = self.tree_nearest_point.query([[x, y]], k=1)
        point_id_nearest = point_id_nearest[0][0]
        
        points_xy = self.tree_nearest_points_xy[point_id_nearest]
        
        return self.imageinfo.toXYZFromDepthMap(glm.vec2(points_xy))
    
    def __getNearestPointFromSelections(self, event):
        if self.image == None:
            return None
        
        if len(self.imageinfo.points) <= 0:
            return None
        
        pos = event.pos()
        x = (self.horizontalScrollBar().value() + pos.x()) / self.scale_factor
        y = (self.verticalScrollBar().value() + pos.y()) / self.scale_factor
        
        points_xy = []
        points = []
        
        for point in self.imageinfo.points:
            points_xy.append(point.points[self.imageinfo])
            points.append(point)
        
        tree = KDTree(points_xy, leaf_size=2)
        _, point_id_nearest = tree.query([[x, y]], k=1)
        point_id_nearest = point_id_nearest[0][0]
        
        point = points[point_id_nearest]
        
        return point
    
    def mouseDoubleClickEvent(self, event):
        xyz = self.__getNearestPoint(event)
        
        if xyz == None:
            return
        
        point = Point(xyz)
        point.selectionInformation = self.selectioninfo
        self.addPointSignal.emit(point)
        
        self.repaintImage()
    
    def mouseReleaseEvent(self, event):
        point = self.__getNearestPointFromSelections(event)
        
        if point == None:
            return
        
        self.selectPointSignal.emit(point)