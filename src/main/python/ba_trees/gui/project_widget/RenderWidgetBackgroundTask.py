import time
import glm
import numpy as np

from OpenGL.GL import *
from PIL import Image, ImageOps
from PyQt6.QtCore import QThread, QWaitCondition, QMutex
from PyQt6.QtGui import QOffscreenSurface, QOpenGLContext, QSurfaceFormat

from ba_trees.gui.background.qt.QtFunctions import QtFunctions
from ba_trees.gui.image_pixel_widget import PointInImageWidget
from ba_trees.workspace import Project
from ba_trees.workspace.colmap.ColmapOpenGL import ColmapProjectOpenGL

from render.data import CoordinateSystem, Primitves, PrimitiveType
from render.data.RenderBufferData import RenderBufferInternalFormat
from render.data.TextureData import TextureInternalFormat, TextureFormat, TextureType, TextureData
from render.functions import RenderDataStorages
from render.functions.MousePickerColor import MousePickerColor
from render.opengl import OpenGLCamera, OpenGLMesh, OpenGLTexture, OpenGLFrameBuffer, OpenGLProgramm
from render.opengl.OpenGLBuffer import OpenGLBufferGroup, OpenGLBufferFactory
from render.opengl.OpenGLRenderBuffer import OpenGLRenderBuffer
from render.render import FrameBuffer, RenderBuffer, Model
from render.render.Buffer import BufferGroup


class SelectionLines():
    def __init__(self):
        self.amount = 0
        self.lines: np.ndarray = np.array([], dtype=np.float32)
        self.colors: np.ndarray = np.array([], dtype=np.float32)
        
        self.model = Model()
        self.buffer_lines = BufferGroup()
        self.buffer_lines.geometry_primitive_type = Primitves.LINES
        
        self.vbo_lines = OpenGLBufferFactory.VBO()
        self.vbo_lines.setMetaData(PrimitiveType.FLOAT, 3, self.amount)
        
        self.vbo_colors = OpenGLBufferFactory.VBO()
        self.vbo_colors.setMetaData(PrimitiveType.FLOAT, 3, self.amount)
        
        self.buffer_lines.addVertexBuffer(self.vbo_lines)
        self.buffer_lines.addVertexBuffer(self.vbo_colors)
        self.model.addMeshes(OpenGLMesh(self.buffer_lines))
    
    def addLine(self, x: list, y: list):
        self.amount += 1
        self.lines = np.append(self.lines, x).astype(np.float32)
        self.colors = np.append(self.colors, [0.0, 1.0, 1.0]).astype(np.float32)
        
        self.amount += 1
        self.lines = np.append(self.lines, y).astype(np.float32)
        self.colors = np.append(self.colors, [1.0, 1.0, 0.0]).astype(np.float32)
        
        
        self.vbo_lines.setData(self.lines)
        self.vbo_lines.setMetaData(PrimitiveType.FLOAT, 3, self.amount)
        
        self.vbo_colors.setData(self.colors)
        self.vbo_colors.setMetaData(PrimitiveType.FLOAT, 3, self.amount)
        
        self.buffer_lines.count_vertices = self.amount
    
    def clearLines(self):
        self.amount = 0
        self.lines = np.resize(self.lines, 0)
        self.colors = np.resize(self.colors, 0)
        # Maybe clear Buffer on GPU
    
    def getModel(self):
        return self.model
    
