from render.render import Shader, Mesh, Model, Texture, Buffer

class OpenGLDataStorage:
    __storage_manger = None
    
    def __init__(self):
        self.storage: dict = {}
    
    @staticmethod
    def getBuffer() -> Buffer:
        raise NotImplementedError()
    
    @staticmethod
    def getMesh() -> Mesh:
        raise NotImplementedError()
    
    @staticmethod
    def getModel() -> Model:
        raise NotImplementedError()
    
    @staticmethod
    def getShader() -> Shader:
        raise NotImplementedError()

    @staticmethod
    def getTexture() -> Texture:
        raise NotImplementedError()
    
    @staticmethod
    def getStorage():
        if OpenGLDataStorage.__storage_manger == None:
            OpenGLDataStorage.__storage_manger = OpenGLDataStorage()
        return OpenGLDataStorage.__storage_manger