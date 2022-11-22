from render.data import Geometry, TextureData, ModelMatrix


class ModelData:
    def __init__(self):
        self.position = ModelMatrix()
        
        self.geometries: list = []
        self.textures: list = []
    
    def addGeometry(self, geometry: Geometry):
        self.geometries.append(geometry)
    
    def getGeometries(self) -> list:
        return self.geometries
    
    def addTexture(self, texture: TextureData):
        self.textures.append(texture)
    
    def getTextures(self) -> list:
        return self.textures
    
    def getModelMatrix(self):
        return self.position