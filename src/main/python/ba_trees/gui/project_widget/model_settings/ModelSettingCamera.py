from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

class ModelSettingCameraWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        #self.ui = Ui_settings_tab()
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
        
        self.modelScaleChanged.emit(render_object.visible)
    
    def setModelScale(self, value: float):
        pass