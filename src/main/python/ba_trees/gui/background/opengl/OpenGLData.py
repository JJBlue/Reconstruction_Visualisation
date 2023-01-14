from pathlib import Path
import queue

from OpenGL.raw.GL.VERSION.GL_2_0 import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER
from PyQt6.QtCore import QThread, QWaitCondition, QMutex
from PyQt6.QtGui import QOffscreenSurface, QOpenGLContext, QSurfaceFormat

from ba_trees.config.ConfigDirectories import ConfigDirectories
from default.Synchronization import synchronized
from render.functions import RenderDataStorages
from render.opengl import OpenGLShader
from render.render.Shader import ShaderFile, ShaderGroup


class OpenGLBackgroundUploadData(QThread):
    signal = QWaitCondition()
    mutex = QMutex()
    
    def __init__(self, queue_functions):
        super().__init__()
        
        self.running = False
        self.queue = queue_functions
        self.queue_context = queue.Queue()
        
        surface_format = QSurfaceFormat()
        surface_format.setVersion(4, 6)
        surface_format.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
        
        self.surface = QOffscreenSurface()
        self.surface.setFormat(surface_format)
        self.surface.format()
        self.surface.create()
        
        self.context = None
    
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
    
    # DO NOT USE! Share with context.globalShareContext() instead
    # Activate globale Share before: QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
    def addShareContext(self, context):
        if self.context != None:
            self.context.setShareContext(context)
        else:
            self.queue_context.put(context)
            self.signal.wakeAll()
    
    def isRunning(self):
        return self.running
    
    def run(self):        
        self.context = QOpenGLContext()
        self.context.setFormat(self.surface.format())
        self.context.setShareContext(self.context.globalShareContext()) # Share with globalShareContext from Qt (Shares over all Applications)
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
    __started = False
    __loaded = False
    __background_tasks: list = []
    
    __queue = None
    
    
    @staticmethod
    @synchronized
    def start():
        if OpenGLData.__started:
            return
        
        OpenGLData.__started = True
        
        OpenGLData.__queue = queue.Queue()
        
        if not OpenGLData.__background_tasks:
            for _ in range(5):
                thread = OpenGLBackgroundUploadData(OpenGLData.__queue)
                thread.start()
                
                OpenGLData.__background_tasks.append(thread)
        
        OpenGLData.runLater(OpenGLData.__load)
    
    @staticmethod
    @synchronized
    def stop():
        if not OpenGLData.__started:
            return
        
        OpenGLData.__started = False
        
        for thread in OpenGLData.__background_tasks:
            thread.stop()
        
        OpenGLData.__background_tasks.clear()
    
    @staticmethod
    def runLater(function):
        if not OpenGLData.__started:
            return
        
        OpenGLData.__queue.put(function)
        OpenGLBackgroundUploadData.signal.wakeAll()
    
    @staticmethod
    def addShareContext(context):
        if not OpenGLData.__background_task.isRunning():
            OpenGLData.__background_task.start()
        
        OpenGLData.__background_task.addShareContext(context)
    
    @staticmethod
    def __load():
        # Shaders
        shader_vert = OpenGLShader(OpenGLData.getShaderFile(GL_VERTEX_SHADER, "point_cloud_sparse.vert"))
        shader_frag = OpenGLShader(OpenGLData.getShaderFile(GL_FRAGMENT_SHADER, "point_cloud_sparse.frag"))
        shader = ShaderGroup(shader_vert, shader_frag)
        RenderDataStorages.getShaders().put("point_cloud_sparse", shader)
        
        shader_vert = OpenGLShader(OpenGLData.getShaderFile(GL_VERTEX_SHADER, "point_cloud_dense.vert"))
        shader_frag = OpenGLShader(OpenGLData.getShaderFile(GL_FRAGMENT_SHADER, "point_cloud_dense.frag"))
        shader = ShaderGroup(shader_vert, shader_frag)
        RenderDataStorages.getShaders().put("point_cloud_dense", shader)
        
        shader_vert = OpenGLShader(OpenGLData.getShaderFile(GL_VERTEX_SHADER, "camera.vert"))
        shader_frag = OpenGLShader(OpenGLData.getShaderFile(GL_FRAGMENT_SHADER, "camera.frag"))
        shader = ShaderGroup(shader_vert, shader_frag)
        RenderDataStorages.getShaders().put("camera", shader)
        
        shader_vert = OpenGLShader(OpenGLData.getShaderFile(GL_VERTEX_SHADER, "images.vert"))
        shader_frag = OpenGLShader(OpenGLData.getShaderFile(GL_FRAGMENT_SHADER, "images.frag"))
        shader = ShaderGroup(shader_vert, shader_frag)
        RenderDataStorages.getShaders().put("images", shader)
        
        shader_vert = OpenGLShader(OpenGLData.getShaderFile(GL_VERTEX_SHADER, "coordinate_system.vert"))
        shader_frag = OpenGLShader(OpenGLData.getShaderFile(GL_FRAGMENT_SHADER, "coordinate_system.frag"))
        shader = ShaderGroup(shader_vert, shader_frag)
        RenderDataStorages.getShaders().put("coordinate_system", shader)

        shader_vert = OpenGLShader(OpenGLData.getShaderFile(GL_VERTEX_SHADER, "FrameBufferImage.vert"))
        shader_frag = OpenGLShader(OpenGLData.getShaderFile(GL_FRAGMENT_SHADER, "FrameBufferImage.frag"))
        shader = ShaderGroup(shader_vert, shader_frag)
        RenderDataStorages.getShaders().put("framebuffer_image", shader)
    
    @staticmethod
    def getShaderFile(shader_type, file: str) -> ShaderFile:
        if not Path(file).exists():
            dirs = ConfigDirectories.getConfigDirectories()
            file = Path(dirs.getShaderFolder()).joinpath(file)
        
        return ShaderFile(shader_type, file)