from PyQt6.QtCore import pyqtSignal, Qt
from sklearn.neighbors import KDTree

from ba_trees.gui.selection_widget import Point
from ba_trees.gui.selection_widget.SelectedImagePreviewWidget import SelectedImagePreviewWidget
from ba_trees.gui.selection_widget.SelectionInformation import Image


class SelectedImageWidget(SelectedImagePreviewWidget):
    addPointSignal = pyqtSignal(Point)
    removePointSignal = pyqtSignal(Point)
    selectPointSignal = pyqtSignal(Point)
    
    def __init__(self, *args):
        super().__init__(*args)
    
    def setImage2(self, imageinfo: Image):
        self.selectioninfo = imageinfo.selectionInformation
        self.imageinfo = imageinfo
        self.setImage(self.imageinfo.getImage())
    
    def __getNearestPoint(self, event):
        if self.image == None:
            return None, None
        
        pos = event.pos()
        x = (self.horizontalScrollBar().value() + pos.x()) / self.scale_factor
        y = (self.verticalScrollBar().value() + pos.y()) / self.scale_factor
        
        sub_project = self.selectioninfo.sub_project
        pycolmap_image = sub_project.pycolmap.images[self.imageinfo.imageinfo.id]
        camera_id = pycolmap_image.camera_id
        pycolmap_camera = sub_project.pycolmap.cameras[camera_id]
        
        points = []
        points3D_id = []
        points_3D = []
        
        for point3D_id, point3D in sub_project.pycolmap.points3D.items():
            if not pycolmap_image.has_point3D(point3D_id):
                continue
            
            points.append(pycolmap_camera.world_to_image(pycolmap_image.project(point3D.xyz)))
            points3D_id.append(point3D_id)
            points_3D.append(point3D)
        
        tree = KDTree(points, leaf_size=2)
        _, point3d_id_nearest = tree.query([[x, y]], k=1)
        point3d_id_nearest = point3d_id_nearest[0][0]
        
        point3D_id = points3D_id[point3d_id_nearest]
        point3D = points_3D[point3d_id_nearest]
        x, y = pycolmap_camera.world_to_image(pycolmap_image.project(point3D.xyz))
        
        if x < 0 or x > self.image.width():
            return None, None
        
        if y < 0 or y > self.image.height():
            return None, None
        
        return point3D_id, point3D
    
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
        _, point3d_id_nearest = tree.query([[x, y]], k=1)
        point3d_id_nearest = point3d_id_nearest[0][0]
        
        point = points[point3d_id_nearest]
        
        return point
    
    def keyReleaseEvent(self, event):
        key = event.key()
        
        if key == Qt.Key.Key_Delete or key == Qt.Key.Key_Backspace:
            for point in self.selectioninfo.selected_points.values():
                self.removePointSignal.emit(point)
        
        self.repaintImage()
    
    def mouseDoubleClickEvent(self, event):
        point3D_id, point3D = self.__getNearestPoint(event)
        
        if point3D_id == None or point3D == None:
            return
        
        point = Point(point3D_id, point3D)
        point.selectionInformation = self.selectioninfo
        self.addPointSignal.emit(point)
        
        self.repaintImage()
    
    def mouseReleaseEvent(self, event):
        point = self.__getNearestPointFromSelections(event)
        
        if point == None:
            return
        
        self.selectPointSignal.emit(point)