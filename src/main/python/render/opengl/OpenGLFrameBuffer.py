import numpy as np

from typing import overload

from OpenGL.GL import *

from render.data.RenderBufferData import RenderBufferInternalFormat
from render.render import FrameBuffer, Texture, RenderBuffer


class OpenGLFrameBuffer(FrameBuffer):
    def __init__(self):
        super().__init__()
        
        self.color_attachments: list = []
        
        self.textures: list = []
        self.render_buffers: list = []
        
        self.fbo = glGenFramebuffers(1)
    
    def __del__(self):
        try:
            self.delete()
        except:
            pass
    
    def delete(self):
        glDeleteFramebuffers(1, self.fbo)
    
    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
    
    def unbind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
    
    def addTexture(self, texture: Texture):
        color_attachment_id = len(self.color_attachments)
        self.color_attachments.append(texture)
        self.textures.append(texture)
        
        attachment = GL_COLOR_ATTACHMENT0 + color_attachment_id
        
        glFramebufferTexture(GL_FRAMEBUFFER, attachment, texture.getID(), 0)
        
        checked = False
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print("ERROR: addColorAttachment")
            checked = False
        else:
            checked = True
        
        return checked
    
    def addRenderBuffer(self, renderbuffer: RenderBuffer):
        self.render_buffers.append(renderbuffer)
        
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
        
        return checked
    
    @overload
    def setDrawBuffer(self, *args: int):
        pass
        
    @overload
    def setDrawBuffer(self, *args: str): # Enums
        raise NotImplementedError()
    
    def setDrawBuffer(self, *args):
        draw_buffers: list = []
        
        for arg in args:
            if isinstance(arg, int):
                draw_buffers.append(GL_COLOR_ATTACHMENT0 + arg)
            else:
                raise NotImplementedError()
        
        self.setOpenGLDrawBuffer(draw_buffers)
    
    # GL_NONE, GL_FRONT_LEFT, GL_FRONT_RIGHT, GL_BACK_LEFT, GL_BACK_RIGHT, GL_COLOR_ATTACHMENT
    def setOpenGLDrawBuffer(self, draw_buffers: list):
        glDrawBuffers(len(draw_buffers), draw_buffers)
    
    def resize(self, width, height):
        for render_buffer in self.render_buffers:
            render_buffer.resize(width, height)
        
        for texture in self.textures:
            texture.resize(width, height)
    
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