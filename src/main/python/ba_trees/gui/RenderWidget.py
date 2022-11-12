from OpenGL.GL import *
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QSurfaceFormat
from PyQt6.QtOpenGL import QOpenGLVersionProfile
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

from ba_trees.config import Shaders
from render import Shader, ShaderSource, Camera, Cube, Mesh
from render.opengl import OpenGLCamera, OpenGLShader, OpenGLMesh


class RenderWidget(QOpenGLWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        #self.setMinimumSize(640, 480)
        self.setFixedSize(QSize(640, 480))
        
    def initializeGL(self):
        super().initializeGL()
        
        self.fmt = QOpenGLVersionProfile()
        self.fmt.setVersion(4, 3)
        self.fmt.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
        
        # OpenGL
        self.camera: Camera = OpenGLCamera()
        self.shader: Shader = OpenGLShader()
        
        shader_vertex: ShaderSource = Shaders.getShaderFile(GL_VERTEX_SHADER, "default.vert")
        self.shader.addShaderSource(shader_vertex)
        
        shader_fragment: ShaderSource = Shaders.getShaderFile(GL_FRAGMENT_SHADER, "default.frag")
        self.shader.addShaderSource(shader_fragment)
        
        self.cube: Mesh = OpenGLMesh(Cube())
        
        
    def paintGL(self):
        super().paintGL()
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.shader.bind()
        
        self.cube.bind()
        #self.shader.uniform("position", position);
        self.shader.uniform("view", self.camera.getView())
        self.shader.uniform("view_normal", self.camera.getViewNormal())
        self.shader.uniform("proj", self.camera.getProjection())
        self.cube.draw()
        self.cube.unbind()
        
        self.shader.unbind()