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
        
        # TODO for shaders
        # TODO type
        shader: GLuint = OpenGLShader.createShader(type)
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
            print(OpenGLShader.getLogShader(shader_id))
            glDeleteShader(shader_id)
            return 0
        
        return shader_id