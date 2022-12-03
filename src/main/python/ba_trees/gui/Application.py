import sys

from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QWidget)

from ba_trees.gui.project_widget import RenderWidget
from ba_trees.gui.main_window import MainWindow


class Application:
    def __init__(self):
        self.app: QApplication = QApplication(sys.argv)
        #self.window = Window()
        self.window = MainWindow()
    
    def getWindows(self) -> QMainWindow:
        return self.window
    
    def getApp(self) -> QApplication:
        return self.app

class Window(QMainWindow): # Old Window
    def __init__(self):
        super().__init__()
        
        self.setGeometry(50, 50, 500, 500)
        self.setWindowTitle("Visualisation Software")
        
        self.render_widget = RenderWidget()
        
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.render_widget)
        
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        
        self.setCentralWidget(self.main_widget)