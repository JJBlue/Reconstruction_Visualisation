from typing import overload

from render.render import Texture, RenderBuffer


class FrameBuffer:
    def __init__(self):
        pass
    
    def bind(self):
        pass
    
    def unbind(self):
        pass
    
    def addTexture(self, texture: Texture):
        raise NotImplementedError()
    
    def addRenderBuffer(self, renderbuffer: RenderBuffer):
        raise NotImplementedError()
    
    @overload
    def setDrawBuffer(self, *args: int):
        raise NotImplementedError()
    
    @overload
    def setDrawBuffer(self, enums: list):
        raise NotImplementedError()
    
    def resize(self, width, height):
        raise NotImplementedError()