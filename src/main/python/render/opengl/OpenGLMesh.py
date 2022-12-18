from OpenGL.GL import *

from render.opengl.OpenGLTypes import Types
from render.render import Buffer, Mesh
from render.render import BufferGroup


class OpenGLMesh(Mesh):
    def __init__(self, buffer_group: BufferGroup = None):
        self.vao = glGenVertexArrays(1)
        super().__init__(buffer_group)
    
    def __del__(self):
        try:
            self.delete()
        except:
            pass
    
    def delete(self):
        glDeleteVertexArrays(self.vao)
    
    def bind(self):
        glBindVertexArray(self.vao)
    
    def unbind(self):
        glBindVertexArray(0)
        
    def draw(self):
        index_buffer = self.buffer_group.getIndexBuffer()
        
        if index_buffer != None:
            primitive_type = Types.PrimitiveTypeToOpenGL(index_buffer.getPrimitiveType())
            glDrawElements(self.buffer_group.geometry_primitive_type, self.buffer_group.count_indices, primitive_type, None)
        else:
            glDrawArrays(self.buffer_group.geometry_primitive_type, 0, self.buffer_group.count_vertices)
    
    def update(self):
        # Vertex Buffer
        index: int = 0
        for vbo in self.buffer_group.getVertexBuffers():
            self.bindVertexBuffer(index, vbo)
            index += 1
        
        # Index Buffer
        buffer = self.buffer_group.getIndexBuffer()
        if buffer != None:
            self.bindIndexBuffer(buffer)
    
    def bindVertexBuffer(self, index: int, buffer: Buffer):
        # Bind VBO with VAO
        glBindVertexArray(self.vao)
        buffer.bind()
        glEnableVertexAttribArray(index)
        
        primitive_type = Types.PrimitiveTypeToOpenGL(buffer.getPrimitiveType())
        dimension = buffer.dimension
        
        if primitive_type == GL_BYTE or primitive_type == GL_UNSIGNED_BYTE or primitive_type == GL_SHORT or primitive_type == GL_UNSIGNED_SHORT or primitive_type == GL_INT or primitive_type == GL_UNSIGNED_INT:
            glVertexAttribIPointer(index, dimension, primitive_type, 0, None);
        elif primitive_type == GL_DOUBLE:
            glVertexAttribLPointer(index, dimension, primitive_type, 0, None);
        else:
            glVertexAttribPointer(index, dimension, primitive_type, GL_FALSE, 0, None);
        
        glBindVertexArray(0)
        buffer.unbind()
    
    def bindIndexBuffer(self, buffer: Buffer):
        glBindVertexArray(self.vao)
        buffer.bind()
        glBindVertexArray(0)
        buffer.unbind()