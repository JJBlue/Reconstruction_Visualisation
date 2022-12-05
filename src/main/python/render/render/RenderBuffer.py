from render.data.RenderBufferData import RenderBufferInternalFormat


class RenderBuffer:
    def __init__(self, internal_format: RenderBufferInternalFormat, width = 10, height = 10):
        self.internal_format: RenderBufferInternalFormat = internal_format
        self.width = width
        self.height = height
    
    def bind(self):
        pass
    
    def unbind(self):
        pass
    
    def getID(self):
        return 0
    
    def resize(self, width, height):
        self.width = width
        self.height = height