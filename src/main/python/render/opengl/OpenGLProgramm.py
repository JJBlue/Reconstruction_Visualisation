from OpenGL.GL import *
import glm

from render.render import Programm, Texture, ShaderGroup


class OpenGLProgramm(Programm):
    def __init__(self, *shaders):
        self.program: GLuint = 0
        super().__init__()
        
        self.program = glCreateProgram()
        
        if shaders:
            self.addShaders(*shaders)
    
    def __del__(self):
        try:
            self.delete()
        except:
            pass
    
    def delete(self):
        if glIsProgram(self.program):
            glDeleteProgram(self.program)
        
        self.program = 0
    
    def bind(self):
        glUseProgram(self.program)
    
    def unbind(self):
        glUseProgram(0)
    
    def uniform(self, name: str, value, arg0: int = 0):
        location: int = glGetUniformLocation(self.program, name)
        
        if isinstance(value, int) or isinstance(value, bool):
            glUniform1i(location, value)
            return
        #elif isinstance(value, np.iarray):
        #    glUniform1iv(location, arg0, value)
        #    return
        
        elif isinstance(value, float):
            glUniform1f(location, value)
            return
        #elif isinstance(value, np.farray):
        #    glUniform1fv(location, arg0, value)
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
        elif isinstance(value, glm.mat3x4):
            glUniformMatrix3x4fv(location, 1, GL_FALSE, glm.value_ptr(value))
            return
        elif isinstance(value, glm.mat4):
            glUniformMatrix4fv(location, 1, GL_FALSE, glm.value_ptr(value))
            return
        elif isinstance(value, glm.mat4x3):
            glUniformMatrix4x3fv(location, 1, GL_FALSE, glm.value_ptr(value))
            return
        
        elif isinstance(value, Texture):
            value.bind(arg0)
            glUniform1i(location, arg0)
            return
        
        raise Exception(f"Type not found: {type(value)}")
    
    def addShaders(self, *shaders) -> bool:
        # Attach Shader
        for shader in shaders:
            if isinstance(shader, ShaderGroup):
                for shader_element in shader.getShaders():
                    glAttachShader(self.program, shader_element.getID())
            else:
                glAttachShader(self.program, shader.getID())
        
        # Link Program
        glLinkProgram(self.program)
        link_status: GLint = glGetProgramiv(self.program, GL_LINK_STATUS)
        if link_status != GL_TRUE:
            print("Error Link Status")
            print(OpenGLProgramm.getLog(self.program))
            glDeleteProgram(self.program)
            return False
        
        return True
    
    @staticmethod
    def getLog(programm_id: GLuint):
        if glIsProgram(programm_id):
            return glGetProgramInfoLog(programm_id)
        return None