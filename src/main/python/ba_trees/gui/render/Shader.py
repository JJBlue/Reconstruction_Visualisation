from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.raw.GL.VERSION.GL_2_0 import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER

class Shader:
    def __init__(self):
        self.programm = None
    
    @staticmethod
    def createShaderFromFile(vert: str, frag: str):
        with open(vert, 'r') as f:
            vertex_src = f.readlines()
            
        with open(frag, 'r') as f:
            fragment_src = f.readlines()
        
        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )
        
        return