from render.render import Buffer, BufferGroup


class Mesh:
    def __init__(self, buffer_group: BufferGroup = None):
        if buffer_group != None:
            self.buffer_group = buffer_group
            self.update()
        else:
            self.buffer_group = BufferGroup()
    
    def bind(self):
        raise NotImplementedError
    
    def draw(self):
        raise NotImplementedError
    
    def unbind(self):
        raise NotImplementedError
    
    def setBufferGroup(self, buffers: BufferGroup):
        self.buffer_group = buffers
        self.update()
    
    def getBufferGroup(self) -> BufferGroup:
        return self.buffer_group
    
    def update(self):
        raise NotImplementedError
    
    def addVertexBuffer(self, buffer: Buffer):
        self.buffer_group.addVertexBuffer(buffer)
        
        index = len(self.buffer_group.getVertexBuffers())
        self.bindVertexBuffer(index - 1, buffer)
    
    def bindVertexBuffer(self, index: int, buffer: Buffer):
        raise NotImplementedError()
    
    def setIndexBuffer(self, buffer: Buffer):
        self.buffer_group.setIndexBuffer(buffer)
        self.bindIndexBuffer(buffer)
    
    def bindIndexBuffer(self, buffer: Buffer):
        raise NotImplementedError()