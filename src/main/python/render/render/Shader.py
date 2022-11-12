import os

from nt import stat

class ShaderSource:
    def __init__(self, shader_type):
        self.src: str = None
        self.type = shader_type
    
    def getSrc(self) -> str:
        return self.src
    
    def getType(self):
        return self.type

class ShaderString(ShaderSource):
    def __init__(self, shader_type, src: str):
        super().__init__(shader_type)
        self.src = src

class ShaderFile(ShaderSource):
    def __init__(self, shader_type, file: str):
        super().__init__(shader_type)
        
        self.file = file
        self.modification_time = None
    
    def getSrc(self) -> str:
        if self.__isFileChanged():
            self.__readFile()
        
        return self.src
    
    def __readFile(self):
        lines = None
        
        with open(self.file, "r") as f:
            lines = f.readlines()
        
        self.src = lines
    
    def __isFileChanged(self) -> bool:
        file_stats = os.stat(self.file)
        modification_time = file_stats[stat.ST_MTIME]
        
        if self.modification_time == None:
            self.modification_time = modification_time
            return True
        
        result = self.modification_time < modification_time
        self.modification_time = modification_time
        
        return result

class Shader:
    def __init__(self):
        self.shader_sources: list = []
    
    def __del__(self):
        pass
    
    def bind(self):
        pass
    
    def unbind(self):
        pass
    
    def recompile(self):
        return self.compile()
    
    def compile(self) -> bool:
        return False # TODO exception
    
    def addShaderSource(self, *args):
        for source in args:
            self.shader_sources.append(source)
        self.recompile()