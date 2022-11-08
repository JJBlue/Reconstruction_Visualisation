import ctypes

from OpenGL import GL
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.arrays._arrayconstants import GL_FLOAT, GL_FALSE
from OpenGL.raw.GL.VERSION.GL_1_0 import GL_COLOR_BUFFER_BIT, \
    GL_DEPTH_BUFFER_BIT, GL_LINES, GL_TRIANGLES
from OpenGL.raw.GL.VERSION.GL_1_5 import GL_ARRAY_BUFFER, GL_STATIC_DRAW
from OpenGL.raw.GL.VERSION.GL_2_0 import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QSurfaceFormat
from PyQt6.QtOpenGL import QOpenGLVersionProfile
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

import numpy as np


class RenderWidget(QOpenGLWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        #self.setMinimumSize(640, 480)
        self.setFixedSize(QSize(640, 480))
        
    def initializeGL(self):
        super().initializeGL()
        
        self.fmt = QOpenGLVersionProfile()
        self.fmt.setVersion(3, 3)
        self.fmt.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
        
        #self.make_assets()
        #self.make_shaders()
        
        vertices = (
            -1.0,  1.0, 0.0, 0.0,
             1.0,  1.0, 1.0, 0.0,
             1.0, -1.0, 1.0, 1.0,
            -1.0, -1.0, 0.0, 1.0
        )
        vertices = np.array(vertices, dtype=np.float32)
        
        self.vbo = GL.glGenBuffers(1)
        self.vao = GL.glGenVertexArrays(1)
        
        GL.glBindVertexArray(self.vao)
        GL.glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        
        GL.glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 15, ctypes.c_void_p(0))
        
        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 15, ctypes.c_void_p(8))
        
    def paintGL(self):
        super().paintGL()
        
        GL.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        GL.glBindVertexArray(self.vao)
        GL.glDrawArrays(GL_TRIANGLES, 0, 8)
        
    def make_assets(self):
        pass
    
    def make_shaders(self):
        vertexFilepath = ""
        fragmentFilepath = ""
        
        with open(vertexFilepath, 'r') as f:
            vertex_src = f.readlines()
            
        with open(fragmentFilepath, 'r') as f:
            fragment_src = f.readlines()
        
        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )
        
        return shader