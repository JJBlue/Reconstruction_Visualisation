from ba_trees.gui.render import Location

class Entity:
    def __init__(self):
        self.position = Location()
    
    def getPosition(self):
        return self.position