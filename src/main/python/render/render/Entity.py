from render.render import Location

class Entity:
    def __init__(self):
        self.position = Location()
    
    def getPosition(self):
        return self.position