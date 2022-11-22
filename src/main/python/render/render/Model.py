from render.data import ModelData
from render.render import Shader, Mesh


class Model:
    def __init__(self, data: ModelData):
        self.data = data
        #self.meshes: list = []
        self.mesh: Mesh = None
        self.textures: list = []
    
    def bind(self, shader: Shader = None):
        if shader:
            shader.uniform("model", self.position.getModel())
            
            i: int = 0
            for tex in self.textures:
                tex.bind(i)
                i += 1
        
        self.mesh.bind()
    
    def draw(self):
        self.mesh.draw()
    
    def unbind(self):
        self.mesh.unbind()
    
    def getMesh(self):
        return self.mesh