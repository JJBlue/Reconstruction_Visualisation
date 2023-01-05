from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QToolBox, QWidget

from ba_trees.gui.project_widget.model_settings.ModelSettingMatrix import ModelSettingMatrixWidget
from ba_trees.gui.project_widget.render_structure.RenderObject import (RenderObject, RenderModel)


class ModelToolBox(QToolBox):
    repaintWorld = pyqtSignal()
    
    def __init__(self, *arg):
        super().__init__(*arg)
        
        self.selected_render_object = None
    
    def selectCurrentModel(self, render_object: RenderObject):
        self.selected_render_object = render_object
        
        current_index = self.currentIndex()
        
        for _ in range(1, self.count()):
            self.removeItem(1)
        
        widget = self.findChild(QWidget, "root_default_settings_tab")
        widget.setRenderObject(render_object, self.__repaintWorld)
        
        if isinstance(render_object, RenderModel):
            model_matrix = render_object.model.model_matrix
            
            page = ModelSettingMatrixWidget()
            widget = page.findChild(QWidget, "root_setting_tab")
            
            widget.setModelMatrix(model_matrix, self.__repaintWorld)
            
            self.addPage("Model Matrix", page)
        
        if current_index < self.count():
            self.setCurrentIndex(current_index)
    
    def __repaintWorld(self):
        self.repaintWorld.emit()
    
    def addPage(self, title: str, widget):
        self.addItem(widget, title)