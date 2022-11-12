from OpenGL.GL import *
from render import ShaderSource, Shader

class OpenGLShader(Shader):
    def __init__(self):
        super().__init__()
        self.program: GLuint = 0
    
    def __del__(self):
        if glIsProgram(self.program):
            glDeleteProgram(self.program)
        
        self.id = 0
    
    def bind(self):
        glUseProgram(self.program)
    
    def unbind(self):
        glUseProgram(0)
    
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