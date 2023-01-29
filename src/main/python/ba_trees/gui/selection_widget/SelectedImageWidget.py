from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QPainter, QPen, QColor

from ba_trees.gui.imageview import ImageView
from ba_trees.gui.selection_widget import Image, SelectionInformation

from sklearn.neighbors import KDTree


class SelectedImageWidget(ImageView):
    def __init__(self, *args):
        super().__init__(*args)
        
        self.list_points = []
        
        self.selectioninfo = None
        self.imageinfo = None
    
    def setImage2(self, selection: SelectionInformation, image: Image):
        self.selectioninfo = selection
        self.imageinfo = image
        self.setImage(self.imageinfo.pixmap)
    
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
        x = (self.horizontalScrollBar().value() + pos.x()) / self.scale_factor
        y = (self.verticalScrollBar().value() + pos.y()) / self.scale_factor
        
        
        sub_project = self.selectioninfo.sub_project
        pycolmap_image = sub_project.pycolmap.images[self.imageinfo.image.id]
        camera_id = pycolmap_image.camera_id
        pycolmap_camera = sub_project.pycolmap.cameras[camera_id]
        
        points = []
        points_3D = []
        
        for point3D_id, point3D in sub_project.pycolmap.points3D.items():
            if not pycolmap_image.has_point3D(point3D_id):
                continue
            
            points.append(pycolmap_camera.world_to_image(pycolmap_image.project(point3D.xyz)))
            points_3D.append(point3D)
        
        tree = KDTree(points, leaf_size=2)
        _, point3d_id_nearest = tree.query([[x, y]], k=1)
        point3d_id_nearest = point3d_id_nearest[0][0]
        point3D = points_3D[point3d_id_nearest]
        x, y = pycolmap_camera.world_to_image(pycolmap_image.project(point3D.xyz))
        
        
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