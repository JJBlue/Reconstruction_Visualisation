import numpy as np

from OpenGL.GL import *

from render.render import Buffer


class OpenGLBuffer(Buffer):
    def __init__(self, buffer_type):
        super().__init__()
        
        self.buffer_type = buffer_type
        self.buffer_id = glGenBuffers(1)
    
    def __del__(self):
        try:
            self.delete()
        except:
            pass
        
    def delete(self):
        glDeleteBuffers(1, self.buffer_id)
    
    def bind(self):
        glBindBuffer(self.buffer_type, self.buffer_id)
    
    def unbind(self):
        glBindBuffer(self.buffer_type, 0)
    
    def setData(self, data: np.ndarray, hint = GL_STATIC_DRAW):
        self.bind()
        glBufferData(self.buffer_type, data.nbytes, data, hint)
        self.unbind()
    
    def setSubData(self, data: np.ndarray, offset_bytes: int):
        self.bind()
        glBufferSubData(self.buffer_type, data.nbytes, offset_bytes, data)
        self.unbind()

class OpenGLBufferFactory:
    @staticmethod
    def VBO():
        return OpenGLBuffer(GL_ARRAY_BUFFER)
    
    @staticmethod
    def IBO():
        return OpenGLBuffer(GL_ELEMENT_ARRAY_BUFFER)

    @staticmethod
    def UBO():
        return OpenGLBuffer(GL_UNIFORM_BUFFER)
    
    @staticmethod
    def SSBO():
        return OpenGLBuffer(GL_SHADER_STORAGE_BUFFER)
    
    @staticmethod
    def TBO():
        return OpenGLBuffer(GL_TEXTURE_BUFFER)
    
    @staticmethod
    def ACBO():
        return OpenGLBuffer(GL_ATOMIC_COUNTER_BUFFER)
    
    @staticmethod
    def DIBO():
        return OpenGLBuffer(GL_DRAW_INDIRECT_BUFFER)
    
    @staticmethod
    def CIBO():
        return OpenGLBuffer(GL_DISPATCH_INDIRECT_BUFFER)
    
    @staticmethod
    def TFBO():
        return OpenGLBuffer(GL_TRANSFORM_FEEDBACK_BUFFER)
    
    @staticmethod
    def PUBO():
        return OpenGLBuffer(GL_PIXEL_UNPACK_BUFFER)
    
    @staticmethod
    def PPBO():
        return OpenGLBuffer(GL_PIXEL_PACK_BUFFER)
    
    @staticmethod
    def CRBO():
        return OpenGLBuffer(GL_COPY_READ_BUFFER)
    
    @staticmethod
    def CWBO():
        return OpenGLBuffer(GL_COPY_WRITE_BUFFER)