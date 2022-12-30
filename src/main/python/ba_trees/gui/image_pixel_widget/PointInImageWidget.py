from pathlib import Path

from PIL import Image as Img, ImageDraw
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QTableWidget, QLabel
from pycolmap import Camera, Image, Point3D

from ba_trees.gui.image_pixel_widget.PointInImageSetup import Ui_point_in_image_form


class PointInImageWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_point_in_image_form()
        self.ui.setupUi(self)
    
    def addImage(self, sub_project, camera: Camera, image: Image, point: Point3D):
        self.ui.table.addImage(sub_project,camera, image, point)

class PointInImageTableWidget(QTableWidget):
    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
        
        self.setRowCount(0)
        self.setColumnCount(4)
        
        row_data = ["image_id", "reproj_error", "track_location", "image_name"]
        self.setHorizontalHeaderLabels(row_data)
        
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        
        #self.horizontalHeader().setStretchLastSection(True)
        #self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    
    def addImage(self, sub_project, camera: Camera, image: Image, point: Point3D):
        self.insertRow(self.rowCount())
        row = self.rowCount() - 1
        
        item = QTableWidgetItem(str(image.image_id))
        self.setItem(row, 0, item)
        
        item = QTableWidgetItem("?")
        self.setItem(row, 1, item)
        
        item = QLabel()
        uv = camera.world_to_image(image.project(point.xyz))
        
        with Img.open(Path(sub_project._src_image_path, image.name)) as img:
            draw = ImageDraw.Draw(img)
            
            size = 30
            draw.line([uv[0] - size, uv[1] - size, uv[0] + size, uv[1] + size], fill=128, width=5)
            draw.line([uv[0] + size, uv[1] - size, uv[0] - size, uv[1] + size], fill=128, width=5)
            draw.arc([uv[0] - size, uv[1] - size, uv[0] + size, uv[1] + size], 0, 360, fill=128, width=5)
            
            img2 = img.convert("RGBA")
            data = img2.tobytes("raw", "BGRA")
            qimg = QImage(data, img2.width, img2.height, QImage.Format.Format_ARGB32)
            pixmap = QPixmap(qimg)
            item.setPixmap(pixmap)
        
        self.setCellWidget(row, 2, item)
        
        item = QTableWidgetItem(image.name)
        self.setItem(row, 3, item)
        
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
