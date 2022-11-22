import numpy as np

from OpenGL.GL import *

from render.opengl import OpenGLBufferFactory, Types
from render.render import Buffer, Mesh
from render.data import Geometry


class OpenGLMesh(Mesh):
    def __init__(self, geometry: Geometry):
        super().__init__(geometry)
        self.vao = glGenVertexArrays(1)
        
        self.vbos: list[Buffer] = []
        self.ibo: Buffer = None
        
        self.geometry_primitive_type = None
        self.count_vertices = 0
        self.count_indices = 0
        
        self.updateGeometry()
    
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
        if self.ibo != None:
            glDrawElements(self.geometry_primitive_type, self.count_indices, GL_UNSIGNED_INT, None)
        else:
            glDrawArrays(self.geometry_primitive_type, 0, self.count_vertices)
    
    def updateGeometry(self):
        if self.geometry == None:
            return
        
        self.geometry_primitive_type = Types.PrimitivesToOpenGL(self.geometry.getPrimitive())
        self.count_vertices = 0
        self.count_indices = 0
        
        # Verticies
        for geo_data in self.geometry.getAllVertices():
            self.addVertexBuffer(Types.PrimitiveTypeToOpenGL(geo_data.getPrimitiveType()), geo_data.getDimension(), geo_data.getSize(), geo_data.getData())
        
        # Indicies
        indices = self.geometry.indices
        if indices != None:
            self.addIndexBuffer(indices.getSize(), indices.getData())
    
    def addVertexBuffer(self, primitive_type, dimension: int, count_vertices: int, vertices: np.ndarray):
        buffer_id = len(self.vbos)
        
        # Upload to VBO Buffer
        buffer: Buffer = OpenGLBufferFactory.VBO()
        buffer.setData(vertices)
        self.vbos.append(buffer)
        self.count_vertices = count_vertices
        
        # Bind VBO with VAO
        glBindVertexArray(self.vao)
        buffer.bind()
        glEnableVertexAttribArray(buffer_id)
        
        if primitive_type == GL_BYTE or primitive_type == GL_UNSIGNED_BYTE or primitive_type == GL_SHORT or primitive_type == GL_UNSIGNED_SHORT or primitive_type == GL_INT or primitive_type == GL_UNSIGNED_INT:
            glVertexAttribIPointer(buffer_id, dimension, primitive_type, 0, None);
        elif primitive_type == GL_DOUBLE:
            glVertexAttribLPointer(buffer_id, dimension, primitive_type, 0, None);
        else:
            glVertexAttribPointer(buffer_id, dimension, primitive_type, GL_FALSE, 0, None);
        
        glBindVertexArray(0)
        buffer.unbind()
    
    def updateVertexBuffer(self):
        raise NotImplementedError
    
    def addIndexBuffer(self, count_indices:int, indicies: np.ndarray):
        self.ibo = OpenGLBufferFactory.IBO()
        self.ibo.setData(indicies)
        self.count_indices = count_indices
        
        # Upload Data
        glBindVertexArray(self.vao)
        self.ibo.bind()
        glBindVertexArray(0)
        self.ibo.unbind()
    
    def updateIndexBuffer(self):
        raise NotImplementedError