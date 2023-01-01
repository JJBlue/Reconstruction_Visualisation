import queue

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget


# Signal only works in QT-Object
class QtFunctions(QWidget):
    __main_object = None
    
    __functions_signal = pyqtSignal()
    __functions = queue.Queue()
    
    @staticmethod
    def init():
        QtFunctions.__main_object = QtFunctions()
        QtFunctions.__main_object.__functions_signal.connect(QtFunctions.__runFunctionInQtThread)
    
    @staticmethod
    def __runFunctionInQtThread():
        function = QtFunctions.__functions.get()
        function()
    
    @staticmethod
    def runLater(function):
        if QtFunctions.__main_object == None:
            raise AttributeError("Please call QtFunctions.init() before")
        
        QtFunctions.__functions.put(function)
        QtFunctions.__main_object.__functions_signal.emit()