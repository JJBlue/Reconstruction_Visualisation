from __future__ import annotations

import numpy as np
from render.data import PrimitiveType


class Buffer:
    def __init__(self):
        self.primitive_type: PrimitiveType = None
        self.dimension: int = 0
        self.amount: int = 0
    
    def __del__(self):
        pass
    
    def bind(self):
        raise NotImplementedError
    
    def unbind(self):
        raise NotImplementedError
    
    def setData(self, data: np.ndarray, hint):
        raise NotImplementedError
    
    def setSubData(self, data: np.ndarray, offset_bytes: int):
        raise NotImplementedError
    
    def setMetaData(self, primitive_type: PrimitiveType, dimension: int, amount: int):
        self.primitive_type = primitive_type
        self.dimension = dimension
        self.amount = amount
    
    def getPrimitiveType(self):
        return self.primitive_type
    
    def getDimension(self):
        return self.dimension
    
    def getAmount(self):
        return self.amount
    
    def clone(self) -> Buffer:
        buffer = Buffer()
        return buffer

class BufferGroup:
    def __init__(self):
        self.vertex_buffers: list = []
        self.index_buffer: Buffer = None
        
        self.geometry_primitive_type = None
        self.count_indices = 0
        self.count_vertices = 0
    
    def __del__(self):
        pass
    
    def addVertexBuffer(self, buffer: Buffer):
        self.vertex_buffers.append(buffer)
        self.count_vertices = buffer.amount
    
    def getVertexBuffers(self) -> list:
        return self.vertex_buffers
    
    def setIndexBuffer(self, buffer: Buffer):
        self.index_buffer = buffer
        self.count_indices = buffer.amount
    
    def getIndexBuffer(self) -> Buffer:
        return self.index_buffer
    
    def clone(self) -> BufferGroup:
        buffer_group = BufferGroup()
        
        buffer_group.vertex_buffers.extend(self.vertex_buffers)
        buffer_group.index_buffer = self.index_buffer
        
        buffer_group.geometry_primitive_type = self.geometry_primitive_type
        buffer_group.count_indices = self.count_indices
        buffer_group.count_vertices = self.count_vertices
        
        return buffer_group