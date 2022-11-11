import os

from nt import stat
from OpenGL.GL import *

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
        self.program: GLuint = 0
        self.id = 0
        
        self.shader_sources: list = []
    
    def __del__(self):
        if glIsProgram(self.id):
            glDeleteProgram(self.id)
        
        self.id = 0
    
    def bind(self):
        glUseProgram(self.program)
    
    def unbind(self):
        glUseProgram(0)
    
    def recompile(self):
        return self.compile()
    
    def compile(self) -> bool:
        program_new = glCreateProgram()
        
        # TODO for shaders
        # TODO type
        shader: GLuint = Shader.createShader(type)
        if shader == 0:
            glDeleteProgram(program_new)
            return False
        
        glAttachShader(program_new, shader)
        
        
        
        glLinkProgram(program_new)
        link_status: GLint = glGetProgramiv(program_new, GL_LINK_STATUS)
        if link_status != GL_TRUE:
            # TODO ERROR
            glDeleteProgram(program_new)
            return False
        
        program_old = self.program
        self.program = program_new
        
        if glIsProgram(program_old):
            glDeleteProgram(program_old)
            
        return True       
    
    def addShaderSource(self, *args):
        for source in args:
            self.shader_sources.append(source)
        self.recompile()
    
    @staticmethod
    def getLogShader(shader_id: GLuint):
        log_length: GLint = 0
        
        if glIsShader(shader_id):
            log_length = glGetShaderiv(shader_id, GL_INFO_LOG_LENGTH)
        elif glIsProgram(shader_id):
            log_length = glGetProgramiv(shader_id, GL_INFO_LOG_LENGTH)
        else:
            print(f"error Shader.getLogShader({shader_id})")
            pass # TODO error
        
        if log_length <= 0:
            return None
        
        if glIsShader(shader_id):
            return glGetShaderInfoLog(shader_id, log_length, None)
        elif glIsProgram(shader_id):
            return glGetProgramInfoLog(shader_id, GL_INFO_LOG_LENGTH, None)
        
        return None
    
    @staticmethod
    def createShader(source: ShaderSource) -> GLuint:
        shader_id: GLuint = glCreateShader(source.getType())
        
        glShaderSource(shader_id, 1, source.getSrc(), None)
        glCompileShader(shader_id)
        
        compiled: GLuint = glGetShaderiv(shader_id, GL_COMPILE_STATUS)
        
        if compiled != GL_TRUE:
            print(Shader.getLogShader(shader_id))
            glDeleteShader(shader_id)
            return 0
        
        return shader_id