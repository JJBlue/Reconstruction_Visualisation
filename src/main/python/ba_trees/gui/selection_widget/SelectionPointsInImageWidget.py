from PyQt6.QtWidgets import QWidget, QListWidgetItem, QListWidget

from ba_trees.gui.selection_widget import (SelectionInformation, SelectedImageWidget,
    SelectedImagePreviewWidget)
from ba_trees.gui.selection_widget.SelectionInformation import Point, Image
from ba_trees.gui.selection_widget.SelectionPointsInImageWidgetSetup import Ui_Form


class SelectionPointsInImageWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.project = None
        self.selections = []
        self.imageviews = []
        
    def setProject(self, project):
        self.project = project
        
        for sub_project in project.getProjects():
            selection = SelectionInformation(sub_project)
            self.selections.append(selection)
        
        selection = self.selections[0]
        self.imageviews.clear()
        for image in selection.images:
            self.__addImage(image)
    
    def __addImage(self, image: Image):
        list_all_images = self.findChild(QListWidget, "listview_all_images")
        
        item = QListWidgetItem()
        
        image_view = SelectedImagePreviewWidget()
        image_view.setBoundWidth(True)
        image_view.disableScroll = True
        image_view.setImage2(image)
        self.imageviews.append(image_view)
        
        #item.setSizeHint(image_view.sizeHint())
        image_view.boundsHeightFunctions.append(item.setSizeHint)
        
        list_all_images.addItem(item)
        list_all_images.setItemWidget(item, image_view)

    def addPoint(self, point: Point):
        point.selectionInformation.addPoint(point)
        self.refreshImageForPoint(point)
    
    def refreshImageForPoint(self, point: Point):
        images = point.points.keys()
        
        for image_view in self.imageviews:
            if not (image_view.imageinfo in images):
                continue
            
            image_view.repaintImage()
    
    def selectPoint(self, point: Point):
        point.selectionInformation.selectPoint(point)
        self.refreshImageForPoint(point)
        
        list_found_images = self.findChild(QListWidget, "listview_point_found_images")
        
        list_found_images.clear()
        
        for image in point.points.keys():
            item = QListWidgetItem()
            
            image_view = SelectedImagePreviewWidget()
            image_view.setBoundWidth(True)
            image_view.disableScroll = True
            image_view.setImage2(image)
            
            image_view.boundsHeightFunctions.append(item.setSizeHint)
            
            list_found_images.addItem(item)
            list_found_images.setItemWidget(item, image_view)
        
        view = self.findChild(SelectedImageWidget, "selected_image")
        view.repaintImage()
    
    def selectImageItem(self, item: QListWidgetItem):
        list_all_images = self.findChild(QListWidget, "listview_all_images")
        self.selectImage(list_all_images.row(item))
    
    def selectImage(self, index: int):
        selection = self.selections[0]
        image = selection.images[index]
        
        view = self.findChild(SelectedImageWidget, "selected_image")
        view.setImage2(image)