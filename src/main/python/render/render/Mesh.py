from render.data import Geometry

class Mesh:
    def __init__(self, geometry: Geometry):
        self.geometry = geometry
        pass
    
    def bind(self):
        raise NotImplementedError
    
    def draw(self):
        raise NotImplementedError
    
    def unbind(self):
        raise NotImplementedError
    
    def updateGeometry(self):
        raise NotImplementedError