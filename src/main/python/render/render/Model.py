from render.render import Buffer

class Model:
    def __init__(self, buffer: Buffer):
        self.vertices = None
        self.buffer: Buffer = buffer
    
    def bind(self):
        self.buffer.bind()
    
    def unbind(self):
        self.buffer.unbind()