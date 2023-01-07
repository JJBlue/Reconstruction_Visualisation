from typing import Callable

from render.functions.RenderDataStorage import RenderDataStorages
from render.opengl import OpenGLProgramm
    
    
class RenderObject:
    def __init__(self):
        self.object = None
        
        self.name = ""
        self.visible = True
        
        self.settings_gui: list = [] # Tabs
        self.values: dict = {} # Some unessacry Values (not be used for rendering, only for infos)
    
    def isVisible(self):
        if isinstance(self.visible, Callable):
            return self.visible()
        return self.visible

class RenderCollection(RenderObject):
    def __init__(self):
        super().__init__()
        self.childs = []

class RenderShaderObject(RenderObject):
    def __init__(self):
        super().__init__()
        
        self.shader_id = None
        self.shader = None
        
        self.shader_uniforms: dict = {}

    def getShader(self):
        if self.shader:
            return self.shader
        
        global_storage = RenderDataStorages.getGloablRenderDataStorage()
        global_shader_storage = global_storage.getShaders()
        
        if self.shader_id and global_shader_storage.has(self.shader_id):
            self.shader = OpenGLProgramm(global_shader_storage.get(self.shader_id))
        
        return self.shader
    
    def setShaderUniforms(self, shader = None):
        if shader == None:
            shader = self.getShader()
        
        if shader == None:
            return
        
        for name, value in self.shader_uniforms.items():
            if isinstance(value, Callable):
                value = value()
            
            shader.uniform(name, value)

class RenderModel(RenderShaderObject):
    def __init__(self):
        super().__init__()
        
        self.model = None
        self.shader_id = None
        self.shader = None
        
        self.shader_uniforms: dict = {}
    
    def getModel(self):
        return self.model
    
class RenderMesh(RenderShaderObject):
    def __init__(self):
        super().__init__()
        
        self.mesh = None