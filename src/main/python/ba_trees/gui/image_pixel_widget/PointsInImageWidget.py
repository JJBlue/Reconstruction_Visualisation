from pathlib import Path

from PIL import Image as Img, ImageDraw
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import (QWidget, QTableWidgetItem, QTableWidget, QLabel, QSizePolicy)
from pycolmap import Camera, Image, Point3D

from ba_trees.gui.image_pixel_widget.PointInImageSetup import Ui_point_in_image_form


class PointInImageWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_point_in_image_form()
        self.ui.setupUi(self)
    
    def addImage(self, sub_project, camera: Camera, image: Image, point: Point3D):
        self.ui.point_information.setPoint(point)
        self.ui.table.addImage(sub_project,camera, image, point)

class PointInImagePointInformationWidget(QTableWidget):
    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
        
        self.setRowCount(3)
        self.setColumnCount(2)
    
    def setPoint(self, camera: Camera, image: Image):
        row = 0
        self.setItem(row, 0, QTableWidgetItem("image_id"))
        self.setItem(row, 1, QTableWidgetItem(f"{image.image_id}"))
        
        row += 1
        self.setItem(row, 0, QTableWidgetItem("camera_id"))
        self.setItem(row, 1, QTableWidgetItem(f"{image.camera_id}"))
        
        row += 1
        self.setItem(row, 0, QTableWidgetItem("camera_model"))
        self.setItem(row, 1, QTableWidgetItem(f"{camera.model_name}"))
        
        row += 1
        self.setItem(row, 0, QTableWidgetItem("camera_params"))
        self.setItem(row, 1, QTableWidgetItem(f"{camera.params_info}"))
        
        row += 1
        self.setItem(row, 0, QTableWidgetItem("qw, qx, qy, qz"))
        self.setItem(row, 1, QTableWidgetItem(f"{image.qvec}"))
        
        row += 1
        self.setItem(row, 0, QTableWidgetItem("tx, ty, tz"))
        self.setItem(row, 1, QTableWidgetItem(f"{image.tvec}"))
        
        row += 1
        self.setItem(row, 0, QTableWidgetItem("dims")) # Image size
        self.setItem(row, 1, QTableWidgetItem(f"?"))
        
        row += 1
        self.setItem(row, 0, QTableWidgetItem("num_points2D"))
        self.setItem(row, 1, QTableWidgetItem(f"{image.num_points2D}"))
        
        row += 1
        self.setItem(row, 0, QTableWidgetItem("num_points3D"))
        self.setItem(row, 1, QTableWidgetItem(f"{image.num_points3D}"))
        
        row += 1
        self.setItem(row, 0, QTableWidgetItem("num_observations"))
        self.setItem(row, 1, QTableWidgetItem(f"{image.num_observations}"))
        
        row += 1
        self.setItem(row, 0, QTableWidgetItem("name"))
        self.setItem(row, 1, QTableWidgetItem(f"{image.name}"))
        
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

class PointInImageTableWidget(QTableWidget):
    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
        
        self.setRowCount(0)
        self.setColumnCount(1)
    
    def addImage(self, sub_project, camera: Camera, image: Image):
        self.insertRow(self.rowCount())
        row = self.rowCount() - 1
        
        item = QLabel()
        uv = camera.world_to_image(image.project(point.xyz))
        
        with Img.open(Path(sub_project._src_image_path, image.name)) as img:
            draw = ImageDraw.Draw(img)
            
            size = 4
            draw.arc([uv[0] - size, uv[1] - size, uv[0] + size, uv[1] + size], 0, 360, fill=128, width=5)
            
            img2 = img.convert("RGBA")
            data = img2.tobytes("raw", "BGRA")
            qimg = QImage(data, img2.width, img2.height, QImage.Format.Format_ARGB32)
            pixmap = QPixmap(qimg)
            
            item.setPixmap(pixmap)
            item.setScaledContents(True)
            item.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        
        self.setCellWidget(row, 0, item)
        
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
