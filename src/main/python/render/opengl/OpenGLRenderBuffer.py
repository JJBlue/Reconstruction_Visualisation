from OpenGL.GL import *

from render.data import RenderBufferInternalFormat
from render.render import RenderBuffer


class OpenGLRenderBuffer(RenderBuffer):
    def __init__(self, internal_format: RenderBufferInternalFormat, width = 10, height = 10):
        super().__init__(internal_format, -1, -1)
        
        self.id = glGenRenderbuffers(1)
        self.resize(width, height)
    
    def __del__(self):
        print("Delete RenderBuffer")
        try:
            self.delete()
        except:
            pass
        
    def delete(self):
        glDeleteRenderbuffers(1, self.id)
    
    def bind(self):
        glBindRenderbuffer(GL_RENDERBUFFER, self.id)
    
    def unbind(self):
        glBindRenderbuffer(GL_RENDERBUFFER, 0)
    
    def resize(self, width, height):
        if self.width == width and self.height == height:
            return
        
        super().resize(width, height)
        
        self.bind()
        glRenderbufferStorage(GL_RENDERBUFFER, OpenGLRenderBuffer.toOpenGLInternalFormat(self.internal_format), self.width, self.height)
        self.unbind()
    
    def getID(self):
        return self.id
    
    @staticmethod
    def toOpenGLInternalFormat(internal_format: RenderBufferInternalFormat):
        if internal_format == RenderBufferInternalFormat.RED:
            return GL_RED
        elif internal_format == RenderBufferInternalFormat.R8:
            return GL_R8
        
        elif internal_format == RenderBufferInternalFormat.RED_INTEGER:
            return GL_RED_INTEGER
        elif internal_format == RenderBufferInternalFormat.R8UI:
            return GL_R8UI
        elif internal_format == RenderBufferInternalFormat.R8I:
            return GL_R8I
        elif internal_format == RenderBufferInternalFormat.R16UI:
            return GL_R16UI
        elif internal_format == RenderBufferInternalFormat.R16I:
            return GL_R16I
        elif internal_format == RenderBufferInternalFormat.R32UI:
            return GL_R32UI
        elif internal_format == RenderBufferInternalFormat.R32I:
            return GL_R32I
        
        elif internal_format == RenderBufferInternalFormat.RG:
            return GL_RG
        elif internal_format == RenderBufferInternalFormat.RG8:
            return GL_RG8
        
        elif internal_format == RenderBufferInternalFormat.RG_INTEGER:
            return GL_RG_INTEGER
        elif internal_format == RenderBufferInternalFormat.RG8UI:
            return GL_RG8UI
        elif internal_format == RenderBufferInternalFormat.RG8I:
            return GL_RG8I
        elif internal_format == RenderBufferInternalFormat.RG16UI:
            return GL_RG16UI
        elif internal_format == RenderBufferInternalFormat.RG16I:
            return GL_RG16I
        elif internal_format == RenderBufferInternalFormat.RG32UI:
            return GL_RG32UI
        elif internal_format == RenderBufferInternalFormat.RG32I:
            return GL_RG32I
        
        elif internal_format == RenderBufferInternalFormat.RGB:
            return GL_RGB
        elif internal_format == RenderBufferInternalFormat.RGB8:
            return GL_RGB8
        elif internal_format == RenderBufferInternalFormat.RGB565:
            return GL_RGB565
        
        elif internal_format == RenderBufferInternalFormat.RGBA:
            return GL_RGBA
        elif internal_format == RenderBufferInternalFormat.RGBA8:
            return GL_RGBA8
        elif internal_format == RenderBufferInternalFormat.SRGB8_ALPHA8:
            return GL_SRGB8_ALPHA8
        elif internal_format == RenderBufferInternalFormat.RGB5_A1:
            return GL_RGB5_A1
        elif internal_format == RenderBufferInternalFormat.RGBA4:
            return GL_RGBA4
        elif internal_format == RenderBufferInternalFormat.RGB10_A2:
            return GL_RGB10_A2
        
        elif internal_format == RenderBufferInternalFormat.RGBA_INTEGER:
            return GL_RGBA_INTEGER
        elif internal_format == RenderBufferInternalFormat.RGBA8UI:
            return GL_RGBA8UI
        elif internal_format == RenderBufferInternalFormat.RGBA8I:
            return GL_RGBA8I
        elif internal_format == RenderBufferInternalFormat.RGB10_A2UI:
            return GL_RGB10_A2UI
        elif internal_format == RenderBufferInternalFormat.RGBA16UI:
            return GL_RGBA16UI
        elif internal_format == RenderBufferInternalFormat.RGBA16I:
            return GL_RGBA16I
        elif internal_format == RenderBufferInternalFormat.RGBA32I:
            return GL_RGBA32I
        elif internal_format == RenderBufferInternalFormat.RGBA32UI:
            return GL_RGBA32UI
        
        elif internal_format == RenderBufferInternalFormat.DEPTH_COMPONENT:
            return GL_DEPTH_COMPONENT
        elif internal_format == RenderBufferInternalFormat.DEPTH_COMPONENT16:
            return GL_DEPTH_COMPONENT16
        elif internal_format == RenderBufferInternalFormat.DEPTH_COMPONENT24:
            return GL_DEPTH_COMPONENT24
        elif internal_format == RenderBufferInternalFormat.DEPTH_COMPONENT32F:
            return GL_DEPTH_COMPONENT32F
        
        elif internal_format == RenderBufferInternalFormat.DEPTH_STENCIL:
            return GL_DEPTH_STENCIL
        elif internal_format == RenderBufferInternalFormat.DEPTH24_STENCIL8:
            return GL_DEPTH24_STENCIL8
        elif internal_format == RenderBufferInternalFormat.DEPTH32F_STENCIL8:
            return GL_DEPTH32F_STENCIL8
        
        elif internal_format == RenderBufferInternalFormat.STENCIL:
            return GL_STENCIL
        elif internal_format == RenderBufferInternalFormat.STENCIL_INDEX8:
            return GL_STENCIL_INDEX8
        return None