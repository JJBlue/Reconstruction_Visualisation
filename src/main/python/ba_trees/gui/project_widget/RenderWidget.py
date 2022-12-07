from OpenGL.GL import *
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, QTimer
from PyQt6.QtGui import QSurfaceFormat
from PyQt6.QtOpenGL import QOpenGLVersionProfile
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

from ba_trees.gui.opengl.OpenGLData import OpenGLData
from ba_trees.gui.project_widget import BackgroundRenderWidget
from ba_trees.gui.project_widget.ControlStatus import ControlStatus
from ba_trees.workspace import Project
from render.data.GeometryStructures import Pane
from render.functions import RenderDataStorages, MousePicking
from render.opengl import OpenGLMesh, OpenGLProgramm
from render.render import Texture


class RenderWidget(QOpenGLWidget):
    # Signal
    showCoordinateSystemChanged = pyqtSignal(bool)
    pointSizeChanged = pyqtSignal(float)
    
    cameraSpeedChanged = pyqtSignal(float)
    cameraFOVChanged = pyqtSignal(float)
    cameraEnableMovementChanged = pyqtSignal(bool)
    
    model_position_x = pyqtSignal(float)
    model_position_y = pyqtSignal(float)
    model_position_z = pyqtSignal(float)
    
    model_rotation_pitch = pyqtSignal(float)
    model_rotation_yaw = pyqtSignal(float)
    model_rotation_roll = pyqtSignal(float)
    
    repaintSignal = pyqtSignal(Texture)
    
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        
        # Widget Settings
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus) # Must be set for keyPressEvent to work
        self.setMouseTracking(True) # To track Mouse Move without click event
        
        self.repaintSignal.connect(self.repaintObject)
        
        # Settings
        self.control_status = ControlStatus.CAMERA_MOVE
        self.mouse_pressed: bool = False
        self.mouse_x: float = -1
        self.mouse_y: float = -1
        
        self.projects: list = []
        
        self.setting_show_coordinate_system = True
        self.point_size = 1.0
        
        self.camera_speed: float = 0.1
        self.camera_enable_movement_speed: bool = True
        
        self.thread = BackgroundRenderWidget(self)
        QTimer.singleShot(1, self.runEmit)
    
    def runEmit(self):
        self.showCoordinateSystemChanged.emit(self.setting_show_coordinate_system)
        self.pointSizeChanged.emit(self.point_size)
        
        self.cameraSpeedChanged.emit(self.camera_speed)
        self.cameraEnableMovementChanged.emit(self.camera_enable_movement_speed)
        
        if self.thread != None and self.thread.camera != None:
            self.cameraFOVChanged.emit(self.thread.camera.fov)
    
    ##########################
    ### Mouse and Keyboard ###
    ##########################
    
    def keyPressEvent(self, event):
        if self.thread.camera != None and self.camera_enable_movement_speed:
            key = event.key()

            if key == Qt.Key.Key_W:
                self.thread.camera.forward(self.camera_speed)
                self.repaintInBackground()
            elif key == Qt.Key.Key_S:
                self.thread.camera.backward(self.camera_speed)
                self.repaintInBackground()
            elif key == Qt.Key.Key_A:
                self.thread.camera.leftward(self.camera_speed)
                self.repaintInBackground()
            elif key == Qt.Key.Key_D:
                self.thread.camera.rightward(self.camera_speed)
                self.repaintInBackground()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_pressed = True

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_pressed = False
            self.mouse_x: float = -1
            self.mouse_y: float = -1
        
        if self.thread != None and self.thread.camera != None:
            pass
            # ray = MousePicking.getRayFromCamera(fvec2(event.position().x(), event.position().y()), fvec2(self.width(), self.height()), self.thread.camera)
            # print(ray)

    def mouseMoveEvent(self, event):
        if self.thread.camera != None and self.camera_enable_movement_speed:
            if self.mouse_pressed:
                pos: QPoint = event.position()
    
                if self.mouse_x != -1:
                    degree: float = pos.x() - self.mouse_x
                    self.thread.camera.yaw(degree * -1.0 / 10.0)
    
                    degree: float = pos.y() - self.mouse_y
                    self.thread.camera.pitch(degree * -1.0 / 10.0)
                    
                    self.repaintInBackground()
                
                self.mouse_x = pos.x()
                self.mouse_y = pos.y()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        
        if self.thread.camera != None:
            self.thread.camera.forward(delta * self.camera_speed)
            self.repaintInBackground()
    
    ###########################
    ### QT Designer Methods ###
    ###########################
    
    def setPointSize(self, size: float):
        if self.point_size != size:
            self.point_size = size
            self.repaintInBackground()
            
            self.pointSizeChanged.emit(self.point_size)
    
    def show_coordinate_system(self, value: bool):
        if self.setting_show_coordinate_system != value:
            self.setting_show_coordinate_system = value
            self.repaintInBackground()
            
            self.showCoordinateSystemChanged.emit(self.setting_show_coordinate_system)
    
    def setCameraSpeed(self, value: float):
        if self.camera_speed != value:
            self.camera_speed = value
            self.cameraSpeedChanged.emit(self.camera_speed)
    
    def enableMovementChanged(self, value: bool):
        if self.camera_enable_movement_speed != value:
            self.camera_enable_movement_speed = value
            self.cameraEnableMovementChanged.emit(self.camera_enable_movement_speed)
    
    def setCameraFOV(self, value: float):
        if self.thread.camera != None and self.thread.camera.fov != value:
            self.thread.camera.fov = value
            self.cameraFOVChanged.emit(self.thread.camera.fov)
            self.repaintInBackground()
            
    
    ###############
    ### Methods ###
    ###############
    
    def addProject(self, project: Project):
        self.projects.append(project)
        self.thread.addProject(project)
        self.repaintInBackground()
    
    ##############
    ### OpenGL ###
    ##############
    def repaintObject(self, value):
        self.outputTexture = value
        self.repaint()
    
    def initializeGL(self)->None:
        super().initializeGL()
        
        self.fmt = QOpenGLVersionProfile()
        self.fmt.setVersion(4, 3)
        self.fmt.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
        
        OpenGLData.load()
        
        # Shaders
        global_storage = RenderDataStorages.getGloablRenderDataStorage()
        global_shader_storage = global_storage.getShaders()

        self.shader = OpenGLProgramm(global_shader_storage.get("framebuffer_image"))
        
        # Meshes
        self.image_mesh = OpenGLMesh(Pane())
        
        self.outputTexture = None
        
        QTimer.singleShot(1, self.initBackground)
        QTimer.singleShot(500, self.runEmit)
        
    def initBackground(self):
        self.thread.start()
    
    def resizeGL(self, width, height):
        super().resizeGL(width, height)
        
        if self.thread != None:
            self.thread.resize(width, height)
            self.thread.repaint()
    
    def repaintInBackground(self):
        if self.thread != None:
            self.thread.repaint()
    
    def paintGL(self):
        super().paintGL()
        
        if self.outputTexture == None:
            return
        
        #self.thread.mutex_texture.lock()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.shader.bind()
        self.image_mesh.bind()
        
        self.shader.uniform("tex", self.outputTexture, 0)
        self.image_mesh.draw()
        
        self.image_mesh.unbind()
        self.shader.unbind()
        
        #self.thread.mutex_texture.unlock()