from PyQt6.QtGui import QStandardItem

from ba_trees.gui.treeitem import Event


class CustomTreeItem(QStandardItem):
    def doubleClickedEvent(self, event: Event):
        pass