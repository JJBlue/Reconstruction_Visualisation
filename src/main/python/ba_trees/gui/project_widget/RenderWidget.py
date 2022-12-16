from OpenGL.GL import *
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, QTimer
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

from ba_trees.gui.project_widget import BackgroundRenderWidget
from ba_trees.gui.project_widget.ControlStatus import ControlStatus
from ba_trees.workspace import Project
from render.data.GeometryStructures import Pane
from render.functions import RenderDataStorages
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
    mousePickingSignal = pyqtSignal(Texture)
    
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        
        # Widget Settings
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus) # Must be set for keyPressEvent to work
        self.setMouseTracking(True) # To track Mouse Move without click event
        
        self.repaintSignal.connect(self.repaintObject)
        self.mousePickingSignal.connect(self.mousePickingTextureChanged)
        
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
        self.thread.start()
        
        QTimer.singleShot(1, self.runEmit)
        #QTimer.singleShot(500, self.runEmit)
    
    def __del__(self):
        self.thread.stop()
    
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
    
    def mouseDoubleClickEvent(self, event):
        self.mouseDoubleClickRunnable()
        
        print("Double Click")
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_pressed = False
            self.mouse_x: float = -1
            self.mouse_y: float = -1

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
    
    def mousePickingTextureChanged(self, texture):
        self.mousePickingTexture = texture
    
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
        
        # Shaders
        global_storage = RenderDataStorages.getGloablRenderDataStorage()
        self.global_shader_storage = global_storage.getShaders()
        
        self.shader = None
        
        # Meshes
        self.image_mesh = OpenGLMesh(Pane())
        self.outputTexture = None
    
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
        
        if not self.shader and self.global_shader_storage.has("framebuffer_image"):
            self.shader = OpenGLProgramm(self.global_shader_storage.get("framebuffer_image"))
        
        if self.outputTexture == None:
            return
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        if self.shader:
            self.shader.bind()
            self.image_mesh.bind()
            
            self.shader.uniform("tex", self.outputTexture, 0)
            self.image_mesh.draw()
            
            self.image_mesh.unbind()
            self.shader.unbind()