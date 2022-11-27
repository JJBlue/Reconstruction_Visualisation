import sys

#from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QPushButton, QMainWindow, QWidget)

from ba_trees.gui.RenderWidget import RenderWidget


class Application:
    title: str = "Visualisation Software"
    icon: str = "icon.png"
    
    def __init__(self):
        self.app: QApplication = QApplication(sys.argv)
        self.window = Window()
    
    def getWindows(self):
        return self.window
    
    def getApp(self):
        return self.app

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(50, 50, 500, 500)
        self.setWindowTitle("Visualisation Software")
        #self.setWindowIcon(QIcon(self.icon))
        
        self.render_widget = RenderWidget()
        self.button = QPushButton()
        
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.render_widget)
        self.main_layout.addWidget(self.button)
        
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        
        self.setCentralWidget(self.main_widget)