###############
### Imports ###
###############

import sys

from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QIcon

############
### Main ###
############
class Window:
    
    title: str = "Visualisation Software"
    icon: str = "icon.png"
    width: int = 500
    height: int = 500
    
    app: QApplication = None
    widget: QWidget = None
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.widget = QWidget()
        self.widget.setGeometry(50, 50, self.width, self.height)
        self.widget.setWindowTitle(self.title)
        self.widget.setWindowIcon(QIcon(self.icon))
        
    def show(self):
        self.widget.show()
        sys.exit(self.app.exec())