class BackgroundRenderWidget(QThread):
    repaintSignal = QWaitCondition()
    mutex_repaintSignal = QMutex()
    
    def __init__(self, rw):
        super().__init__()
        
        self.rw = rw
        self.running = False
        self.width: int = 1080
        self.height: int = 1920
        #self.format = self.rw.format()
        
        surface_format = QSurfaceFormat()
        surface_format.setVersion(4, 6)
        surface_format.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
        self.format = surface_format
        
        self.surface = QOffscreenSurface()
        self.surface.setFormat(self.format)
        self.surface.create()
        
        self.projects: list = []
        self.new_projects: list = []
        self.opengl_project_data: list = []
        self.outputTexture = None
        
        # Events
        self.sizeChanged = True
        self.should_repaint = False
        
        # OpenGL
        self.camera = None
        self.runnables = []
    
    ######################
    ### Global Methops ###
    ######################
    
    def selectPixelCoord(self, window, x: int, y: int, radius: int = 10):
        def run(window = window, x: int = x, y: int = y, radius: int = radius):
            self.__selectPixelCoordGL(window, x, y, radius)
        
        self.runnables.append(run)
    
    def __selectPixelCoordGL(self, window, x: int, y: int, radius: int = 10): # TODO failed near border
        selected_pixels = []
        y = self.height - y # Flip (OpenGL)
        
        # Read Pixels and store in data
        self.framebuffer.bind()
        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        glReadBuffer(GL_COLOR_ATTACHMENT1)
        
        image_x = int(glm.clamp(x - radius, 0, x))
        image_y = int(glm.clamp(y - radius, 0, y))
        image_width = int(glm.clamp(2 * radius + 1, x - image_x + 1, self.width - x))
        image_height = int(glm.clamp(2 * radius + 1, y - image_y + 1, self.height - y))
        
        data = glReadPixels(image_x, image_y, image_width, image_height, GL_RGBA_INTEGER, GL_UNSIGNED_INT)
        
        self.framebuffer.unbind()
        data = np.asarray(data, np.uint32).flatten()
        
        # Search for nearest Pixel (begin center: clicked pixel and move outside in rectangles)
        size: int = 2 * radius + 1
        x_center: int = int((size - 1) / 2)
        y_center: int = int((size - 1) / 2)
        
        color_size = 4
        width, height = size, size
        size: int = (size) * color_size
        
        for i in range(radius + 1):
            if len(selected_pixels) > 0:
                break
            
            for xi in range(i * 2 + 1):
                xt: int = x_center + i - xi
                
                if xt < 0:
                    break
                if xt >= width:
                    continue
                
                yt: int = y_center - i
                if yt >= 0:
                    pixel: int = yt * size + xt * color_size
                    pick_result = MousePickerColor.colorToID_list(data, pixel)
                    
                    if pick_result != None:
                        selected_pixels.append(pick_result)
                        break
                
                if i == 0:
                    continue
                
                yt: int = y_center + i
                if yt < height:
                    pixel: int = yt * size + xt * color_size
                    pick_result = MousePickerColor.colorToID_list(data, pixel)
                    
                    if pick_result != None:
                        selected_pixels.append(pick_result)
                        break
            
            for yi in range(1, i * 2):
                yt: int = y_center + i - yi
                
                if yt < 0:
                    break
                if yt >= height:
                    continue
                
                xt: int = x_center - i
                if xt >= 0:
                    pixel: int = yt * size + xt * color_size
                    pick_result = MousePickerColor.colorToID_list(data, pixel)
                    
                    if pick_result != None:
                        selected_pixels.append(pick_result)
                        break
                
                xt: int = x_center + i
                if xt < width:
                    pixel: int = yt * size + xt * color_size
                    pick_result = MousePickerColor.colorToID_list(data, pixel)
                    
                    if pick_result != None:
                        selected_pixels.append(pick_result)
                        break
        
        if len(selected_pixels) <= 0:
            print("nothing found")
            self.lines.clearLines()
            return
        
        # Test Files
        # 9383 <Point3D 'xyz=[0.0222964  0.811361  0.574178], track_length=3, error=0.276763'> [0.02229639 0.8113615  0.57417846]
        # 4073 vec3(    0.0222964,     0.811361,     0.574178 )
        # Three Cameras (x x 0 x)
        #selected_pixels = [MousePickInfo(0, 0, 4073)]
        self.lines.clearLines()
        
        # Add To Result Window (tmp_list)
        piig_list = []
        
        # Vertices to Coordinates & World to Image
        for mouse_pick in selected_pixels:
            project_id = 0
            sub_project_id = 0
            point_id = mouse_pick.vertex_id
            
            # Vertices to Coordinates
            project_opengl = self.opengl_project_data[project_id]
            sub_project_opengl = project_opengl.getSubProjects()[sub_project_id]
            
            vertices = sub_project_opengl.geometry_sparse.vertices.data
            point3D_glm = glm.vec3(vertices[point_id * 3], vertices[point_id * 3 + 1], vertices[point_id * 3 + 2])
            
            # World to Image
            project = self.projects[project_id]
            sub_project = project.getPyColmapProjects()[sub_project_id]
            
            point3d_id = None
            point3D = None
            for i, p in sub_project.points3D.items():
                pf = np.asarray(p.xyz, dtype=np.float32)
                if pf[0] == point3D_glm.x and pf[1] == point3D_glm.y and pf[2] == point3D_glm.z:
                    point3d_id = i
                    point3D = p
            
            if point3d_id == None:
                print("point3d_id not found")
                self.lines.clearLines()
                return
            
            for _, image in sub_project.images.items():
                if not image.has_point3D(point3d_id):
                    continue
                
                image_id = image.image_id
                camera_id = image.camera_id
                
                camera = sub_project.cameras[camera_id]
                
                vertices = sub_project_opengl.geometry_cameras[image_id].vertices.data
                point3D_camera = glm.vec3(vertices[0], vertices[1], vertices[2])
        
                # Create OpenGL Lines
                self.lines.addLine(glm.vec3(point3D_glm.x, -point3D_glm.y, -point3D_glm.z), glm.vec3(point3D_camera.x, -point3D_camera.y, -point3D_camera.z))
                
                # Add To Result Window
                piig_list.append([sub_project_opengl.project, camera, image, point3D])
        
        
        # Add Tab (Run Later in Qt-Thread)
        def lambda_window_tab():
            piig = PointInImageWidget()
            
            for piig_arg in piig_list:
                piig.addImage(piig_arg[0], piig_arg[1], piig_arg[2], piig_arg[3])
            
            window.ui.tabs.addTab(piig, f"ProjectName - {point3d_id}")
        QtFunctions.runLater(lambda_window_tab)
    
    def addProject(self, project: Project):
        self.projects.append(project)
        self.new_projects.append(project)
    
    def resize(self, width, height):
        self.width = width
        self.height = height
        self.sizeChanged = True
    
    def repaint(self):
        self.should_repaint = True
        self.repaintSignal.wakeAll()
    
    ######################
    ### Thread Methods ###
    ######################
    
    def start(self):
        self.running = True
        QThread.start(self)
    
    def stop(self):
        self.running = False
        
        self.mutex_repaintSignal.lock()
        self.repaintSignal.wakeAll()
        self.mutex_repaintSignal.unlock()
    
    def run(self):
        # Initialize
        self.__initialize()
        sleep_count = 0
        
        while self.running:
            self.should_repaint = False
            sleep_count = 0
            
            self.__render_steps()
            
            # wait is long sleep, so only go to wait if nessecary
            if not self.should_repaint:
                while sleep_count < 1000 and not self.should_repaint:
                    time.sleep(0.001)
                    sleep_count += 1
                
                if self.should_repaint:
                    continue
                
                self.mutex_repaintSignal.lock()
                if self.running:
                    self.repaintSignal.wait(self.mutex_repaintSignal)
                self.mutex_repaintSignal.unlock()
        
        self.__deinitialize()
    
    ##############
    ### OpenGL ###
    ##############
    
    def __render_steps(self, _ = None):
        self.context.makeCurrent(self.surface)
        
        self.__update()
        self.__render()
        
        self.context.doneCurrent()
    
    def __initialize(self):
        # Create Context
        self.context = QOpenGLContext()
        self.context.setFormat(self.format)
        self.context.setShareContext(self.context.globalShareContext())
        self.context.create()
        
        self.context.makeCurrent(self.surface)
        
        # OpenGL
        self.camera = OpenGLCamera()
        
        # Global storage
        global_storage = RenderDataStorages.getGloablRenderDataStorage()
        self.global_shader_storage = global_storage.getShaders()
        
        # Shaders
        self.shader_point_cloud_sparse = None
        self.shader_point_cloud_dense = None
        self.shader_images = None
        self.shader_coordinate_system = None
        
        # Geometries
        self.coordinate_system = Model()
        buffer_group = OpenGLBufferGroup.createBufferGroup(CoordinateSystem()) # TODO store coordinate_system buffer: global
        self.coordinate_system.addMeshes(OpenGLMesh(buffer_group))
        self.coordinate_system.getModelMatrix().scale(1000.0)
        
        # Point3D to Camera Lines
        self.lines = SelectionLines()
        
        # FrameBuffer
        self.framebuffer: FrameBuffer = OpenGLFrameBuffer()
        self.framebuffer.bind()
        
        # Texture: Output of the (3D-)View
        texture_data: TextureData = TextureData(TextureInternalFormat.RGBA, TextureFormat.RGBA, TextureType.UNSIGNED_BYTE, self.width, self.height, None)
        texture_data.setUseMipmap(False)
        texture_data.setRepeatImage(False)
        texture_data.setUnpackAlignment(False)
        texture_data.setPoorFiltering(True)
        
        self.outputTexture = OpenGLTexture(texture_data)
        self.framebuffer.addTexture(self.outputTexture)
        
        # Texture: Output of the MousePicking Color Texture
        texture_data: TextureData = TextureData(TextureInternalFormat.RGBA32UI, TextureFormat.RGBA_INTEGER, TextureType.UNSIGNED_INT, self.width, self.height, None)
        texture_data.setUseMipmap(False)
        texture_data.setRepeatImage(False)
        texture_data.setUnpackAlignment(False)
        texture_data.setPoorFiltering(True)
        
        self.outputMousePickingTexture = OpenGLTexture(texture_data)
        self.framebuffer.addTexture(self.outputMousePickingTexture)
        
        # Add Depth Buffer
        depth_buffer: RenderBuffer = OpenGLRenderBuffer(RenderBufferInternalFormat.DEPTH_COMPONENT, self.width, self.height)
        self.framebuffer.addRenderBuffer(depth_buffer)
        
        # Done Framebuffer
        self.framebuffer.setDrawBuffer(0, 1)
        self.framebuffer.unbind()
        
        # Done Context
        self.context.doneCurrent()
    
    def __deinitialize(self):
        self.context.makeCurrent(self.surface)
        
        # Delete Camera
        camera = self.camera
        self.camera = None
        del camera
        
        # Delete Objects
        del self.coordinate_system
        self.coordinate_system = None
        
        del self.framebuffer
        self.framebuffer = None
        
        del self.outputTexture
        self.outputTexture = None#
        
        del self.outputMousePickingTexture
        self.outputMousePickingTexture = None
        
        # Context Done
        self.context.doneCurrent()
        
        # Delete Context
        context = self.context
        self.context = None
        del context
    
    def __update(self):
        # Initialize
        if not self.shader_point_cloud_sparse and self.global_shader_storage.has("point_cloud_sparse"):
            self.shader_point_cloud_sparse = OpenGLProgramm(self.global_shader_storage.get("point_cloud_sparse"))
        
        if not self.shader_point_cloud_dense and self.global_shader_storage.has("point_cloud_dense"):
            self.shader_point_cloud_dense = OpenGLProgramm(self.global_shader_storage.get("point_cloud_dense"))
        
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
            
            cogl = ColmapProjectOpenGL(project)
            cogl.create()
            self.opengl_project_data.append(cogl)
        
        # Run Runnables
        while len(self.runnables) > 0:
            run = self.runnables.pop()
            run()
    
    def __render(self):
        # Start Binding
        self.framebuffer.bind()
        glViewport(0, 0, self.width, self.height);
        
        # Clear OpenGL Frame
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Enable OpenGL Settings
        glFrontFace(GL_CCW)
        glCullFace(GL_BACK)
        glEnable(GL_CULL_FACE)
        
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ZERO)
        
        # Draw Coordinate System
        if self.rw.setting_show_coordinate_system and self.shader_coordinate_system:
            self.shader_coordinate_system.bind()
            self.camera.updateShaderUniform(self.shader_coordinate_system)
            
            self.coordinate_system.bind(self.shader_coordinate_system)
            self.coordinate_system.draw()
            self.coordinate_system.unbind()
            
            self.shader_coordinate_system.unbind()
        
        # Draw Lines (Point3D to Camera)
        if self.shader_coordinate_system:
            self.shader_coordinate_system.bind()
            self.camera.updateShaderUniform(self.shader_coordinate_system)
            
            model = self.lines.getModel()
            model.bind(self.shader_coordinate_system)
            model.draw()
            model.unbind()
            
            self.shader_coordinate_system.unbind()
        
        # Draw Projects
        for project in self.opengl_project_data:
            for sub_project in project.getSubProjects():
                if self.shader_coordinate_system:
                    self.shader_coordinate_system.bind()
                    self.camera.updateShaderUniform(self.shader_coordinate_system)
                    
                    for cam in sub_project.cameras:
                        cam.bind(self.shader_coordinate_system)
                        cam.draw()
                        cam.unbind()
                    
                    self.shader_coordinate_system.unbind()
                
                # Draw Image
                if self.shader_images:
                    glDisable(GL_CULL_FACE)
                    self.shader_images.bind()
                    self.camera.updateShaderUniform(self.shader_images)
                    
                    for img in sub_project.images:
                        img.bind(self.shader_images)
                        img.draw()
                        img.unbind()
                    
                    self.shader_images.unbind()
                    glEnable(GL_CULL_FACE)
                
                # Draw Point Dense
                if self.shader_point_cloud_dense:
                    self.shader_point_cloud_dense.bind()
                    self.shader_point_cloud_dense.uniform("point_size", self.rw.point_size)
                    self.camera.updateShaderUniform(self.shader_point_cloud_dense)
                    
                    point_cloud = sub_project.point_cloud_dense
                    point_cloud.bind(self.shader_point_cloud_dense)
                    point_cloud.draw()
                    point_cloud.unbind()
                    
                    self.shader_point_cloud_dense.unbind()
        
        ### Clickable Objects
        # Draw Point Sparse
        if self.shader_point_cloud_sparse:
            self.shader_point_cloud_sparse.bind()
            self.shader_point_cloud_sparse.uniform("point_size", self.rw.point_size)
            self.camera.updateShaderUniform(self.shader_point_cloud_sparse)
            
            for project in self.opengl_project_data:
                for sub_project in project.getSubProjects():
                    point_cloud = sub_project.point_cloud_sparse
                    point_cloud.bind(self.shader_point_cloud_sparse)
                    point_cloud.draw()
                    point_cloud.unbind()
            
            self.shader_point_cloud_sparse.unbind()
        
        # Disable OpenGL Settings
        glDisable(GL_BLEND)
        glDisable(GL_CULL_FACE)
        glDisable(GL_VERTEX_PROGRAM_POINT_SIZE)
        glDisable(GL_DEPTH_TEST)
        
        # Finish Draw
        self.framebuffer.unbind()
        glFlush() # Start Rendering if it is not happend yet
        glFinish() # Wait for finished rendering
        
        #self.saveImage(GL_COLOR_ATTACHMENT0, 0)
        #self.saveImage(GL_COLOR_ATTACHMENT1, 1)
        
        # Send Signal for finishing
        self.rw.repaintSignal.emit(self.outputTexture)
        self.rw.mousePickingSignal.emit(self.outputMousePickingTexture)

    def saveImage(self, store = GL_COLOR_ATTACHMENT0, index = 0):
        self.framebuffer.bind()
        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        
        if store == GL_COLOR_ATTACHMENT0:
            glReadBuffer(GL_COLOR_ATTACHMENT0)
            data = glReadPixels(0, 0, self.width, self.height, GL_RGBA, GL_UNSIGNED_BYTE)
        else:
            glReadBuffer(GL_COLOR_ATTACHMENT1)
            data = glReadPixels(0, 0, self.width, self.height, GL_RGBA_INTEGER, GL_UNSIGNED_INT)
            data = np.asarray(data)
        
            with np.nditer(data, op_flags=['readwrite']) as it:
                for x in it:
                    x[...] = x % 255
            
            data = data.astype(np.ubyte)
        
        self.framebuffer.unbind()
        
        image = Image.frombytes("RGBA", (self.width, self.height), data)
        image = ImageOps.flip(image)
        image.save(f"J:\\Codes\\git\\BA_Trees\\config\\test{index}.png", 'PNG')