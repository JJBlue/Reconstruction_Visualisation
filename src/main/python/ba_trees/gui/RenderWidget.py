from PyQt6.QtCore import QSize
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

from ba_trees.gui.render import Shader, Camera, ShaderSource, ShaderFile
from OpenGL.GL import *


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
        #self.camera: Camera = Camera()
        self.shader: Shader = Shader()
        
        shader_vertex: ShaderSource = ShaderFile(GL_VERTEX_SHADER, "J:\D\Schule Informatik\git\BA_Trees\src\main\python\ba_trees\gui\render\shader\default.vert")
        self.shader.addShaderSource(shader_vertex)
        
        
    def paintGL(self):
        super().paintGL()
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)