from OpenGL.GL import *
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, QTimer
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import QTreeWidgetItem

from ba_trees.gui.project_widget import BackgroundRenderWidget
from ba_trees.gui.project_widget.ControlStatus import ControlStatus
from ba_trees.gui.project_widget.RenderSettings import RenderObject, RenderModel
from ba_trees.workspace import Project
from render.data.GeometryStructures import Pane
from render.functions import RenderDataStorages
from render.opengl import OpenGLMesh, OpenGLProgramm
from render.opengl.OpenGLBuffer import OpenGLBufferGroup
from render.render import Texture


class RenderWidget(QOpenGLWidget):
    # Signal
    showCoordinateSystemChanged = pyqtSignal(bool)
    pointSizeChanged = pyqtSignal(float)
    
    cameraSpeedChanged = pyqtSignal(float)
    cameraFOVChanged = pyqtSignal(float)
    cameraEnableMovementChanged = pyqtSignal(bool)
    
    renderStructureChanged = pyqtSignal(RenderObject)
    cameraScaleModelChanged = pyqtSignal(float)
    
    repaintSignal = pyqtSignal(Texture)
    mousePickingSignal = pyqtSignal(Texture)
    
    
    # Model Settings
    modelPositionXChanged = pyqtSignal(float)
    modelPositionYChanged = pyqtSignal(float)
    modelPositionZChanged = pyqtSignal(float)
    modelRotationPitchChanged = pyqtSignal(float)
    modelRotationYawChanged = pyqtSignal(float)
    modelRotationRollChanged = pyqtSignal(float)
    modelPositionScaleXChanged = pyqtSignal(float)
    modelPositionScaleYChanged = pyqtSignal(float)
    modelPositionScaleZChanged = pyqtSignal(float)
    
    modelVisibleChanged = pyqtSignal(bool)
    
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
        
        self.selected_models = None
        self.show_dense_model = True
        self.show_sparse_model = True
        self.show_camera_model = True
        self.camera_scale_model = 0.4
        
        self.selected_render_object = None
        
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
        pos: QPoint = event.position()
        self.thread.selectPixelCoord(self.window(), pos.x(), pos.y())
        self.thread.repaint()
    
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
    
    def selectCurrentModel(self, render_object: RenderObject):
        self.selected_render_object = render_object
        
        if isinstance(render_object, RenderModel):
            model_matrix = render_object.model.model_matrix
            
            self.modelPositionXChanged.emit(model_matrix.getX())
            self.modelPositionYChanged.emit(model_matrix.getY())
            self.modelPositionZChanged.emit(model_matrix.getZ())
            self.modelRotationPitchChanged.emit(model_matrix.getPitch())
            self.modelRotationYawChanged.emit(model_matrix.getYaw())
            self.modelRotationRollChanged.emit(model_matrix.getRoll())
        else:
            self.modelPositionXChanged.emit(0)
            self.modelPositionYChanged.emit(0)
            self.modelPositionZChanged.emit(0)
            self.modelRotationPitchChanged.emit(0)
            self.modelRotationYawChanged.emit(0)
            self.modelRotationRollChanged.emit(0)
        
        self.modelVisibleChanged.emit(render_object.visible)
    
    def __getModelMatrixFromModel(self):
        render_object = self.selected_render_object
        if render_object == None:
            return
        
        model_matrix = None
        if isinstance(render_object, RenderModel):
            model_matrix = render_object.model.model_matrix
        
        return model_matrix
    
    def setModelPositionX(self, value: float):
        model_matrix = self.__getModelMatrixFromModel()
        if model_matrix == None:
            return
        
        model_matrix.setX(value)
        self.repaintInBackground()
    
    def setModelPositionY(self, value: float):
        model_matrix = self.__getModelMatrixFromModel()
        if model_matrix == None:
            return
        
        model_matrix.setY(value)
        self.repaintInBackground()
    
    def setModelPositionZ(self, value: float):
        model_matrix = self.__getModelMatrixFromModel()
        if model_matrix == None:
            return
        
        model_matrix.setZ(value)
        self.repaintInBackground()
    
    def setModelPositionPitch(self, value: float):
        model_matrix = self.__getModelMatrixFromModel()
        if model_matrix == None:
            return
        
        model_matrix.setPitch(value)
        self.thread.repaint()
    
    def setModelPositionYaw(self, value: float):
        model_matrix = self.__getModelMatrixFromModel()
        if model_matrix == None:
            return
        
        model_matrix.setYaw(value)
        self.repaintInBackground()
    
    def setModelPositionRoll(self, value: float):
        model_matrix = self.__getModelMatrixFromModel()
        if model_matrix == None:
            return
        
        model_matrix.setRoll(value)
        self.repaintInBackground()
    
    def setModelPositionScaleX(self, value: float):
        model_matrix = self.__getModelMatrixFromModel()
        if model_matrix == None:
            return
        
        model_matrix.scaleX(value)
        self.repaintInBackground()
    
    def setModelPositionScaleY(self, value: float):
        model_matrix = self.__getModelMatrixFromModel()
        if model_matrix == None:
            return
        
        model_matrix.scaleY(value)
        self.repaintInBackground()
    
    def setModelPositionScaleZ(self, value: float):
        model_matrix = self.__getModelMatrixFromModel()
        if model_matrix == None:
            return
        
        model_matrix.scaleZ(value)
        self.repaintInBackground()
    
    def setModelVisible(self, value: bool):
        render_object = self.selected_render_object
        if render_object == None:
            return
        
        render_object.visible = value
        self.repaintInBackground()
    
    def setCameraScaleModel(self, value: float):
        pass
    
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
        buffer_group = OpenGLBufferGroup.createBufferGroup(Pane()) # TODO global
        self.image_mesh = OpenGLMesh(buffer_group)
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