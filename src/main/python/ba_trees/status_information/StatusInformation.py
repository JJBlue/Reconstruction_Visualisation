from enum import Enum

from ba_trees.status_information.StatusEvent import StatusChangedEvent, \
    AddedStatusEvent, RemovedStatusEvent
from default.eventhandler.EventHandler import EventManager


class Status(Enum):
    NOT_STARTED = 1
    STARTED = 2
    FINISHED = 3

class StatusInformationChild:
    def __init__(self, parent = None):
        self.parent = parent
        self.status = Status.NOT_STARTED
    
    def setStatus(self, status: Status):
        self.status = status
        EventManager.getEventManager().callAsync(StatusChangedEvent(self.parent, self))
        
        if self.parent != None and self.parent.getChildsAmount() == self.parent.getFinishedAmount():
            StatusInformations.removeStatus(self.parent)

class StatusInformation:
    def __init__(self):
        self.text = "Status Information"
        
        self.childs: list = []
        self.max_amount = 0
    
    def add(self, child: StatusInformationChild):
        child.parent = self
        self.childs.append(child)
        self.max_amount = len(self.childs)
    
    def getChildsAmount(self):
        return self.max_amount
    
    def getFinishedAmount(self):
        count = 0
        
        for child in self.childs:
            if child.status == Status.FINISHED:
                count += 1
        
        return count

class StatusInformations:
    __status: list = []
    
    @staticmethod
    def addStatus(status: StatusInformation):
        StatusInformations.__status.append(status)
        EventManager.getEventManager().callAsync(AddedStatusEvent(status))
        
        if status.getChildsAmount() == status.getFinishedAmount():
            StatusInformations.removeStatus(status)
    
    @staticmethod
    def removeStatus(status: StatusInformation):
        StatusInformations.__status.remove(status)
        EventManager.getEventManager().callAsync(RemovedStatusEvent(status))
    
    @staticmethod
    def getAlllStatus():
        return StatusInformations.__status