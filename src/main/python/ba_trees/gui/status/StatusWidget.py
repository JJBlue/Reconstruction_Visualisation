from PyQt6.QtCore import QEvent
from PyQt6.QtWidgets import QWidget

from ba_trees.gui.status import StatusToolTipWidget


class StatusWidget(QWidget):
    def __init__(self, *arg):
        super().__init__(*arg)
        
        window = self.window()
        
        self.tooltip = StatusToolTipWidget()
        self.tooltip.setParent(window)
        self.tooltip.hide()

    def __del__(self):
        del self.tooltip

    def event(self, event: QEvent):
        if event.type() == QEvent.Type.ToolTip: # QHelpEvent
            window = self.window()

            pos = window.mapFromGlobal(event.globalPos())
            pos.setX(pos.x() - 9)
            pos.setY(pos.y() - 9)
            
            self.tooltip.setMousePosition(pos)
            self.tooltip.show()
            self.tooltip.raise_()
            
            
            event.ignore()
            
            return True
        
        return QWidget.event(self, event)
    
    def leaveEvent(self, *args, **kwargs):
        self.tooltip.hide()
        
        return QWidget.leaveEvent(self, *args, **kwargs)