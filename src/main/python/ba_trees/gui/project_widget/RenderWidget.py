from OpenGL.GL import *
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QSurfaceFormat
from PyQt6.QtOpenGL import QOpenGLVersionProfile
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

from ba_trees.config.Shaders import Shaders
from ba_trees.workspace import Project
from render.data import Geometry, CoordinateSystem
from render.opengl import OpenGLCamera, OpenGLShader, OpenGLMesh, OpenGLModel
from render.render import Shader, Camera, Model


class RenderWidget(QOpenGLWidget):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        
        # Widget Settings
        #self.setFixedSize(QSize(1920, 1080))
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus) # Must be set for keyPressEvent to work
        self.setMouseTracking(True) # To track Mouse Move without click event
        
        # GL Settings
        self.camera: Camera = None
        self.shader: Shader = None
        
        self.camera_speed: float = 0.1
        
        self.mouse_pressed: bool = False
        self.mouse_x: float = -1
        self.mouse_y: float = -1
        
        self.projects: list = []
        self.opengl_project_data: list = []
        
        self.setting_show_coordinate_system = False
    
    ##########################
    ### Mouse and Keyboard ###
    ##########################
    
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
        if event.button() == Qt.MouseButton.LeftButton and self.camera != None:
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

    ###########################
    ### QT Designer Methods ###
    ###########################
    
    def change_point_cloud_point_size(self, size: int):
        pass
    
    def show_coordinate_system(self, value: bool):
        self.setting_show_coordinate_system = value
        self.repaint()
    
    ###############
    ### Methods ###
    ###############
    
    def addProject(self, project: Project):
        self.projects.append(project)
        
        data: dict = {}
        
        point_cloud: Model = OpenGLModel(project.getModel())
        data["point_cloud"] = point_cloud
        
        #self.model_image: Model = OpenGLModel(self.project.getImages()[0])
        
        self.opengl_project_data.append(data)
    
    ##############
    ### OpenGL ###
    ##############
    
    def initializeGL(self):
        super().initializeGL()
        
        self.fmt = QOpenGLVersionProfile()
        self.fmt.setVersion(4, 3)
        self.fmt.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
        
        # OpenGL
        self.camera = OpenGLCamera()
        
        # Shaders
        self.shader_point_cloud = OpenGLShader()
        self.shader_images = OpenGLShader()
        self.shader_coordinate_system = OpenGLShader()
        
        self.shader_point_cloud.addShaderSource(
            Shaders.getShaderFile(GL_VERTEX_SHADER, "point_cloud.vert"),
            Shaders.getShaderFile(GL_FRAGMENT_SHADER, "point_cloud.frag")
        )
        
        self.shader_images.addShaderSource(
            Shaders.getShaderFile(GL_VERTEX_SHADER, "images.vert"),
            Shaders.getShaderFile(GL_FRAGMENT_SHADER, "images.frag")
        )
        
        self.shader_coordinate_system.addShaderSource(
            Shaders.getShaderFile(GL_VERTEX_SHADER, "coordinate_system.vert"),
            Shaders.getShaderFile(GL_FRAGMENT_SHADER, "coordinate_system.frag")
        )
        
        # Geometries
        self.coordinate_system: Geometry = OpenGLMesh(CoordinateSystem())
    
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
        
        
        # Draw Coordinate System
        if self.setting_show_coordinate_system:
            self.shader_coordinate_system.bind()
            self.camera.updateShaderUniform(self.shader_coordinate_system)
            
            self.coordinate_system.bind()
            self.coordinate_system.draw()
            self.coordinate_system.unbind()
            
            self.shader_coordinate_system.unbind()
        
        # Draw Point Cloud
        self.shader_point_cloud.bind()
        self.camera.updateShaderUniform(self.shader_point_cloud)
        
        for data in self.opengl_project_data:
            point_cloud = data["point_cloud"]
            
            point_cloud.bind(self.shader_point_cloud)
            point_cloud.draw()
            point_cloud.unbind()
        
        self.shader_point_cloud.unbind()
        
        
        # Draw Image
        self.shader_images.bind()
        self.camera.updateShaderUniform(self.shader_images)
        
        for data in self.opengl_project_data:
            pass
            #self.model_image.bind(self.shader_images)
            #self.model_image.draw()
            #self.model_image.unbind()
        
        self.shader_images.unbind()
        
        
        # Disable OpenGL Settings
        glDisable(GL_CULL_FACE)
        glDisable(GL_VERTEX_PROGRAM_POINT_SIZE);
        glDisable(GL_DEPTH_TEST);