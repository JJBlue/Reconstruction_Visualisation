from pathlib import Path
from threading import Thread

from PIL import Image as Img, ImageDraw
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import (QWidget, QTableWidgetItem, QTableWidget, QLabel, QSizePolicy)
from pycolmap import Camera, Image

from ba_trees.gui.background.qt.QtFunctions import QtFunctions
from ba_trees.gui.image_pixel_widget.PointsInImageSetup import Ui_point_in_image_form


class PointsInImageWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_point_in_image_form()
        self.ui.setupUi(self)
    
    def addImage(self, sub_project, camera: Camera, image: Image):
        self.ui.image_information.setInfo(camera, image)
        self.ui.table.addImage(sub_project, camera, image)

class PointsInImageImageInformationWidget(QTableWidget):
    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
        
        self.setRowCount(11)
        self.setColumnCount(2)
    
    def setInfo(self, camera: Camera, image: Image):
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
        self.setItem(row, 1, QTableWidgetItem(f"{camera.params} ({camera.params_info()})"))
        
        row += 1
        self.setItem(row, 0, QTableWidgetItem("qw, qx, qy, qz"))
        self.setItem(row, 1, QTableWidgetItem(f"{image.qvec}"))
        
        row += 1
        self.setItem(row, 0, QTableWidgetItem("tx, ty, tz"))
        self.setItem(row, 1, QTableWidgetItem(f"{image.tvec}"))
        
        row += 1
        self.setItem(row, 0, QTableWidgetItem("dims")) # Image size
        self.setItem(row, 1, QTableWidgetItem(f"{camera.width}x{camera.height}"))
        
        row += 1
        self.setItem(row, 0, QTableWidgetItem("num_points2D"))
        self.setItem(row, 1, QTableWidgetItem(f"{image.num_points2D()}"))
        
        row += 1
        self.setItem(row, 0, QTableWidgetItem("num_points3D"))
        self.setItem(row, 1, QTableWidgetItem(f"{image.num_points3D()}"))
        
        row += 1
        self.setItem(row, 0, QTableWidgetItem("num_observations"))
        self.setItem(row, 1, QTableWidgetItem(f"{image.num_observations}"))
        
        row += 1
        self.setItem(row, 0, QTableWidgetItem("name"))
        self.setItem(row, 1, QTableWidgetItem(f"{image.name}"))
        
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

class PointsInImageImageWidget(QTableWidget):
    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
        
        self.setRowCount(0)
        self.setColumnCount(1)
    
    def addImage(self, sub_project, camera: Camera, image: Image):
        self.insertRow(self.rowCount())
        row = self.rowCount() - 1
        
        item = QLabel()
        
        def runLater(item=item, row=row):
            with Img.open(Path(sub_project.reconstruction._src_image_path, image.name)) as img:
                width, height = img.size
                draw = ImageDraw.Draw(img)
                
                factor = (width / 1920)
                size = factor * 4
                thickness = 2 if factor < 1 else int(1*factor)
                
                for point2D in image.points2D:
                    uv = point2D.xy
                    draw.arc([uv[0] - size, uv[1] - size, uv[0] + size, uv[1] + size], 0, 360, fill="pink", width=thickness)
                
                for point3D_id, point3D in sub_project.pycolmap.points3D.items():
                    if not image.has_point3D(point3D_id):
                        continue
                    
                    uv = camera.world_to_image(image.project(point3D.xyz))
                    draw.arc([uv[0] - size, uv[1] - size, uv[0] + size, uv[1] + size], 0, 360, fill=128, width=thickness)
                    
                img2 = img.convert("RGBA")
                data = img2.tobytes("raw", "BGRA")
                qimg = QImage(data, img2.width, img2.height, QImage.Format.Format_ARGB32)
                pixmap = QPixmap(qimg)
                
                item.setPixmap(pixmap)
                item.setScaledContents(True)
                item.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
                
                nw = max(0, min(1200, width))
                nh = max(0, min(675, height))
                
                sw = nw / width
                sh = nh / height
                
                scale = sw if sw < sh else sh
            
            def runLaterLater(item=item, row=row, width=width, height=height, scale=scale):                
                self.setColumnWidth(0, int(width * scale))
                self.setRowHeight(0, int(height * scale))
                
                self.setCellWidget(row, 0, item)
            
            QtFunctions.runLater(runLaterLater)
            
        thread = Thread(target=runLater)
        thread.start()
