from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

from ba_trees.gui.project_widget.model_settings.ModelSettingMatrixSetup import Ui_settings_tab


class ModelSettingMatrixWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_settings_tab()
        self.ui.setupUi(self)

class ModelSettingMatrix(QWidget):
    # Model Settings
    modelPositionXChanged = pyqtSignal(float)
    modelPositionYChanged = pyqtSignal(float)
    modelPositionZChanged = pyqtSignal(float)
    modelRotationPitchChanged = pyqtSignal(float)
    modelRotationYawChanged = pyqtSignal(float)
    modelRotationRollChanged = pyqtSignal(float)
    modelPositionScaleXChanged = pyqtSignal(float)
    modelPositionScaleYChanged = pyqtSignal(float)
    modelPositionScaleZChanged = pyqtSignal(float)
    
    def __init__(self, *arg):
        super().__init__(*arg)
        
        self.repaint_function = None
        
    def setModelMatrix(self, model_matrix, repaint):
        self.model_matrix = model_matrix
        self.repaint_function = repaint
        
        self.modelPositionXChanged.emit(model_matrix.getX())
        self.modelPositionYChanged.emit(model_matrix.getY())
        self.modelPositionZChanged.emit(model_matrix.getZ())
        self.modelRotationPitchChanged.emit(model_matrix.getPitch())
        self.modelRotationYawChanged.emit(model_matrix.getYaw())
        self.modelRotationRollChanged.emit(model_matrix.getRoll())
    
    def __getModelMatrixFromModel(self):
        return self.model_matrix
    
    def setModelPositionX(self, value: float):
        model_matrix = self.__getModelMatrixFromModel()
        if model_matrix == None:
            return
        
        model_matrix.setX(value)
        self.repaint_function()
    
    def setModelPositionY(self, value: float):
        model_matrix = self.__getModelMatrixFromModel()
        if model_matrix == None:
            return
        
        model_matrix.setY(value)
        self.repaint_function()
    
    def setModelPositionZ(self, value: float):
        model_matrix = self.__getModelMatrixFromModel()
        if model_matrix == None:
            return
        
        model_matrix.setZ(value)
        self.repaint_function()
    
    def setModelPositionPitch(self, value: float):
        model_matrix = self.__getModelMatrixFromModel()
        if model_matrix == None:
            return
        
        model_matrix.setPitch(value)
        self.repaint_function()
    
    def setModelPositionYaw(self, value: float):
        model_matrix = self.__getModelMatrixFromModel()
        if model_matrix == None:
            return
        
        model_matrix.setYaw(value)
        self.repaint_function()
    
    def setModelPositionRoll(self, value: float):
        model_matrix = self.__getModelMatrixFromModel()
        if model_matrix == None:
            return
        
        model_matrix.setRoll(value)
        self.repaint_function()
    
    def setModelPositionScaleX(self, value: float):
        model_matrix = self.__getModelMatrixFromModel()
        if model_matrix == None:
            return
        
        model_matrix.scaleX(value)
        self.repaint_function()
    
    def setModelPositionScaleY(self, value: float):
        model_matrix = self.__getModelMatrixFromModel()
        if model_matrix == None:
            return
        
        model_matrix.scaleY(value)
        self.repaint_function()
    
    def setModelPositionScaleZ(self, value: float):
        model_matrix = self.__getModelMatrixFromModel()
        if model_matrix == None:
            return
        
        model_matrix.scaleZ(value)
        self.repaint_function()