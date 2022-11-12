import glm
import numpy as np

from OpenGL.GL import *
from render import ShaderSource, Shader

class OpenGLShader(Shader):
    def __init__(self):
        super().__init__()
        self.program: GLuint = 0
    
    def __del__(self):
        try:
            self.delete()
        except:
            pass
    
    def delete(self):
        if glIsProgram(self.program):
            glDeleteProgram(self.program)
        
        self.id = 0
    
    def bind(self):
        glUseProgram(self.program)
    
    def unbind(self):
        glUseProgram(0)
    
    def uniform(self, name: str, value, count: int = 0):
        location: int = glGetUniformLocation(self.program, name)
        
        if isinstance(value, int):
            glUniform1i(location, value)
            return
        #elif isinstance(value, np.iarray):
        #    glUniform1iv(location, count, value)
        #    return
        
        elif isinstance(value, float):
            glUniform1f(location, value)
            return
        #elif isinstance(value, np.farray):
        #    glUniform1fv(location, count, value)
        #    return
        
        elif isinstance(value, glm.fvec2):
            glUniform2f(location, value.x, value.y)
            return
        elif isinstance(value, glm.fvec3):
            glUniform3f(location, value.x, value.y, value.z)
            return
        elif isinstance(value, glm.fvec4):
            glUniform4f(location, value.x, value.y, value.z, value.w)
            return
        
        elif isinstance(value, glm.ivec2):
            glUniform2i(location, value.x, value.y)
            return
        elif isinstance(value, glm.ivec3):
            glUniform3i(location, value.x, value.y, value.z)
            return
        elif isinstance(value, glm.ivec4):
            glUniform4i(location, value.x, value.y, value.z, value.w)
            return
        
        elif isinstance(value, glm.uvec2):
            glUniform2ui(location, value.x, value.y)
            return
        elif isinstance(value, glm.uvec3):
            glUniform3ui(location, value.x, value.y, value.z)
            return
        elif isinstance(value, glm.uvec4):
            glUniform4ui(location, value.x, value.y, value.z, value.w)
            return
        
        elif isinstance(value, glm.mat3):
            glUniformMatrix3fv(location, 1, GL_FALSE, glm.value_ptr(value))
            return
        elif isinstance(value, glm.mat4):
            glUniformMatrix4fv(location, 1, GL_FALSE, glm.value_ptr(value))
            return
        
        #elif isinstance(value, Texture):
        #    texture.bind(unit)
        #    glUniform1i(location, unit)
        
        raise Exception(f"Type not found: {type(value)}")
    
    def compile(self) -> bool:
        program_new = glCreateProgram()
        
        # Attach Shader
        for source in self.shader_sources:
            shader: GLuint = OpenGLShader.createShader(source)
            if shader == 0:
                glDeleteProgram(program_new)
                return False
            
            glAttachShader(program_new, shader)
        
        
        # Link Program
        glLinkProgram(program_new)
        link_status: GLint = glGetProgramiv(program_new, GL_LINK_STATUS)
        if link_status != GL_TRUE:
            print("Error Link Status")
            glDeleteProgram(program_new)
            return False
        
        # Change Program with old program
        program_old = self.program
        self.program = program_new
        
        if program_old != 0 and glIsProgram(program_old):
            glDeleteProgram(program_old)
        
        return True
    
    @staticmethod
    def getLogShader(shader_id: GLuint):
        if glIsShader(shader_id):
            return glGetShaderInfoLog(shader_id)
        elif glIsProgram(shader_id):
            return glGetProgramInfoLog(shader_id)
        
        return None
    
    @staticmethod
    def createShader(source: ShaderSource) -> GLuint:
        shader_id: GLuint = glCreateShader(source.getType())
        
        glShaderSource(shader_id, source.getSrc())
        glCompileShader(shader_id)
        
        compiled: GLuint = glGetShaderiv(shader_id, GL_COMPILE_STATUS)
        
        if compiled != GL_TRUE:
            print(OpenGLShader.getLogShader(shader_id))
            glDeleteShader(shader_id)
            return 0
        
        return shader_id