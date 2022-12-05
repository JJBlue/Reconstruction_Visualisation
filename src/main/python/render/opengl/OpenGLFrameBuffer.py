from OpenGL.GL import *

from render.render import FrameBuffer, Texture, RenderBuffer
from render.data.RenderBufferData import RenderBufferInternalFormat


class OpenGLFrameBuffer(FrameBuffer):
    def __init__(self):
        super().__init__()
        
        self.color_attachments: list = []
        self.draw_buffers: list = []
        
        self.fbo = glGenFramebuffers(1)
    
    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
    
    def unbind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
    
    def addColorAttachment(self, texture: Texture, is_draw_buffer: bool = True):
        self.bind()
        
        color_attachment_id = len(self.color_attachments)
        self.color_attachments.append(texture)
        
        glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0 + color_attachment_id, texture.getID(), 0)
        
        if is_draw_buffer:
            self.draw_buffers.append(GL_COLOR_ATTACHMENT0 + color_attachment_id)
            glDrawBuffers(len(self.draw_buffers), self.draw_buffers)
        
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print("ERROR: addColorAttachment")
            checked = False
        else:
            checked = True
        
        self.unbind()
        
        return checked
    
    def addRenderBuffer(self, renderbuffer: RenderBuffer):
        self.bind()
        
        attachment = OpenGLFrameBuffer.toOpenGLAttachment(renderbuffer.getInternalFormat(), 0)
        
        if attachment == GL_COLOR_ATTACHMENT0:
            color_attachment_id = len(self.color_attachments)
            self.color_attachments.append(renderbuffer)
            attachment = GL_COLOR_ATTACHMENT0 + color_attachment_id
        
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, attachment, GL_RENDERBUFFER, renderbuffer.getID())
        
        checked = False
        
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print("ERROR: addRenderBuffer")
            checked = False
        else:
            checked = True
        
        self.unbind()
        
        return checked
    
    def getID(self):
        return self.fbo
    
    @staticmethod
    def toOpenGLAttachment(internal_format: RenderBufferInternalFormat, i: int = 0):
        if internal_format == RenderBufferInternalFormat.RED:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.R8:
            return GL_COLOR_ATTACHMENT0 + i
        
        elif internal_format == RenderBufferInternalFormat.RED_INTEGER:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.R8UI:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.R8I:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.R16UI:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.R16I:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.R32UI:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.R32I:
            return GL_COLOR_ATTACHMENT0 + i
        
        elif internal_format == RenderBufferInternalFormat.RG:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.RG8:
            return GL_COLOR_ATTACHMENT0 + i
        
        elif internal_format == RenderBufferInternalFormat.RG_INTEGER:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.RG8UI:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.RG8I:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.RG16UI:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.RG16I:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.RG32UI:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.RG32I:
            return GL_COLOR_ATTACHMENT0 + i
        
        elif internal_format == RenderBufferInternalFormat.RGB:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.RGB8:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.RGB565:
            return GL_COLOR_ATTACHMENT0 + i
        
        elif internal_format == RenderBufferInternalFormat.RGBA:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.RGBA8:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.SRGB8_ALPHA8:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.RGB5_A1:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.RGBA4:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.RGB10_A2:
            return GL_COLOR_ATTACHMENT0 + i
        
        elif internal_format == RenderBufferInternalFormat.RGBA_INTEGER:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.RGBA8UI:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.RGBA8I:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.RGB10_A2UI:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.RGBA16UI:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.RGBA16I:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.RGBA32I:
            return GL_COLOR_ATTACHMENT0 + i
        elif internal_format == RenderBufferInternalFormat.RGBA32UI:
            return GL_COLOR_ATTACHMENT0 + i
        
        elif internal_format == RenderBufferInternalFormat.DEPTH_COMPONENT:
            return GL_DEPTH_ATTACHMENT
        elif internal_format == RenderBufferInternalFormat.DEPTH_COMPONENT16:
            return GL_DEPTH_ATTACHMENT
        elif internal_format == RenderBufferInternalFormat.DEPTH_COMPONENT24:
            return GL_DEPTH_ATTACHMENT
        elif internal_format == RenderBufferInternalFormat.DEPTH_COMPONENT32F:
            return GL_DEPTH_ATTACHMENT
        
        elif internal_format == RenderBufferInternalFormat.DEPTH_STENCIL:
            return GL_DEPTH_STENCIL_ATTACHMENT
        elif internal_format == RenderBufferInternalFormat.DEPTH24_STENCIL8:
            return GL_DEPTH_STENCIL_ATTACHMENT
        elif internal_format == RenderBufferInternalFormat.DEPTH32F_STENCIL8:
            return GL_DEPTH_STENCIL_ATTACHMENT
        
        elif internal_format == RenderBufferInternalFormat.STENCIL:
            return GL_STENCIL_ATTACHMENT
        elif internal_format == RenderBufferInternalFormat.STENCIL_INDEX8:
            return GL_STENCIL_ATTACHMENT
        return None