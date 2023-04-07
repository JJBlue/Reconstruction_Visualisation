from threading import Thread

from PyQt6.QtWidgets import QWidget, QListWidgetItem, QListWidget

from ba_trees.gui.selection_widget import (SelectionInformation, SelectedImageWidget,
    SelectedImagePreviewWidget)
from ba_trees.gui.selection_widget.SelectionInformation import Point, Image
from ba_trees.gui.selection_widget.SelectionPointsInImageWidgetSetup import Ui_Form
from ba_trees.gui.background.qt.QtFunctions import QtFunctions

from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count


class SelectionPointsInImageWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.project = None
        self.selections = []
        self.imageviews = []
        
        self.found_images = []
        
    def setProject(self, project):
        self.project = project
        
        def run():
            for sub_project in project.getProjects():
                selection = SelectionInformation(sub_project)
                self.selections.append(selection)
            
            selection = self.selections[0]
            self.imageviews.clear()
            
            
            n_cores = cpu_count()
            executor = ThreadPoolExecutor(max_workers=n_cores)
            
            for image in selection.images:
                def importRun(image=image):
                    image.getPreviewImage()
                    
                    def qtRun(image=image):
                        self.__addImage(image)
                    QtFunctions.runLater(qtRun)
                
                executor.submit(importRun)
            
            executor.shutdown(wait=True)
        
        thread = Thread(target=run)
        thread.start()
    
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
        
        images = point.points.keys()
        
        for image_view in self.imageviews:
            if not (image_view.imageinfo in images):
                continue
            
            image_view.repaintImage()
    
    def removePoint(self, point: Point):
        images = point.points.keys()
        point.selectionInformation.removePoint(point)
        
        for image_view in self.imageviews:
            if not (image_view.imageinfo in images):
                continue
            
            image_view.repaintImage()
    
    def selectPoint(self, point: Point):
        images = [p.points.keys() for p in point.selectionInformation.selected_points.values()]
        images.append(point.points.keys())
        images = [item for sublist in images for item in sublist]
        
        point.selectionInformation.selectPoint(point)
        
        for image_view in self.imageviews:
            if not (image_view.imageinfo in images):
                continue
            
            image_view.repaintImage()
        
        list_found_images = self.findChild(QListWidget, "listview_point_found_images")
        
        list_found_images.clear()
        self.found_images.clear()
        
        for image in point.points.keys():
            item = QListWidgetItem()
            
            image_view = SelectedImagePreviewWidget()
            image_view.setBoundWidth(True)
            image_view.disableScroll = True
            image_view.setImage2(image)
            
            self.found_images.append(image)
            image_view.boundsHeightFunctions.append(item.setSizeHint)
            
            list_found_images.addItem(item)
            list_found_images.setItemWidget(item, image_view)
        
        view = self.findChild(SelectedImageWidget, "selected_image")
        view.repaintImage()
    
    def selectImageItem(self, item: QListWidgetItem):
        list_all_images = self.findChild(QListWidget, "listview_all_images")
        self.selectImageByIndex(list_all_images.row(item))
    
    def selectImageItem2(self, item: QListWidgetItem):
        list_found_images = self.findChild(QListWidget, "listview_point_found_images")
        self.selectImage(self.found_images[list_found_images.row(item)])
    
    def selectImageByIndex(self, index: int):
        selection = self.selections[0]
        image = selection.images[index]
        self.selectImage(image)
    
    def selectImage(self, image: Image):
        view = self.findChild(SelectedImageWidget, "selected_image")
        view.setImage2(image)