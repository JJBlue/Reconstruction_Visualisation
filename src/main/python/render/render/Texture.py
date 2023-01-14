from render.data import TextureData


class Texture:
    def __init__(self, data: TextureData = None):
        self.image = data
    
    def bind(self, image_id):
        pass
    
    def unbind(self):
        pass
    
    def resize(self, width, height):
        pass
    
    def getID(self):
        return 0