from default.eventhandler.EventHandler import Event

class StatusEvent(Event):
    def __init__(self):
        super().__init__()

class AddedStatusEvent(StatusEvent):
    def __init__(self, status):
        super().__init__()
        
        self.status = status

class RemovedStatusEvent(StatusEvent):
    def __init__(self, status):
        super().__init__()
        
        self.status = status

class StatusChangedEvent(StatusEvent):
    def __init__(self, information, child):
        super().__init__()
        
        self.information = information
        self.child = child