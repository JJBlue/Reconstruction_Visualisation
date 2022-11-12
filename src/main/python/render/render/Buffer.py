class Buffer:
    def __init__(self, buffer_type):
        self.buffer_type = buffer_type
    
    def __del__(self):
        pass
    
    def bind(self):
        raise NotImplementedError
    
    def unbind(self):
        raise NotImplementedError
    
    def setData(self, data: list, size_bytes: int, hint):
        raise NotImplementedError
    
    def setSubData(self, data: list, size_bytes: int, offset_bytes: int):
        raise NotImplementedError