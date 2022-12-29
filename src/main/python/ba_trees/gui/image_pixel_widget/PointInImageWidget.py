from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QTableWidget

from ba_trees.gui.image_pixel_widget.PointInImageSetup import Ui_point_in_image_form


class PointInImageWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_point_in_image_form()
        self.ui.setupUi(self)

class PointInImageTableWidget(QTableWidget):
    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
        
        self.setRowCount(0)
        self.setColumnCount(5)
        
        row_data = ["", "image_id", "reproj_error", "track_location", "image_name"]
        self.setHorizontalHeaderLabels(row_data)
        
        self.insertRow(self.rowCount())
        row = self.rowCount() - 1
        for column in range(5):
            item = QTableWidgetItem(row_data[column])
            self.setItem(row, column, item)
        
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        
        #self.horizontalHeader().setStretchLastSection(True)
        #self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    
    def addImage(self, point, image, camera):
        pass
