from render.data import TextureData


class Texture:
    def __init__(self, image: TextureData):
        self.image = image
    
    def bind(self, image_id):
        pass
    
    def unbind(self):
        pass
    
    def getID(self):
        return 0