from PyQt6.QtWidgets import QMainWindow

class Event:
    def __init__(self, window: QMainWindow, caller):
        self.window = window
        self.caller = caller