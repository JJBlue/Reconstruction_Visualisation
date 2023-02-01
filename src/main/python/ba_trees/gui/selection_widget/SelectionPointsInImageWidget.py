from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QListWidgetItem, QListWidget

from ba_trees.gui.imageview import ImageView
from ba_trees.gui.selection_widget import (SelectionInformation, SelectedImageWidget)
from ba_trees.gui.selection_widget.SelectionInformation import Point, Image
from ba_trees.gui.selection_widget.SelectionPointsInImageWidgetSetup import Ui_Form


class SelectionPointsInImageWidget(QWidget):
    pointSelectionChanged = pyqtSignal()
    imageSelectionChanged = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.project = None
        self.selections = []
        
    def setProject(self, project):
        self.project = project
        
        for sub_project in project.getProjects():
            selection = SelectionInformation(sub_project)
            self.selections.append(selection)
        
        selection = self.selections[0]
        for image in selection.images:
            self.__addImage(image)
    
    def __addImage(self, image: Image):
        list_all_images = self.findChild(QListWidget, "listview_all_images")
        
        item = QListWidgetItem()
        
        image_view = ImageView()
        image_view.setBoundWidth(True)
        image_view.disableScroll = True
        image_view.setImage(image.image)
        
        #item.setSizeHint(image_view.sizeHint())
        image_view.boundsHeightFunctions.append(item.setSizeHint)
        
        list_all_images.addItem(item)
        list_all_images.setItemWidget(item, image_view)

    def addPoint(self, point: Point):
        
        pass
    
    def selectPoint(self):
        pass
    
    def selectImageItem(self, item: QListWidgetItem):
        list_all_images = self.findChild(QListWidget, "listview_all_images")
        self.selectImage(list_all_images.row(item))
    
    def selectImage(self, index: int):
        selection = self.selections[0]
        image = selection.images[index]
        
        view = self.findChild(SelectedImageWidget, "selected_image")
        view.setImage2(selection, image)