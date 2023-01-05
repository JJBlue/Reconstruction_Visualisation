from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget


class ModelSettingDefault(QWidget):
    modelVisibleChanged = pyqtSignal(bool)
    
    def __init__(self, *arg):
        super().__init__(*arg)
        
        self.repaint_function = None
    
    def setRenderObject(self, render_object, repaint):
        self.render_object = render_object
        self.repaint_function = repaint
        
        self.modelVisibleChanged.emit(render_object.visible)
    
    def setModelVisible(self, value: bool):
        render_object = self.render_object
        if render_object == None:
            return
        
        render_object.visible = value
        self.repaint_function()