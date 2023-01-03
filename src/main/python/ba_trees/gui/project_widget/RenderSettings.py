from render.functions.RenderDataStorage import RenderDataStorages
from render.opengl import OpenGLProgramm


class RenderObject:
    def __init__(self):
        self.object = None
        
        self.name = ""
        self.visible = True

class RenderCollection(RenderObject):
    def __init__(self):
        super().__init__()
        self.childs = []

class RenderMesh(RenderObject): # Currently Model
    def __init__(self):
        super().__init__()
        self.model = None
        self.shader_id = None
        self.shader = None # TODO Shader Local or Global Context
        
        self.shader_uniforms: dict = {}
    
    def getShader(self):
        if self.shader:
            return self.shader
        
        global_storage = RenderDataStorages.getGloablRenderDataStorage()
        global_shader_storage = global_storage.getShaders()
        
        if self.shader_id and global_shader_storage.has(self.shader_id):
            self.shader = OpenGLProgramm(global_shader_storage.get(self.shader_id))
        
        return self.shader