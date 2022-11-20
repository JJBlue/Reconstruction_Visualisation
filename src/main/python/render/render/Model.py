import glm

from render.render import Mesh, Shader


class Model:
    def __init__(self, mesh: Mesh):
        self.mesh: Mesh = mesh
        self.model: glm.mat4 = glm.fmat4x4(1.0)
    
    def bind(self, shader: Shader = None):
        if shader:
            shader.uniform("model", self.model)
        
        self.mesh.bind()
    
    def draw(self):
        self.mesh.draw()
    
    def unbind(self):
        self.mesh.unbind()
    
    def getMesh(self):
        return self.mesh