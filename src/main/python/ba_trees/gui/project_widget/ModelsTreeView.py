import queue

from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QTreeView

from ba_trees.gui.project_widget.RenderSettings import (RenderObject, RenderCollection, RenderModel, RenderMesh)


class ModelsTreeView(QTreeView):
    def __init__(self, root: RenderObject, *args):
        super().__init__(args)
        
        self.updateRoot(root)
    
    def updateRoot(self, root: RenderObject):
        root_tree_model = QStandardItemModel()
        self.root_node = root_tree_model.invisibleRootItem()
        
        
        visit_queue = queue.Queue()
        visit_queue.put([root, self.root_node])
        
        while not visit_queue.empty():
            list_item = visit_queue.get()
            
            render_object = list_item[0]
            parent_item = list_item[1]
            
            
            tree_item = RenderObjectTreeItem(render_object)
            parent_item.appendRow(tree_item)
            
            if isinstance(render_object, RenderCollection):
                for child in render_object.childs:
                    visit_queue.put([child, tree_item])
            elif isinstance(render_object, RenderModel):
                pass
            elif isinstance(render_object, RenderMesh):
                pass
        
        
        self.setModel(root_tree_model)
        # self.expandAll()

class CustomTreeItem(QStandardItem):
    def __init__(self):
        super().__init__()
        
        self.setEditable(False)

class RenderObjectTreeItem(CustomTreeItem):
    def __init__(self, render_object: RenderObject):
        super().__init__()
        
        self.render_object = render_object
        self.setText(render_object.name)