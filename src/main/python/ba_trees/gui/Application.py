import sys

from PyQt6.QtCore import QCoreApplication, Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow)

from ba_trees.gui.background.opengl.OpenGLData import OpenGLData
from ba_trees.gui.background.qt.QtFunctions import QtFunctions
from ba_trees.gui.main_window import MainWindow


class Application:
    def __init__(self):
        QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
        self.app: QApplication = QApplication(sys.argv)
        
        QtFunctions.init()
        OpenGLData.start()
        
        self.window = MainWindow()
        
        #from ba_trees.gui.selection_widget import SelectionPointsImageWidget
        #widget = SelectionPointsImageWidget()
        #widget.setImage("")
        #self.window.ui.tabs.addTab(widget, "test")
        
        #from ba_trees.gui.project_widget import RenderWidgetTest
        #widget = RenderWidgetTest()
        #self.window.ui.tabs.addTab(widget, "Project")
    
    def getWindows(self) -> QMainWindow:
        return self.window
    
    def getApp(self) -> QApplication:
        return self.app