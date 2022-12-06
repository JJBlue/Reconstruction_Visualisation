from render.data import ModelData
from render.opengl import OpenGLMesh, OpenGLTexture
from render.render import Model


class OpenGLModel(Model):
    def __init__(self, data: ModelData):
        super().__init__(data)
        
        for geo in data.getGeometries():
            self.meshes.append(OpenGLMesh(geo))
        
        for tex in data.getTextures():
            self.textures.append(OpenGLTexture(tex))