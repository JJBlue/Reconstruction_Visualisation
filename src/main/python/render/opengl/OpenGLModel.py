from render.data import ModelData
from render.opengl import OpenGLMesh, OpenGLTexture
from render.render import Model


class OpenGLModel(Model):
    def __init__(self, data: ModelData = None):
        if not data:
            data = ModelData()
        
        super().__init__(data)
        
        self.addGeometries(*data.getGeometries())
        self.addTextureDatas(*data.getTextures())
    
    def addGeometries(self, *geometries):
        for geo in geometries:
            self.addMeshes(OpenGLMesh(geo))
    
    def addMeshes(self, *meshes):
        for mesh in meshes:
            self.meshes.append(mesh)
    
    def addTextureDatas(self, *textures):
        for texture in textures:
            self.addMeshes(OpenGLTexture(texture))
    
    def addTexture(self, *textures):
        for texture in textures:
            self.textures.append(texture)