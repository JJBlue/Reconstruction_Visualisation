from pathlib import Path
import queue

from OpenGL.raw.GL.VERSION.GL_2_0 import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER
from PyQt6.QtCore import QThread, QWaitCondition, QMutex
from PyQt6.QtGui import QOffscreenSurface, QOpenGLContext

from ba_trees.config.ConfigDirectories import ConfigDirectories
from default.Synchronization import synchronized
from render.functions import RenderDataStorages
from render.opengl import OpenGLShader
from render.render.Shader import ShaderFile, ShaderGroup


class OpenGLBackgroundUploadData(QThread):
    signal = QWaitCondition()
    mutex = QMutex()
    
    def __init__(self):
        super().__init__()
        
        self.running = False
        self.queue = queue.Queue()
        self.queue_context = queue.Queue()
    
    @synchronized
    def start(self) -> None:
        if self.running:
            return
        
        self.running = True
        super().start()
    
    @synchronized
    def stop(self):
        if not self.running:
            return
        
        self.running = False
        self.signal.wakeAll()
    
    def add(self, functon):
        self.queue.put(functon)
        self.signal.wakeAll()
    
    def addShareContext(self, context):
        self.queue_context.put(context)
        self.signal.wakeAll()
    
    def isRunning(self):
        return self.running
    
    def run(self):
        self.surface = QOffscreenSurface()
        self.surface.create()
        
        self.context = QOpenGLContext()
        self.context.create()
        
        while self.running:
            self.context.makeCurrent(self.surface)
            
            while not self.queue.empty():
                while not self.queue_context.empty():
                    self.context.setShareContext(self.queue.get())
                
                runnable = self.queue.get()
                runnable()
            
            self.context.doneCurrent()
            
            self.mutex.lock()
            self.signal.wait(self.mutex)
            self.mutex.unlock()

class OpenGLData:
    __loaded = False
    __background_task = OpenGLBackgroundUploadData()
    
    @staticmethod
    @synchronized
    def start():
        OpenGLData.__background_task.start()
        OpenGLData.load()
    
    @staticmethod
    @synchronized
    def stop():
        OpenGLData.__background_task.stop()
    
    def add(self, function):
        if not OpenGLData.__background_task.isRunning():
            OpenGLData.__background_task.start()
        
        OpenGLData.__background_task.add(function)
    
    def addShareContext(self, context):
        if not OpenGLData.__background_task.isRunning():
            OpenGLData.__background_task.start()
        
        OpenGLData.__background_task.addShareContext(context)
    
    @staticmethod
    @synchronized
    def load():
        if OpenGLData.__loaded:
            return
        
        # Shaders
        def upload_shader_point_cloud():
            shader_vert = OpenGLShader(OpenGLData.getShaderFile(GL_VERTEX_SHADER, "point_cloud.vert"))
            shader_frag = OpenGLShader(OpenGLData.getShaderFile(GL_FRAGMENT_SHADER, "point_cloud.frag"))
            shader = ShaderGroup(shader_vert, shader_frag)
            RenderDataStorages.getShaders().put("point_cloud", shader)
        OpenGLData.__background_task.add(upload_shader_point_cloud)
        
        def upload_shader_images():
            shader_vert = OpenGLShader(OpenGLData.getShaderFile(GL_VERTEX_SHADER, "images.vert"))
            shader_frag = OpenGLShader(OpenGLData.getShaderFile(GL_FRAGMENT_SHADER, "images.frag"))
            shader = ShaderGroup(shader_vert, shader_frag)
            RenderDataStorages.getShaders().put("images", shader)
        OpenGLData.__background_task.add(upload_shader_images)
        
        def upload_shader_coordinate_system():
            shader_vert = OpenGLShader(OpenGLData.getShaderFile(GL_VERTEX_SHADER, "coordinate_system.vert"))
            shader_frag = OpenGLShader(OpenGLData.getShaderFile(GL_FRAGMENT_SHADER, "coordinate_system.frag"))
            shader = ShaderGroup(shader_vert, shader_frag)
            RenderDataStorages.getShaders().put("coordinate_system", shader)
        OpenGLData.__background_task.add(upload_shader_coordinate_system)

        def upload_shader_framebuffer_image():
            shader_vert = OpenGLShader(OpenGLData.getShaderFile(GL_VERTEX_SHADER, "FrameBufferImage.vert"))
            shader_frag = OpenGLShader(OpenGLData.getShaderFile(GL_FRAGMENT_SHADER, "FrameBufferImage.frag"))
            shader = ShaderGroup(shader_vert, shader_frag)
            RenderDataStorages.getShaders().put("framebuffer_image", shader)
        OpenGLData.__background_task.add(upload_shader_framebuffer_image)
        
        # Finished
        OpenGLData.__loaded = True
    
    @staticmethod
    def getShaderFile(shader_type, file: str) -> ShaderFile:
        if not Path(file).exists():
            dirs = ConfigDirectories.getConfigDirectories()
            file = Path(dirs.getShaderFolder()).joinpath(file)
        
        return ShaderFile(shader_type, file)