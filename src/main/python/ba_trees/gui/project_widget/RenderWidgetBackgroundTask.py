from OpenGL.GL import *
from PIL import Image, ImageOps
from PyQt6.QtCore import QThread, QWaitCondition, QMutex
from PyQt6.QtGui import QOffscreenSurface, QOpenGLContext

from ba_trees.workspace import Project
from render.data import CoordinateSystem
from render.data.TextureData import TextureInternalFormat, TextureFormat, TextureType, TextureData
from render.functions import RenderDataStorages
from render.opengl import OpenGLCamera, OpenGLModel, OpenGLMesh, OpenGLTexture, OpenGLFrameBuffer, OpenGLProgramm
from render.render import FrameBuffer


class BackgroundRenderWidget(QThread):
    repaintSignal = QWaitCondition()
    mutex_repaintSignal = QMutex()
    
    def __init__(self, rw):
        super().__init__()
        
        self.rw = rw
        self.format = self.rw.format()
        
        self.surface = QOffscreenSurface()
        self.surface.setFormat(self.format)
        self.surface.create()
        
        self.new_projects: list = []
        self.opengl_project_data: list = []
        self.outputTexture = None
        
        self.width: int = 1080
        self.height: int = 1920
        
        # OpenGL
        self.camera = None
    
    def addProject(self, project: Project):
        self.new_projects.append(project)
    
    def resize(self, width, height):
        self.width = width
        self.height = height
        self.sizeChanged = True
    
    def repaint(self):
        self.repaintSignal.wakeAll()
    
    def run(self):
        # Create Context
        self.context = QOpenGLContext()
        self.context.setFormat(self.format)
        self.context.setShareContext(self.context.globalShareContext())
        self.context.create()
        
        # Initialize
        self.context.makeCurrent(self.surface)
        self.__initialize()
        self.context.doneCurrent()
        
        while True: # Change True
            self.__render_steps()
            
            self.mutex_repaintSignal.lock()
            self.repaintSignal.wait(self.mutex_repaintSignal)
            self.mutex_repaintSignal.unlock()
    
    def __render_steps(self, _ = None):
        self.context.makeCurrent(self.surface)
        
        self.__update()
        self.__render()
        
        self.context.doneCurrent()
    
    def __initialize(self):
        # OpenGL
        self.camera = OpenGLCamera()
        
        # Global storage
        global_storage = RenderDataStorages.getGloablRenderDataStorage()
        self.global_shader_storage = global_storage.getShaders()
        local_mesh_storage = RenderDataStorages.getLocalRenderDataStorage(self.context).getMeshes()
        
        # Shaders
        self.shader_point_cloud = None
        self.shader_images = None
        self.shader_coordinate_system = None
        
        # Meshes
        mesh = OpenGLMesh(CoordinateSystem())
        local_mesh_storage.put("coordinate_system", mesh)
        
        # Geometries
        self.coordinate_system = local_mesh_storage.get("coordinate_system")
        
        # FrameBuffer
        self.framebuffer: FrameBuffer = OpenGLFrameBuffer()
        self.framebuffer.bind()
        
        self.framebuffer.resize(self.width, self.height)
        
        # Texture: Output of the (3D-)View
        texture_data: TextureData = TextureData(TextureInternalFormat.RGBA, TextureFormat.RGBA, TextureType.UNSIGNED_BYTE, self.width, self.height, None)
        texture_data.setUseMipmap(False)
        texture_data.setRepeatImage(False)
        texture_data.setUnpackAlignment(False)
        texture_data.setPoorFiltering(True)
        
        self.outputTexture = OpenGLTexture(texture_data)
        self.framebuffer.addTexture(self.outputTexture)
        
        # Texture: Output of the MousePicking Color Texture
        self.outputMousePickingTexture = OpenGLTexture(texture_data)
        self.framebuffer.addTexture(self.outputMousePickingTexture)
        
        self.framebuffer.setDrawBuffer(0)
        
        self.framebuffer.unbind()
    
    def __update(self):
        # Initialize
        if not self.shader_point_cloud and self.global_shader_storage.has("point_cloud"):
            self.shader_point_cloud = OpenGLProgramm(self.global_shader_storage.get("point_cloud"))
        
        if not self.shader_images and self.global_shader_storage.has("images"):
            self.shader_images = OpenGLProgramm(self.global_shader_storage.get("images"))
        
        if not self.shader_coordinate_system and self.global_shader_storage.has("coordinate_system"):
            self.shader_coordinate_system = OpenGLProgramm(self.global_shader_storage.get("coordinate_system"))
        
        # Update Objects
        self.camera.update()
        
        # Resize
        if self.sizeChanged:
            self.sizeChanged = False
            
            self.framebuffer.resize(self.width, self.height)
        
        # Add Project to OpenGL
        while len(self.new_projects) > 0:
            project = self.new_projects.pop()
            
            data: dict = {}
            
            point_cloud = OpenGLModel()
            point_cloud.addGeometries(project.getDense())
            data["point_cloud_dense"] = point_cloud
            
            point_cloud = OpenGLModel()
            point_cloud.addGeometries(project.getSparse())
            data["point_cloud_sparse"] = point_cloud
            
            #self.model_image = OpenGLModel(self.project.getImages()[0])
            
            self.opengl_project_data.append(data)
    
    def __render(self):
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
        if self.rw.setting_show_coordinate_system and self.shader_coordinate_system:
            self.shader_coordinate_system.bind()
            self.camera.updateShaderUniform(self.shader_coordinate_system)
            
            self.coordinate_system.bind()
            self.coordinate_system.draw()
            self.coordinate_system.unbind()
            
            self.shader_coordinate_system.unbind()
        
        # Draw Point Cloud
        if self.shader_point_cloud:
            self.shader_point_cloud.bind()
            self.shader_point_cloud.uniform("point_size", self.rw.point_size)
            self.camera.updateShaderUniform(self.shader_point_cloud)
            
            for data in self.opengl_project_data:
                self.shader_point_cloud.uniform("mouse_picker", True)
                point_cloud = data["point_cloud_sparse"]
                point_cloud.bind(self.shader_point_cloud)
                point_cloud.draw()
                point_cloud.unbind()
                
                self.shader_point_cloud.uniform("mouse_picker", False)
                point_cloud = data["point_cloud_dense"]
                point_cloud.bind(self.shader_point_cloud)
                point_cloud.draw()
                point_cloud.unbind()
            
            self.shader_point_cloud.unbind()
        
        
        # Draw Image
        if self.shader_images:
            self.shader_images.bind()
            self.camera.updateShaderUniform(self.shader_images)
            
            for data in self.opengl_project_data:
                pass
                #self.model_image.bind(self.shader_images)
                #self.model_image.draw()
                #self.model_image.unbind()
            
            self.shader_images.unbind()
        
        #self.saveImage()
        self.framebuffer.unbind()
        glFlush() # Start Rendering if it is not happend yet
        glFinish() # Wait for finished rendering
        
        # Disable OpenGL Settings
        glDisable(GL_CULL_FACE)
        glDisable(GL_VERTEX_PROGRAM_POINT_SIZE);
        glDisable(GL_DEPTH_TEST);
        
        self.rw.repaintSignal.emit(self.outputTexture)

    def saveImage(self):
        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        data = glReadPixels(0, 0, self.width, self.height, GL_RGBA, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGBA", (self.width, self.height), data)
        image = ImageOps.flip(image)
        image.save('J:\\Codes\\git\\BA_Trees\\config\\test.png', 'PNG')