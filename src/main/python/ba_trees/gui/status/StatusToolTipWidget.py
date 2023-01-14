from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QListWidget, QLabel, QListWidgetItem, QProgressBar)

from ba_trees.gui.background.qt.QtFunctions import QtFunctions
from ba_trees.status_information import StatusInformation
from ba_trees.status_information.StatusEvent import AddedStatusEvent, RemovedStatusEvent
from ba_trees.status_information.StatusInformation import StatusInformations, StatusChangedEvent
from default.eventhandler.EventHandler import EventManager


class StatusToolTipWidget(QWidget):
    def __init__(self, *arg):
        super().__init__(*arg)
        
        layout = QHBoxLayout(self)
        
        self.listview = QListWidget()
        layout.addWidget(self.listview)
        
        self.status_list: dict = {}
        for status in StatusInformations.getAlllStatus():
            item = QListWidgetItem(self.listview)
            self.listview.addItem(item)
            row = StatusBarWidget(status)
            item.setSizeHint(row.minimumSizeHint())
            self.listview.setItemWidget(item, row)
            
            self.status_list[status] = row
        
        
        EventManager.getEventManager().register(StatusChangedEvent, self.statusChanged)
        EventManager.getEventManager().register(AddedStatusEvent, self.addedStatusEvent)
        EventManager.getEventManager().register(RemovedStatusEvent, self.removedStatusEvent)
    
    def __del__(self):
        EventManager.getEventManager().unregister(StatusChangedEvent, self.statusChanged)
        EventManager.getEventManager().unregister(AddedStatusEvent, self.addedStatusEvent)
        EventManager.getEventManager().unregister(RemovedStatusEvent, self.removedStatusEvent)
    
    def statusChanged(self, event):
        if event.information in self.status_list:
            self.status_list[event.information].statusChanged(event)
    
    def addedStatusEvent(self, event):
        def run(event = event):
            item = QListWidgetItem(self.listview)
            self.listview.addItem(item)
            row = StatusBarWidget(event.status, item)
            item.setSizeHint(row.minimumSizeHint())
            self.listview.setItemWidget(item, row)
            
            self.status_list[event.status] = row
        QtFunctions.runLater(run)
    
    def removedStatusEvent(self, event):
        def run(event = event):
            if event.status in self.status_list:
                #self.listview.removeItemWidget(self.status_list[event.status].item)
                row = self.listview.row(self.status_list[event.status].item)
                self.listview.takeItem(row)
                del self.status_list[event.status]
        QtFunctions.runLater(run)
    
    def setMousePosition(self, pos):
        window = self.window()
        
        if window != None:
            w = self.width()
            ww = window.width()
            
            if ww > w:
                if pos.x() + w > ww:
                    pos.setX(ww - w)
            else: # Nothing
                pass
        
        pos.setY(pos.y() - self.height() - 10)
        
        self.setGeometry(pos.x(), pos.y(), self.width(), self.height())

class StatusBarWidget(QWidget):
    def __init__(self, status: StatusInformation, item, parent=None):
        super().__init__(parent)
    
        self.item = item
        self.row = QHBoxLayout()
        
        self.row.addWidget(QLabel(status.text))
        
        self.bar = QProgressBar()
        self.bar.setMaximum(status.getChildsAmount())
        self.bar.setValue(status.getFinishedAmount())
        
        self.row.addWidget(self.bar)

        self.setLayout(self.row)
    
    def statusChanged(self, event):
        def run(event = event):
            self.bar.setValue(event.information.getFinishedAmount())
        QtFunctions.runLater(run)
        