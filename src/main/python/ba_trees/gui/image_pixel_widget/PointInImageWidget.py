from pathlib import Path

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QTableWidget, QLabel, \
    QHBoxLayout
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
        
        print(camera)
        print(image)
        print(point)
        
        item = QTableWidgetItem(str(image.image_id))
        self.setItem(row, 0, item)
        
        item = QTableWidgetItem("?")
        self.setItem(row, 1, item)
        
        pixmap = QPixmap(str(Path(sub_project._src_image_path, image.name)))
        item = QLabel()
        item.setPixmap(pixmap)
        
        self.setCellWidget(row, 2, item)
        
        item = QTableWidgetItem(image.name)
        self.setItem(row, 3, item)
        
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
