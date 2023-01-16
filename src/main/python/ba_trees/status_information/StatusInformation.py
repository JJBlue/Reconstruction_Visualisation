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
        self.parents: list = []
        if parent != None:
            self.parents.append(parent)
        
        self.status = Status.NOT_STARTED
    
    def setStatus(self, status: Status):
        if self.status == status:
            return
        
        self.status = status
        
        for parent in self.parents:
            EventManager.getEventManager().callAsync(StatusChangedEvent(parent, self))
            
            if parent.getChildsAmount() == parent.getFinishedAmount():
                StatusInformations.removeStatus(parent)

class StatusInformation:
    def __init__(self):
        self.text = "Status Information"
        
        self.childs: list = []
        self.max_amount = 0
    
    def add(self, child: StatusInformationChild):
        child.parents.append(self)
        self.childs.append(child)
        self.max_amount = len(self.childs)
    
    def get(self, index: int):
        return self.childs[index]
    
    def getChildsAmount(self):
        return self.max_amount
    
    def getFinishedAmount(self):
        count = 0
        
        for child in self.childs:
            if child.status == Status.FINISHED:
                count += 1
        
        return count
    
    def isFinished(self):
        return self.getChildsAmount() == self.getFinishedAmount()

class StatusInformations:
    __status: list = set()
    
    @staticmethod
    def addStatus(status: StatusInformation):
        StatusInformations.__status.add(status)
        EventManager.getEventManager().callAsync(AddedStatusEvent(status))
        
        if status.getChildsAmount() == status.getFinishedAmount():
            StatusInformations.removeStatus(status)
    
    @staticmethod
    def removeStatus(status: StatusInformation):
        StatusInformations.__status.discard(status)
        EventManager.getEventManager().callAsync(RemovedStatusEvent(status))
    
    @staticmethod
    def getAlllStatus():
        return StatusInformations.__status