from PyQt6.QtCore import QModelIndex
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtWidgets import QTreeView, QMainWindow

from ba_trees.gui.main_window.treeitem import ProjectTreeItem, Event
from ba_trees.workspace import Workspace


class ProjectTreeView(QTreeView):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
    
    def updateWorkspaceGui(self, workspace: Workspace):
        if workspace == None:
            self.setModel(0, QStandardItemModel())
            return
        
        # Show Projects
        root_tree_model = QStandardItemModel()
        self.root_node = root_tree_model.invisibleRootItem()
        
        for project in workspace.getProjects():
            project_tree_item = ProjectTreeItem(project)
            self.root_node.appendRow(project_tree_item)
        
        self.setModel(root_tree_model)
        # self.expandAll()
    
    def doubleClickedEvent(self, index: QModelIndex):
        current_parent = self.parent()
        while current_parent != None and not isinstance(current_parent, QMainWindow):
            current_parent = current_parent.parent()
        window: QMainWindow = current_parent
        
        item = self.selectedIndexes()[0]
        item.model().itemFromIndex(index).doubleClickedEvent(Event(window, self))