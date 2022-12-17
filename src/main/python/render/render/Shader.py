from pathlib import Path

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
        lines: list = []
        
        with open(self.file, "r") as f:
            for line in f.readlines():
                lines.append(line)
        
        self.src = ''.join(lines)
    
    def __isFileChanged(self) -> bool:
        file_stats = Path(self.file).stat()
        modification_time = file_stats.st_mtime
        
        if self.modification_time == None:
            self.modification_time = modification_time
            return True
        
        result = self.modification_time < modification_time
        self.modification_time = modification_time
        
        return result

class Shader:
    def __init__(self, source: ShaderSource):
        self.shader_source = source
    
    def __del__(self):
        pass
    
    def recompile(self):
        return self.compile()
    
    def compile(self) -> bool:
        raise NotImplementedError
        return False
    
    def getID(self):
        return 0

class ShaderGroup(Shader):
    def __init__(self, *shaders):
        self.shaders: list = []
        
        for shader in shaders:
            self.shaders.append(shader)
    
    def __del__(self):
        pass
    
    def recompile(self):
        return self.compile()
    
    def compile(self) -> bool:
        result: bool = True
        
        for shader in self.shaders:
            tf = shader.compile()
            
            if not tf:
                result = False
        
        return result
    
    def getShaders(self) -> list:
        return self.shaders