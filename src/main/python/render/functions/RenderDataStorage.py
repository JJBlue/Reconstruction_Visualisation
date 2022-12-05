from typing import TypeVar, Generic

K = TypeVar("K")
V = TypeVar("V")

from render.render import Shader, Mesh, Model, Texture, Buffer

class OpenGLDataStorageElements(Generic[K, V]):
    def __init__(self):
        self.storage: dict[K, V] = {}
    
    def get(self, key: K) -> V:
        if not (key in self.storage):
            return None
        return self.storage[key]
    
    def put(self, key: K, value: V):
        if key in self.storage:
            raise AssertionError(f"Name {str} already in use")
        
        self.storage[key] = value

class OpenGLDataStorage:
    __buffers: OpenGLDataStorageElements[str, Buffer] = OpenGLDataStorageElements[str, Buffer]()
    __meshes: OpenGLDataStorageElements[str, Mesh] = OpenGLDataStorageElements[str, Mesh]()
    __models: OpenGLDataStorageElements[str, Model] = OpenGLDataStorageElements[str, Model]()
    __shaders: OpenGLDataStorageElements[str, Shader] = OpenGLDataStorageElements[str, Shader]()
    __textures: OpenGLDataStorageElements[str, Texture] = OpenGLDataStorageElements[str, Texture]()
    
    # Shareable
    @staticmethod
    def getBuffers() -> OpenGLDataStorageElements[str, Buffer]:
        return OpenGLDataStorage.__buffers
    
    # Not Shareable (VAO)
    @staticmethod
    def getMeshes() -> OpenGLDataStorageElements[str, Mesh]:
        return OpenGLDataStorage.__meshes
    
    # Not Shareable (Meshes)
    @staticmethod
    def getModels() -> OpenGLDataStorageElements[str, Model]:
        return OpenGLDataStorage.__models
    
    # Shareable
    @staticmethod
    def getShaders() -> OpenGLDataStorageElements[str, Shader]:
        return OpenGLDataStorage.__shaders

    # Shareable
    @staticmethod
    def getTextures() -> OpenGLDataStorageElements[str, Texture]:
        return OpenGLDataStorage.__textures

class OpenGLLocalDataStorage():
    def __init__(self):
        pass