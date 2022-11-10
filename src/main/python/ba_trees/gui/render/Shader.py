from nt import stat
import os

from OpenGL.GL.VERSION.GL_2_0 import glShaderSource, GL_INFO_LOG_LENGTH
from OpenGL.GL.shaders import (compileProgram, compileShader, GL_FALSE,
    glGetShaderiv, GL_COMPILE_STATUS, GL_TRUE, glDeleteShader, glGetProgramiv,
    glGetShaderInfoLog, glGetProgramInfoLog, glAttachShader, GL_LINK_STATUS)
from OpenGL.raw.GL.VERSION.GL_2_0 import (GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, glCreateShader,
    glCompileShader, glIsShader, glIsProgram, glDeleteProgram, glUseProgram,
    glCreateProgram, glLinkProgram)
from OpenGL.raw.GL._types import GLuint, GLint


class ShaderSource:
    def __init__(self):
        self.src: str = None
    
    def getSrc(self) -> str:
        return self.src

class ShaderString(ShaderSource):
    def __init__(self, src: str):
        self.src = src

class ShaderFile(ShaderSource):
    def __init__(self, file: str):
        super().__init__()
        
        self.file = file
        self.modification_time = None
    
    def getSrc(self) -> str:
        if self.__isFileChanged():
           self.__readFile() 
        
        return self.src
    
    def __readFile(self):
        
        
        pass # TODO
    
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
    
    @staticmethod
    def getLogShader(id: GLuint):
        log_length: GLint = 0
        
        if glIsShader(id):
            log_length = glGetShaderiv(id, GL_INFO_LOG_LENGTH)
        elif glIsProgram(id):
            log_length = glGetProgramiv(id, GL_INFO_LOG_LENGTH)
        else:
            pass # TODO error
        
        if log_length <= 0:
            return None
        
        if glIsShader(id):
            return glGetShaderInfoLog(id, log_length, None)
        elif glIsProgram(id):
            return glGetProgramInfoLog(id, GL_INFO_LOG_LENGTH, None)
        
        return None
    
    @staticmethod
    def createShader(type):
        id = glCreateShader(type)
            
        #with open(frag, 'r') as f:
        #    fragment_src = f.readlines()
        #
        #shader = compileProgram(
        #    compileShader(vertex_src, GL_VERTEX_SHADER),
        #    compileShader(fragment_src, GL_FRAGMENT_SHADER)
        #)
        
        glShaderSource(id, 1, source_str, None)
        glCompileShader(id)
        
        compiled: GLuint = glGetShaderiv(id, GL_COMPILE_STATUS)
        
        if compiled != GL_TRUE:
            # print log
            glDeleteShader(id)
        
        return Shader(id)