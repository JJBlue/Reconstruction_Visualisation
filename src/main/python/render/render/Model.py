from render.data import ModelMatrix
from render.render import Shader


class Model:
    def __init__(self):
        self.model_matrix = ModelMatrix()
        
        self.meshes: list = []
        self.textures: list = []
    
    def bind(self, shader: Shader = None):
        if shader:
            shader.uniform("model", self.model_matrix.getModel())
            
            i: int = 0
            for tex in self.textures:
                shader.uniform("texture" + str(i), tex, i)
                i += 1
        
        if len(self.meshes) == 1:
            self.meshes[0].bind()
    
    def draw(self):
        count: int = len(self.meshes)
        
        for mesh in self.meshes:
            if count > 1:
                mesh.bind()
            
            mesh.draw()
            
            if count > 1:
                mesh.unbind()
    
    def unbind(self):
        if len(self.meshes) == 1:
            self.meshes[0].unbind()
    
    def addMeshes(self, *meshes):
        for mesh in meshes:
            self.meshes.append(mesh)
    
    def getMeshes(self) -> list:
        return self.meshes
    
    def addTexture(self, *textures):
        for texture in textures:
            self.textures.append(texture)
    
    def getTextures(self) -> list:
        return self.textures
    
    def setModelMatrix(self, model_matrix):
        self.model_matrix = model_matrix
    
    def getModelMatrix(self) -> ModelMatrix:
        return self.model_matrix