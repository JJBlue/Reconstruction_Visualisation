from OpenGL.GL import *
from PyQt6.QtCore import QSize
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

from ba_trees.config import Shaders
from render import Shader, ShaderSource, Camera
from render.opengl import OpenGLCamera, OpenGLShader


class RenderWidget(QOpenGLWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        #self.setMinimumSize(640, 480)
        self.setFixedSize(QSize(640, 480))
        
    def initializeGL(self):
        super().initializeGL()
        
        #self.fmt = QOpenGLVersionProfile()
        #self.fmt.setVersion(3, 3)
        #self.fmt.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
        
        # OpenGL
        self.camera: Camera = OpenGLCamera()
        self.shader: Shader = OpenGLShader()
        
        shader_vertex: ShaderSource = Shaders.getShaderFile(GL_VERTEX_SHADER, "default.vert")
        self.shader.addShaderSource(shader_vertex)
        
        
    def paintGL(self):
        super().paintGL()
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)