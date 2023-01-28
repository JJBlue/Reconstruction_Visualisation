from PIL import Image as Img
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QWidget, QListView, QListWidgetItem
from colmap_wrapper.colmap.camera import ImageInformation

from ba_trees.gui.imageview import ImageView
from ba_trees.gui.selection_widget import SelectionInformation
from ba_trees.gui.selection_widget.SelectionPointsInImageWidgetSetup import Ui_Form


class SelectionPointsInImageWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.images = {}
        self.selections = SelectionInformation()
        
    def setProject(self, project):
        subprojects = []
        self.images[project] = subprojects
        
        for sub_project in project.getProjects():
            reconstruction = sub_project.reconstruction
            
            list_images = []
            subprojects.append(list_images)
            
            for image_idx in reconstruction.images.keys():
                image: ImageInformation = reconstruction.images[image_idx]
                    
                with Img.open(image.path) as img:
                    img2 = img.convert("RGBA")
                    data = img2.tobytes("raw", "BGRA")
                    qimg = QImage(data, img2.width, img2.height, QImage.Format.Format_ARGB32)
                    pixmap = QPixmap(qimg)
                        
                    list_images.append(pixmap)
                    self.addImage(pixmap)
    
    def addImage(self, pixmap):
        list_all_images = self.findChild(QListView, "listview_all_images")
        
        item = QListWidgetItem()
        
        image_view = ImageView()
        image_view.setImage(pixmap)
        
        item.setSizeHint(image_view.sizeHint())
        list_all_images.addItem(item)
        list_all_images.setItemWidget(item, image_view)