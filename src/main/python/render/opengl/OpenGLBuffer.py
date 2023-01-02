from __future__ import annotations

import numpy as np

from OpenGL.GL import *

from render.data import Geometry, PrimitiveType
from render.render import Buffer, BufferGroup


class OpenGLBuffer(Buffer):
    def __init__(self, buffer_type):
        super().__init__()
        
        self.primitive_type = PrimitiveType.FLOAT
        self.buffer_type = buffer_type
        self.buffer_id = glGenBuffers(1)
    
    def __del__(self):
        try:
            self.delete()
        except:
            pass
        
    def delete(self):
        glDeleteBuffers(1, [self.buffer_id])
    
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
    
    def clone(self) -> OpenGLBuffer:
        buffer = OpenGLBuffer()
        buffer.buffer_type = self.buffer_type
        buffer.buffer_id = self.buffer_id
        return buffer

class OpenGLBufferGroup:
    @staticmethod
    def createVertexBuffer(primitive_type: PrimitiveType, dimension: int, count_vertices: int, vertices: np.ndarray) -> Buffer:
        buffer: Buffer = OpenGLBufferFactory.VBO()
        buffer.setMetaData(primitive_type, dimension, count_vertices)
        buffer.setData(vertices)
        
        return buffer
    
    @staticmethod
    def createIndexBuffer(primitive_type: PrimitiveType, dimension: int, count_indices: int, indicies: np.ndarray) -> Buffer:
        index_buffer = OpenGLBufferFactory.IBO()
        index_buffer.setMetaData(primitive_type, dimension, count_indices)
        index_buffer.setData(indicies)
        
        return index_buffer
    
    @staticmethod
    def createBufferGroup(geometry: Geometry) -> BufferGroup:
        if geometry == None:
            return
        
        buffers: BufferGroup = BufferGroup()
        
        # Verticies
        for geo_data in geometry.getAllVertices():
            buffer = OpenGLBufferGroup.createVertexBuffer(geo_data.getPrimitiveType(), geo_data.getDimension(), geo_data.getSize(), geo_data.getData())
            buffers.addVertexBuffer(buffer)
        
        # Indicies
        indices = geometry.indices
        if indices != None:
            buffer = OpenGLBufferGroup.createIndexBuffer(indices.getPrimitiveType(), indices.getDimension(), indices.getSize(), indices.getData())
            buffers.setIndexBuffer(buffer)
        
        buffers.geometry_primitive_type = geometry.getPrimitive()
        
        return buffers
    
    @staticmethod
    def reupload_GeometryToMesh(mesh, geometry: Geometry):
        OpenGLBufferGroup.reupload_GeometryToBufferGroup(mesh.buffer_group, geometry)
    
    @staticmethod
    def reupload_GeometryToBufferGroup(buffers: BufferGroup, geometry: Geometry): # TODO delete or create buffers
        vertices = geometry.getAllVertices()
        vertex_buffers = buffers.getVertexBuffers()
        
        # Verticies
        for i in range(len(vertices)):
            geo_data = vertices[i]
            vertex_buffers[i].setMetaData(geo_data.getPrimitiveType(), geo_data.getDimension(), geo_data.getSize())
            vertex_buffers[i].setData(geo_data.getData())
            buffers.count_vertices = vertex_buffers[i].amount
        
        # Indicies
        indices = geometry.indices
        if indices != None:
            buffer = buffers.getIndexBuffer()
            buffer.setMetaData(indices.getPrimitiveType(), indices.getDimension(), indices.getSize())
            buffer.setData(indices.getData())
            buffers.count_indices = buffer.amount
        
        buffers.geometry_primitive_type = geometry.getPrimitive()

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