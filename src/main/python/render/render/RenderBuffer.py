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
    
    def resize(self, width, height):
        self.width = width
        self.height = height
    
    def getInternalFormat(self):
        return self.internal_format
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def getSize(self):
        return [self.width, self.height]
    
    def getID(self):
        return 0