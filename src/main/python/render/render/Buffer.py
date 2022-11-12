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