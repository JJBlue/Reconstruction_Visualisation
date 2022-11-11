from OpenGL.GL import *


class Buffer:
    def __init__(self, buffer_type):
        self.id = glGenBuffers(1)
        self.buffer_type = buffer_type
    
    def __del__(self):
        glDeleteBuffers(1, self.id)
    
    def bind(self):
        glBindBuffer(self.buffer_type, self.id)
    
    def unbind(self):
        glBindBuffer(self.buffer_type, 0)
    
    def setData(self, data: list, size_bytes: int, hint = GL_STATIC_DRAW):
        self.bind()
        glBufferData(self.buffer_type, size_bytes, data, hint)
        self.unbind()
    
    def setSubData(self, data: list, size_bytes: int, offset_bytes: int):
        self.bind()
        glBufferSubData(self.buffer_type, offset_bytes, size_bytes, data)
        self.unbind()

#VBO  = Buffer(GL_ARRAY_BUFFER)
#IBO  = Buffer(GL_ELEMENT_ARRAY_BUFFER)
#UBO  = Buffer(GL_UNIFORM_BUFFER)
#SSBO = Buffer(GL_SHADER_STORAGE_BUFFER)
#TBO  = Buffer(GL_TEXTURE_BUFFER)
#QBO  = Buffer(GL_QUERY_BUFFER)
#ACBO = Buffer(GL_ATOMIC_COUNTER_BUFFER)
#DIBO = Buffer(GL_DRAW_INDIRECT_BUFFER)
#CIBO = Buffer(GL_DISPATCH_INDIRECT_BUFFER)
#TFBO = Buffer(GL_TRANSFORM_FEEDBACK_BUFFER)
#PUBO = Buffer(GL_PIXEL_UNPACK_BUFFER)
#PPBO = Buffer(GL_PIXEL_PACK_BUFFER)
#CRBO = Buffer(GL_COPY_READ_BUFFER)
#CWBO = Buffer(GL_COPY_WRITE_BUFFER)