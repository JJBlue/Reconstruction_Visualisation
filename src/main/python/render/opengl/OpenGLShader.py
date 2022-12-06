from OpenGL.GL import *

from render import ShaderSource, Shader


class OpenGLShader(Shader):
    def __init__(self, source: ShaderSource):
        super().__init__(source)
        
        self.shader: GLuint = glCreateShader(source.getType())
        
        glShaderSource(self.shader, source.getSrc())
        glCompileShader(self.shader)
        
        compiled: GLuint = glGetShaderiv(self.shader, GL_COMPILE_STATUS)
        
        if compiled != GL_TRUE:
            print(OpenGLShader.getLog(self.shader))
            self.delete()
            raise AttributeError("Shader could not be created")
    
    def __del__(self):
        try:
            self.delete()
        except:
            pass
    
    def delete(self):
        if glIsShader(self.shader):
            glDeleteShader(self.shader)
        
        self.shader = 0
    
    def bind(self):
        glUseProgram(self.program)
    
    def unbind(self):
        glUseProgram(0)
    
    def compile(self) -> bool:
        # Attach Shader
        for source in self.shader_sources:
            shader: GLuint = OpenGLShader.createShader(source)
            if shader == 0:
                return False
        
        return True
    
    def getID(self):
        return self.shader
    
    @staticmethod
    def getLog(shader_id: GLuint):
        if glIsShader(shader_id):
            return glGetShaderInfoLog(shader_id)
        return None