### Not used yet, was a little idea

from enum import Enum

class RenderType(Enum):
    EMPTY = 0
    OpenGL = 1

class RenderObjectSetting:
    pass

class RenderModule():
    def __init__(self):
        __render_class: dict = {}
    
    def set(self, classy, obj: object):
        self.__render_class[classy] = obj
    
    def get(self, classy) -> object:
        if not (classy in RenderModule.__render_class):
            return None
        
        return RenderModule.__render_class[type]

class RenderModules():
    __render_modules: dict = {}
    
    @staticmethod
    def set(render_type: RenderType, classy):
        if not (type in RenderModules.__render_modules):
            RenderModules.__render_modules[render_type] = RenderModule()
        
        RenderModules.__render_modules[render_type].set(classy)
    
    @staticmethod
    def get(render_type: RenderType) -> RenderModule:
        if not (render_type in RenderModules.__render_modules):
            return None
        
        return RenderModules.__render_modules[render_type]
    
    @staticmethod
    def getObject(render_type: RenderType, classy):
        rm: RenderModule = RenderModules.get(render_type)
        
        if not rm:
            return None
        
        return rm.get(classy)