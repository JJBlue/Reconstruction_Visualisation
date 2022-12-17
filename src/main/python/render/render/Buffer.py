import numpy as np


class Buffer:
    def __init__(self):
        pass
    
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

class BufferGroup:
    def __init__(self):
        self.vertex_buffers: list = []
        self.index_buffer: Buffer = None
    
    def __del__(self):
        pass
    
    def addVertexBuffer(self, buffer: Buffer):
        self.buffers.append(buffer)
    
    def addIndexBuffer(self, buffer: Buffer):
        self.index_buffer = buffer