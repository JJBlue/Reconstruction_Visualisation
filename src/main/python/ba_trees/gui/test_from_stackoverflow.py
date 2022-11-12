import sys

import numpy as np
from OpenGL import GL
from PyQt6.QtOpenGL import QOpenGLWindow
from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QApplication


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set-up MainWindow
        self.setWindowTitle("ORCAgui")
        self.mainwindow_layout = QHBoxLayout()

        self.show()


class OpenGLWindow(QOpenGLWindow):

    def __init__(self):
        super().__init__()

    def initializeGL(self):
        vertices = np.array([0.0, 1.0, -1.0, -1.0, 1.0, -1.0], dtype=np.float32)

        bufferId = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, bufferId)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_STATIC_DRAW)

        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 2, GL.GL_FLOAT, GL.GL_FALSE, 0, None)

    def paintGL(self):
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
        print("here")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    GLwindow = OpenGLWindow()
    GLwindow.show()
    app.exec()