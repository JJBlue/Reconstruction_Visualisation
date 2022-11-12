class Mesh:
    def __init__(self):
        pass
    
    def bind(self):
        raise NotImplementedError
    
    def draw(self):
        raise NotImplementedError
    
    def unbind(self):
        raise NotImplementedError