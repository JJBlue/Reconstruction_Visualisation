from OpenGL.GL import *
from PyQt6.QtCore import QSize, Qt, QPoint
from PyQt6.QtGui import QSurfaceFormat
from PyQt6.QtOpenGL import QOpenGLVersionProfile
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

from ba_trees.config import Shaders
from render import Shader, Camera, Cube, CubeDotCloud, Mesh
from render.opengl import OpenGLCamera, OpenGLShader, OpenGLMesh


class RenderWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        
        # Widget Settings
        #self.setMinimumSize(640, 480)
        self.setFixedSize(QSize(1920, 1080))
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus) # Must be set for keyPressEvent to work
        self.setMouseTracking(True) # To track Mouse Move without click event
        
        # GL Settings
        self.camera: Camera = None
        self.shader: Shader = None
        
        self.camera_speed: float = 0.1
        
        self.mouse_pressed: bool = False
        self.mouse_x: float = -1
        self.mouse_y: float = -1
    
    def keyPressEvent(self, event):
        if self.camera != None:
            key = event.key()

            if key == Qt.Key.Key_W:
                self.camera.forward(self.camera_speed)
                self.repaint()
            elif key == Qt.Key.Key_S:
                self.camera.backward(self.camera_speed)
                self.repaint()
            elif key == Qt.Key.Key_A:
                self.camera.leftward(self.camera_speed)
                self.repaint()
            elif key == Qt.Key.Key_D:
                self.camera.rightward(self.camera_speed)
                self.repaint()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_pressed = True

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_pressed = False
            self.mouse_x: float = -1
            self.mouse_y: float = -1

    def mouseMoveEvent(self, event):
        if self.mouse_pressed:
            pos: QPoint = event.position()

            if self.mouse_x != -1:
                degree: float = pos.x() - self.mouse_x
                self.camera.yaw(degree * -1.0 / 10.0)

                degree: float = pos.y() - self.mouse_y
                self.camera.pitch(degree * -1.0 / 10.0)
                
                self.repaint()
            
            self.mouse_x = pos.x()
            self.mouse_y = pos.y()

    def initializeGL(self):
        super().initializeGL()
        
        self.fmt = QOpenGLVersionProfile()
        self.fmt.setVersion(4, 3)
        self.fmt.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
        
        # OpenGL
        self.camera = OpenGLCamera()
        self.shader = OpenGLShader()
        
        #self.shader.addShaderSource(
        #    Shaders.getShaderFile(GL_VERTEX_SHADER, "default.vert"),
        #    Shaders.getShaderFile(GL_FRAGMENT_SHADER, "default.frag")
        #)
        
        #self.cube: Mesh = OpenGLMesh(Cube())
        
        self.shader.addShaderSource(
            Shaders.getShaderFile(GL_VERTEX_SHADER, "point_cloud.vert"),
            Shaders.getShaderFile(GL_FRAGMENT_SHADER, "point_cloud.frag")
        )
        
        self.cube: Mesh = OpenGLMesh(CubeDotCloud())
        
        
    def paintGL(self):
        super().paintGL()
        
        # Update Objects
        self.camera.update()
        
        # Clear OpenGL Frame
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Enable OpenGL Settings
        glFrontFace(GL_CCW)
        glCullFace(GL_BACK)
        glEnable(GL_CULL_FACE)
        
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE);
        
        glEnable(GL_DEPTH_TEST);
        
        # Draw
        self.shader.bind()
        
        self.cube.bind()
        #self.shader.uniform("position", position);
        self.shader.uniform("view", self.camera.getView())
        self.shader.uniform("view_normal", self.camera.getViewNormal())
        self.shader.uniform("proj", self.camera.getProjection())
        self.cube.draw()
        self.cube.unbind()
        
        self.shader.unbind()
        
        # Disable OpenGL Settings
        glDisable(GL_CULL_FACE)
        glDisable(GL_VERTEX_PROGRAM_POINT_SIZE);
        glDisable(GL_DEPTH_TEST);