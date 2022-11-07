###############
### Imports ###
###############

import sys
import numpy as np

from OpenGL import GL
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

############
### Main ###
############
class Application:
    title: str = "Visualisation Software"
    icon: str = "icon.png"
    
    def __init__(self):
        self.app: QApplication = QApplication(sys.argv)

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        
        self.setGeometry(50, 50, 500, 500)
        self.setWindowTitle("Visualisation Software")
        #self.setWindowIcon(QIcon(self.icon))
        
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(QPushButton())
        
        self.glWidget = DrawWidget()
        mainLayout.addWidget(self.glWidget)
        
        self.setLayout(mainLayout)
        
    def show(self):
        self.widget.show()
    
    def getApp(self) -> QApplication:
        return self.app
    
    def getWidget(self) -> QWidget:
        return self.widget
    
class DrawWidget(QOpenGLWidget):
    def __init__(self, parent = None):
        super(DrawWidget, self).__init__(parent)
        self.setMinimumSize(640, 480)
        
    def initializeGL(self):
        vertices = np.array([0.0, 1.0, -1.0, -1.0, 1.0, -1.0], dtype=np.float32)
        
        bufferId = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, bufferId)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_STATIC_DRAW)
        
        GL.glEnableVertexArrayAttrib(0)
        GL.glVertexAttribPointer(0, 2, GL.GL_FLOAT, GL.GL_FALSE, 0, None)
        
    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glLoadIdentity()
        
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)