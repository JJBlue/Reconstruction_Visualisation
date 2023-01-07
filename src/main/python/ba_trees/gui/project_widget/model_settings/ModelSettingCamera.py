from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

from ba_trees.gui.project_widget.model_settings.ModelSettingCameraSetup import Ui_settings_tab


class ModelSettingCameraWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_settings_tab()
        self.ui.setupUi(self)

class ModelSettingCamera(QWidget):
    # Model Settings
    modelScaleChanged = pyqtSignal(float)
    
    def __init__(self, *arg):
        super().__init__(*arg)
        
        self.repaint_function = None
        
    def setRenderObject(self, render_object, repaint):
        self.render_object = render_object
        self.repaint_function = repaint
        
        if "sub_project" in self.render_object.values:
            sub_project = self.render_object.values["sub_project"]
            self.modelScaleChanged.emit(sub_project.getCameraScale())
    
    def setModelScale(self, value: float):
        if "sub_project" in self.render_object.values:
            sub_project = self.render_object.values["sub_project"]
            sub_project.reupload(value)
            
            self.repaint_function()