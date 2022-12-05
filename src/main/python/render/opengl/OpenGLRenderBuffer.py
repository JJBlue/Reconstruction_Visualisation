from OpenGL.GL import *

class OpenGLRenderBuffer:
    def __init__(self):
        super().__init__()
        
        self.id = glGenRenderbuffers(1)
        
    def bind(self):
        glBindRenderbuffer(self.id)
    
    def unbind(self):
        glBindRenderbuffer(0)