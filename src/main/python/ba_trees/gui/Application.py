import sys

from PyQt6.QtCore import QCoreApplication, Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow)

from ba_trees.gui.main_window import MainWindow
from ba_trees.gui.opengl.OpenGLData import OpenGLData


class Application:
    def __init__(self):
        QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
        self.app: QApplication = QApplication(sys.argv)
        
        OpenGLData.start()
        
        self.window = MainWindow()
    
    def getWindows(self) -> QMainWindow:
        return self.window
    
    def getApp(self) -> QApplication:
        return self.app