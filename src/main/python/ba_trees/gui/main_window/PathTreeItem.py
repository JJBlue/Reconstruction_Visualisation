from pathlib import Path

from PyQt6.QtGui import QStandardItem

class PathTreeItem(QStandardItem):
    def __init__(self, path: Path):
        super().__init__()
        
        self.setEditable(False)
        self.setText(path.parts[-1])