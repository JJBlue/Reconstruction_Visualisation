import time

from OpenGL.GL import *
from PIL import Image, ImageOps
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, QTimer, QThread
from PyQt6.QtGui import QSurfaceFormat, QOffscreenSurface, QOpenGLContext
from PyQt6.QtOpenGL import QOpenGLVersionProfile
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

from ba_trees.gui.opengl.OpenGLData import OpenGLData
from ba_trees.workspace import Project
from render.data import CoordinateSystem
from render.data.GeometryStructures import Pane
from render.data.TextureData import TextureInternalFormat, TextureFormat, TextureType, TextureData
from render.functions import RenderDataStorages
from render.opengl import OpenGLCamera, OpenGLModel, OpenGLMesh, OpenGLTexture, OpenGLFrameBuffer, \
    OpenGLProgramm
from render.render import Shader, Camera, FrameBuffer


class BackgroundRenderWidget(QThread):
    def __init__(self, rw):
        super().__init__()
        
        self.rw = rw
        self.format = self.rw.format()
        
        self.surface = QOffscreenSurface()
        self.surface.setFormat(self.format)
        self.surface.create()
        
        self.new_projects: list = []
        self.opengl_project_data: list = []
        self.outputTextureID = 0
    
    def addProject(self, project: Project):
        self.new_projects.append(project)
    
    def run(self):
        self.context = QOpenGLContext()
        self.context.setFormat(self.format)
        self.context.setShareContext(self.rw.context())
        self.context.create()
        
        self.context.makeCurrent(self.surface)
        
        self.initialize()
        
        # TODO maybe:
        # To Update automatic, run while loop
        #self.initializeNewObjects()
        self.update()
        self.render()
        
        self.context.doneCurrent()
    
    def initialize(self):
        self.width: int = 1080
        self.height: int = 1920
        
        # OpenGL
        self.camera = OpenGLCamera()
        OpenGLData.load()
        
        # Global storage
        global_storage = RenderDataStorages.getGloablRenderDataStorage()
        global_shader_storage = global_storage.getShaders()
        local_mesh_storage = RenderDataStorages.getLocalRenderDataStorage(self.context).getMeshes()
        
        # Shaders
        self.shader_point_cloud = OpenGLProgramm(global_shader_storage.get("point_cloud"))
        self.shader_images = OpenGLProgramm(global_shader_storage.get("images"))
        self.shader_coordinate_system = OpenGLProgramm(global_shader_storage.get("coordinate_system"))
        
        # Meshes
        mesh = OpenGLMesh(CoordinateSystem())
        local_mesh_storage.put("coordinate_system", mesh)
        
        # Geometries
        self.coordinate_system = local_mesh_storage.get("coordinate_system")
        
        # FrameBuffer
        self.framebuffer: FrameBuffer = OpenGLFrameBuffer()
        self.framebuffer.bind()
        
        self.framebuffer.resize(self.width, self.height)
        
        texture_data: TextureData = TextureData(TextureInternalFormat.RGBA, TextureFormat.RGBA, TextureType.UNSIGNED_BYTE, self.width, self.height, None)
        texture_data.setUseMipmap(False)
        texture_data.setRepeatImage(False)
        texture_data.setUnpackAlignment(False)
        texture_data.setPoorFiltering(True)
        
        texture = OpenGLTexture(texture_data)
        self.outputTextureID = texture.getID()
        self.framebuffer.addTexture(texture)
        self.framebuffer.setDrawBuffer(0)
        
        self.framebuffer.unbind()
    
    def initializeNewObjects(self):
        # Add Project to OpenGL
        while len(self.new_projects) > 0:
            project = self.new_projects.pop()
            
            data: dict = {}
        
            point_cloud = OpenGLModel(project.getModel())
            data["point_cloud"] = point_cloud
            
            #self.model_image: Model = OpenGLModel(self.project.getImages()[0])
            
            self.opengl_project_data.append(data)
    
    def update(self):
        # Update Objects
        self.camera.update()
    
    def render(self):
        # Enable OpenGL Settings
        glFrontFace(GL_CCW)
        glCullFace(GL_BACK)
        glEnable(GL_CULL_FACE)
        
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE);
        glEnable(GL_DEPTH_TEST);
        
        self.framebuffer.bind()
        glViewport(0, 0, self.width, self.height);
        
        # Clear OpenGL Frame
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Draw Coordinate System
        if self.rw.setting_show_coordinate_system:
            self.shader_coordinate_system.bind()
            self.camera.updateShaderUniform(self.shader_coordinate_system)
            
            self.coordinate_system.bind()
            self.coordinate_system.draw()
            self.coordinate_system.unbind()
            
            self.shader_coordinate_system.unbind()
        
        # Draw Point Cloud
        self.shader_point_cloud.bind()
        self.shader_point_cloud.uniform("point_size", self.rw.point_size)
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
        
        self.save()
        
        self.framebuffer.unbind()
        
        # Disable OpenGL Settings
        glDisable(GL_CULL_FACE)
        glDisable(GL_VERTEX_PROGRAM_POINT_SIZE);
        glDisable(GL_DEPTH_TEST);
        
        self.rw.repaintSignal.emit(self.outputTextureID)

    def save(self):
        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        data = glReadPixels(0, 0, self.width, self.height, GL_RGBA, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGBA", (self.width, self.height), data)
        image = ImageOps.flip(image)
        image.save('J:\\Codes\\git\\BA_Trees\\config\\test.png', 'PNG')
        

class RenderWidget(QOpenGLWidget):
    # Signal
    showCoordinateSystemChanged = pyqtSignal(bool)
    pointSizeChanged = pyqtSignal(float)
    
    cameraSpeedChanged = pyqtSignal(float)
    cameraFOVChanged = pyqtSignal(float)
    cameraEnableMovementChanged = pyqtSignal(bool)
    
    repaintSignal = pyqtSignal(int)
    
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        
        # Widget Settings
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus) # Must be set for keyPressEvent to work
        self.setMouseTracking(True) # To track Mouse Move without click event
        
        self.repaintSignal.connect(self.repaintObject)
        
        # GL Settings
        self.camera: Camera = None
        self.shader: Shader = None
        
        self.mouse_pressed: bool = False
        self.mouse_x: float = -1
        self.mouse_y: float = -1
        
        self.projects: list = []
        
        # Settings
        self.setting_show_coordinate_system = True
        self.point_size = 1.0
        
        self.camera_speed: float = 0.1
        self.camera_enable_movement_speed: bool = True
        
        QTimer.singleShot(1, self.runEmit)
    
    def runEmit(self):
        self.showCoordinateSystemChanged.emit(self.setting_show_coordinate_system)
        self.pointSizeChanged.emit(self.point_size)
        
        self.cameraSpeedChanged.emit(self.camera_speed)
        self.cameraEnableMovementChanged.emit(self.camera_enable_movement_speed)
        
        if self.camera != None:
            self.cameraFOVChanged.emit(self.camera.fov)
    
    ##########################
    ### Mouse and Keyboard ###
    ##########################
    
    def keyPressEvent(self, event):
        if self.camera != None and self.camera_enable_movement_speed:
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
        if self.camera != None and self.camera_enable_movement_speed:
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

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        
        self.camera.forward(delta * self.camera_speed)
        self.repaint()
    
    ###########################
    ### QT Designer Methods ###
    ###########################
    
    def setPointSize(self, size: float):
        if self.point_size != size:
            self.point_size = size
            self.repaint()
            
            self.pointSizeChanged.emit(self.point_size)
    
    def show_coordinate_system(self, value: bool):
        if self.setting_show_coordinate_system != value:
            self.setting_show_coordinate_system = value
            self.repaint()
            
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
        if self.camera != None and self.camera.fov != value:
            self.camera.fov = value
            self.cameraFOVChanged.emit(self.camera.fov)
            self.repaint()
            
    
    ###############
    ### Methods ###
    ###############
    
    def addProject(self, project: Project):
        self.projects.append(project)
        #self.thread.addProject(project)
        #self.repaint()
    
    ##############
    ### OpenGL ###
    ##############
    def repaintObject(self, value: int):
        print("repaint")
        print(value)
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
        
        self.outputTextureID = 0
        
        QTimer.singleShot(1, self.initBackground)
        
    def initBackground(self):
        # Background Thread
        self.thread = BackgroundRenderWidget(self)
        self.thread.start()
    
    def resizeGL(self, width, height):
        super().resizeGL(width, height)
        
    def paintGL(self):
        super().paintGL()
        
        if self.outputTextureID == 0:
            return
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.shader.bind()
        
        self.image_mesh.bind()
        self.image_mesh.draw()
        self.image_mesh.unbind()
        
        self.shader.unbind()
    