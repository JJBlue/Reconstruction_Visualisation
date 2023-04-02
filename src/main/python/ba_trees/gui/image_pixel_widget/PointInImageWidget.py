from threading import Thread

from pathlib import Path

from PIL import Image as Img, ImageDraw
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import (QWidget, QTableWidgetItem, QTableWidget, QLabel, QSizePolicy)
from pycolmap import Camera, Image, Point3D

from ba_trees.gui.image_pixel_widget.PointInImageSetup import Ui_point_in_image_form
from ba_trees.gui.background.qt.QtFunctions import QtFunctions


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
    
    def setPoint(self, point: Point3D):
        item = QTableWidgetItem("position")
        self.setItem(0, 0, item)
        
        item = QTableWidgetItem(f"{point.xyz}")
        self.setItem(0, 1, item)
        
        item = QTableWidgetItem("color")
        self.setItem(1, 0, item)
        
        item = QTableWidgetItem(f"{point.color}")
        self.setItem(1, 1, item)
        
        item = QTableWidgetItem("error")
        self.setItem(2, 0, item)
        
        item = QTableWidgetItem(f"{point.error}")
        self.setItem(2, 1, item)
        
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

class PointInImageTableWidget(QTableWidget):
    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
        
        self.setRowCount(0)
        self.setColumnCount(4)
        
        row_data = ["image_id", "reproj_error", "track_location", "image_name"]
        self.setHorizontalHeaderLabels(row_data)
        
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        
        self.setColumnWidth(2, 450)
        
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
        
        # Version 1 (Sometimes broken, need PyColmap to work)
        #uv = camera.world_to_image(image.project(point.xyz))
        
        # Version 2
        import glm
        intrinsics = sub_project.reconstruction.images[image.image_id].intrinsics.K
        
        mat_extrinsics = glm.mat4x4(1.0)
        mat_row = 0
        for array_row in image.projection_matrix():
            column = 0
            for value in array_row:
                mat_extrinsics[column][mat_row] = value
                column += 1
            mat_row += 1
        
        mat_intrinsics = glm.mat3x3(1.0)
        mat_row = 0
        for array_row in intrinsics:
            column = 0
            for value in array_row:
                mat_intrinsics[column][mat_row] = value
                column += 1
            mat_row += 1
        
        mat_intrinsics = glm.mat4x3(mat_intrinsics)
                        
        image_plane = mat_intrinsics @ mat_extrinsics @ glm.vec4(point.xyz[0], point.xyz[1], point.xyz[2], 1.0)
        depth = image_plane.z
        image_uv = glm.vec2(image_plane.xy) / depth
        
        uv = glm.vec2(round(image_uv.x), round(image_uv.y))
        # Version 2 end
        
        def runLater(item=item, row=row, uv=uv):
            with Img.open(Path(sub_project.reconstruction._src_image_path, image.name)) as img:
                width, _ = img.size
                draw = ImageDraw.Draw(img)
                
                factor = (width / 1920)
                size = factor * 30
                thickness = 5 if factor < 1 else int(5*factor)
                
                draw.line([uv[0] - size, uv[1] - size, uv[0] + size, uv[1] + size], fill=128, width=thickness)
                draw.line([uv[0] + size, uv[1] - size, uv[0] - size, uv[1] + size], fill=128, width=thickness)
                draw.arc([uv[0] - size, uv[1] - size, uv[0] + size, uv[1] + size], 0, 360, fill=128, width=thickness)
                
                img2 = img.convert("RGBA")
                data = img2.tobytes("raw", "BGRA")
                scale = float(img2.height) / float(img2.width)
                qimg = QImage(data, img2.width, img2.height, QImage.Format.Format_ARGB32)
                pixmap = QPixmap(qimg)
                
                item.setPixmap(pixmap)
                item.setScaledContents(True)
                item.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
            
            def runLaterLater(item=item, row=row, scale=scale):
                self.setCellWidget(row, 2, item)
                self.setRowHeight(row, int(scale * self.columnWidth(2)))
                
                item = QTableWidgetItem(image.name)
                self.setItem(row, 3, item)
                
            QtFunctions.runLater(runLaterLater)
        
        thread = Thread(target=runLater)
        thread.start()
