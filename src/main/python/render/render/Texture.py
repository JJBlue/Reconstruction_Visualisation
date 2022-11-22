from render.data import TextureData


class Texture:
    def __init__(self, image: TextureData):
        self.mipmap: bool = True
        self.image = image
    
    def bind(self, image_id):
        pass
    
    def unbind(self):
        pass