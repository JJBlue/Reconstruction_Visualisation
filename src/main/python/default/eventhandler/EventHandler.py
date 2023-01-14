from enum import Enum

from concurrent.futures import ThreadPoolExecutor
from typing import Callable

from PyQt6.QtCore import QReadWriteLock


class Event:
    def __init__(self):
        self.cancelled = False

class EventPriority(Enum):
    LOWEST = 0,
    LOW = 1,
    NORMAL = 2,
    HIGH = 3,
    HIGHEST = 4

class EventHandler:
    def __init__(self):
        self.priority = EventPriority.NORMAL # TODO not used
        self.ignoreCancelled = False
        self.function = None



class EventManager:
    manager = None
    
    def __init__(self):
        self.lock_rw = QReadWriteLock()
        self.handlers: dict = {} # Class: list<Callable>
        
        self.executor = ThreadPoolExecutor(max_workers=5)
    
    def __del__(self):
        self.executor.shutdown(wait = False, cancel_futures = True)
    
    def register(self, event_class, function: Callable, event_handler = None):
        if event_handler == None:
            event_handler = EventHandler()
        
        if function == None and event_handler.function == None:
            return
        
        if function != None:
            event_handler.function = function
        
        
        self.lock_rw.lockForWrite()
        
        if not (event_class in self.handlers):
            self.handlers[event_class] = []
        self.handlers[event_class].append(event_handler)
        
        self.lock_rw.unlock()
    
    def unregister(self, event_class, function: Callable):
        self.lock_rw.lockForWrite()
        
        if not (event_class in self.handlers):
            return
        
        removes = []
        
        for handler in self.handlers[event_class]:
            if handler.function == function:
                removes.append(handler)
        
        for handler in removes:
            self.handlers[event_class].remove(handler)
        
        if len(self.handlers[event_class] == 0):
            del self.handlers[event_class]
        
        self.lock_rw.unlock()
    
    def call(self, event: Event):
        event_class = type(event)
        
        self.lock_rw.lockForRead()
        
        if not (event_class in self.handlers):
            return
        
        for handler in self.handlers[event_class]:
            if event.cancelled and not handler.ignoreCancelled:
                continue
            
            handler.function(event)
        
        self.lock_rw.unlock()
    
    def callAsync(self, event: Event):
        self.executor.submit(self.call, event)
    
    @staticmethod
    def getEventManager():
        if EventManager.manager == None: # TODO: Thread unsafe
            EventManager.manager = EventManager()
        return EventManager.manager