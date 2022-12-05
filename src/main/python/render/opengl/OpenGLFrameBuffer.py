from OpenGL.GL import *

from render.render import FrameBuffer, Texture, RenderBuffer


class OpenGLFrameBuffer(FrameBuffer):
    def __init__(self):
        super().__init__()
        
        self.color_attachments: list = []
        
        self.fbo = glGenFramebuffers(1)
    
    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
    
    def unbind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
    
    def addColorAttachment(self, texture: Texture):
        self.bind()
        
        color_attachment_id = len(self.color_attachments)
        self.color_attachments.append(texture)
        
        glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0 + color_attachment_id, texture.getID(), 0)
        
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print("ERROR: addColorAttachment")
            checked = False
        else:
            checked = True
        
        self.unbind()
        
        return checked
    
    def addRenderBuffer(self, renderbuffer: RenderBuffer):
        self.bind()
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, renderbuffer.getID())
        
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