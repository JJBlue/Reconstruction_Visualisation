from PyQt6.QtWidgets import QWidget

from ba_trees.gui.project_widget.ProjectWidgetSetup import Ui_root


class ProjectWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_root()
        self.ui.setupUi(self)