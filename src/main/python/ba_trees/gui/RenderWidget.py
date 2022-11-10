from OpenGL.raw.GL.VERSION.GL_1_0 import (GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, glClear)
from PyQt6.QtCore import QSize
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

from ba_trees.gui.render.Camera import Camera


class RenderWidget(QOpenGLWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        #self.setMinimumSize(640, 480)
        self.setFixedSize(QSize(640, 480))
        self.camera = Camera()
        
    def initializeGL(self):
        super().initializeGL()
        
        #self.fmt = QOpenGLVersionProfile()
        #self.fmt.setVersion(3, 3)
        #self.fmt.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
        
        
        
    def paintGL(self):
        super().paintGL()
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)