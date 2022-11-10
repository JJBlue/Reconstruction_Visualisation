from ba_trees.gui.render import Buffer

class Model:
    def __init__(self):
        self.vertices = None
        self.buffer = Buffer()
    
    def bind(self):
        self.buffer.bind()
    
    def unbind(self):
        self.buffer.unbind()