import subprocess

from pathlib import Path

from ba_trees.gui.treeitem import Event
from ba_trees.gui.treeitem.CustomTreeItem import CustomTreeItem
from PyQt6.QtWidgets import QLabel, QScrollArea
from PyQt6.QtGui import QPixmap


class PathTreeItem(CustomTreeItem):
    def __init__(self, path: Path):
        super().__init__()
        
        self.path: Path = path
        
        self.setEditable(False)
        self.setText(path.parts[-1])
        
        if path.is_dir():
            files = self.path.iterdir()
            for f in files:
                child_item = PathTreeItem(f)
                self.appendRow(child_item)
    
    def doubleClickedEvent(self, event: Event):
        window = event.window
        
        if self.path.exists():
            if self.path.is_file():
                # Open Image
                if self.path.suffix.lower() in [".jpg", ".jpeg", ".jfif", ".pjpeg", ".pjp", ".png", ".bmp", ".raw"]:
                    pixmap: QPixmap = QPixmap(str(self.path))
                    
                    image: QLabel = QLabel()
                    image.setPixmap(pixmap)
                    
                    area: QScrollArea = QScrollArea()
                    area.setWidget(image)
                    
                    window.ui.tabs.addTab(area, self.text())
                else:
                    subprocess.Popen(r'explorer /select,"' + str(self.path) + '"')
            elif self.path.is_dir():
                subprocess.Popen(r'explorer /select,"' + str(self.path) + '"')