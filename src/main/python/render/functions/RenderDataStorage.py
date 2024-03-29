import threading

from typing import TypeVar, Generic

from render.render import Shader, Mesh, Model, Texture, Buffer


K = TypeVar("K")
V = TypeVar("V")


class RenderDataStorageElements(Generic[K, V]):
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
    
    def has(self, key: K):
        return key in self.storage
    
    def remove(self, key: K) -> bool:
        if not (key in self.storage):
            return True
        
        del self.storage[key]
        
        return True

class RenderDataStorage:
    def __init__(self, local: bool = True):
        self.__local = local
        
        self.__buffers: RenderDataStorageElements[str, Buffer] = RenderDataStorageElements[str, Buffer]()
        self.__shaders: RenderDataStorageElements[str, Shader] = RenderDataStorageElements[str, Shader]()
        self.__textures: RenderDataStorageElements[str, Texture] = RenderDataStorageElements[str, Texture]()
        
        if local:
            self.__meshes: RenderDataStorageElements[str, Mesh] = RenderDataStorageElements[str, Mesh]()
            self.__models: RenderDataStorageElements[str, Model] = RenderDataStorageElements[str, Model]()
    
    # Shareable
    def getBuffers(self) -> RenderDataStorageElements[str, Buffer]:
        return self.__buffers
    
    # Not Shareable (VAO)
    def getMeshes(self) -> RenderDataStorageElements[str, Mesh]:
        if not self.__local:
            raise AssertionError("Not Local")
        return self.__meshes
    
    # Not Shareable (Meshes)
    def getModels(self) -> RenderDataStorageElements[str, Model]:
        if not self.__local:
            raise AssertionError("Not Local")
        return self.__models
    
    # Shareable
    def getShaders(self) -> RenderDataStorageElements[str, Shader]:
        return self.__shaders

    # Shareable
    def getTextures(self) -> RenderDataStorageElements[str, Texture]:
        return self.__textures

class RenderDataStorages:
    __global_storage = RenderDataStorage(local = False)
    __local_storages: dict = {} # Saved Storage from Context
    __thread_context: dict = {}
    
    # Shareable
    @staticmethod
    def getBuffers() -> RenderDataStorageElements[str, Buffer]:
        return RenderDataStorages.__global_storage.getBuffers()
    
    # Shareable
    @staticmethod
    def getShaders() -> RenderDataStorageElements[str, Shader]:
        return RenderDataStorages.__global_storage.getShaders()

    # Shareable
    @staticmethod
    def getTextures() -> RenderDataStorageElements[str, Texture]:
        return RenderDataStorages.__global_storage.getTextures()
    
    @staticmethod
    def getGloablRenderDataStorage():
        return RenderDataStorages.__global_storage
    
    @staticmethod
    def makeCurrent(context):
        thread_id = threading.current_thread().ident
        RenderDataStorages.__thread_context[thread_id] = context
    
    @staticmethod
    def doneCurrent():
        thread_id = threading.current_thread().ident
        
        if thread_id in RenderDataStorages.__thread_context:
            del RenderDataStorages.__thread_context[thread_id]
    
    @staticmethod
    def getLocalRenderDataStorage(context = None) -> RenderDataStorage:
        if context == None:
            thread_id = threading.current_thread().ident
            
            if thread_id in RenderDataStorages.__thread_context:
                context = RenderDataStorages.__thread_context[thread_id]
            else:
                raise AttributeError("No Context found")
        
        if not (context in RenderDataStorages.__local_storages):
            RenderDataStorages.__local_storages[context] = RenderDataStorage(local = True)
        
        return RenderDataStorages.__local_storages[context]
    
    @staticmethod
    def deleteLocalRenderDataStorage(context):
        if not (context in RenderDataStorages.__local_storages):
            return
        del RenderDataStorages.__local_storages[context]