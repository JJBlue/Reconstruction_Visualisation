from pathlib import Path
import queue
import time
import glm
import numpy as np

from OpenGL.GL import *
from PIL import Image, ImageOps
from PyQt6.QtCore import QThread, QWaitCondition, QMutex
from PyQt6.QtGui import QOffscreenSurface, QOpenGLContext, QSurfaceFormat

from ba_trees.config.ConfigDirectories import ConfigDirectories
from ba_trees.gui.background.qt.QtFunctions import QtFunctions
from ba_trees.gui.image_pixel_widget import (PointInImageWidget, PointsInImageWidget)
from ba_trees.gui.project_widget.model_settings.ModelSettingCamera import ModelSettingCameraWidget
from ba_trees.gui.project_widget.render_structure.RenderGuiSettings import RenderGuiSetting
from ba_trees.gui.project_widget.render_structure.RenderObject import (RenderCollection, RenderModel, RenderMesh)
from ba_trees.workspace import Project
from ba_trees.workspace.colmap.ColmapOpenGL import ColmapProjectOpenGL

from render.data import CoordinateSystem, Primitves, PrimitiveType
from render.data.RenderBufferData import RenderBufferInternalFormat
from render.data.TextureData import TextureInternalFormat, TextureFormat, TextureType, TextureData
from render.functions.MousePickerColor import MousePickerColor
from render.opengl import OpenGLCamera, OpenGLMesh, OpenGLTexture, OpenGLFrameBuffer
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
        
        self.vbo_lines.setData(self.lines)
        self.vbo_lines.setMetaData(PrimitiveType.FLOAT, 3, self.amount)
        
        self.vbo_colors.setData(self.colors)
        self.vbo_colors.setMetaData(PrimitiveType.FLOAT, 3, self.amount)
        
        self.buffer_lines.count_vertices = self.amount
    
    def getModel(self):
        return self.model
    
class BackgroundRenderWidget(QThread):
    repaintSignal = QWaitCondition()
    mutex_repaintSignal = QMutex()
    
    def __init__(self, rw):
        super().__init__()
        
        self.snapshot = False
        
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
        
        self.opengl_project_data: list = []
        self.outputTexture = None
        
        self.mouse_picker = MousePickerColor()
        self.mouse_picker.id_bit_sizes =    {
                                                "project_id": 16,
                                                "sub_project_id": 16,
                                                "object_id": 16, # 0 = dense, 1 = sparse, 2...n = Camera/Image
                                                #"mesh_id": 0,
                                                #"primitive_id": 0,
                                                "vertex_id": 32
                                            }
        
        self.root_collection: RenderCollection = RenderCollection()
        self.root_collection.name = "Models"
        
        self.root_collection_background: RenderCollection = RenderCollection()
        self.root_collection_background.name = "Models"
        
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
                    pick_result = self.mouse_picker.colorToID_list(data, pixel)
                    
                    if pick_result != None:
                        selected_pixels.append(pick_result)
                        break
                
                if i == 0:
                    continue
                
                yt: int = y_center + i
                if yt < height:
                    pixel: int = yt * size + xt * color_size
                    pick_result = self.mouse_picker.colorToID_list(data, pixel)
                    
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
                    pick_result = self.mouse_picker.colorToID_list(data, pixel)
                    
                    if pick_result != None:
                        selected_pixels.append(pick_result)
                        break
                
                xt: int = x_center + i
                if xt < width:
                    pixel: int = yt * size + xt * color_size
                    pick_result = self.mouse_picker.colorToID_list(data, pixel)
                    
                    if pick_result != None:
                        selected_pixels.append(pick_result)
                        break
        
        self.lines.clearLines()
        if len(selected_pixels) <= 0:
            print("nothing found")
            return
        
        # Add To Result Window (tmp_list)
        piig_list = []
        psiig_list = []
        
        # Vertices to Coordinates & World to Image
        for mouse_pick in selected_pixels:            
            project_id = mouse_pick.project_id
            sub_project_id = mouse_pick.sub_project_id
            object_id = mouse_pick.object_id
            point_id = mouse_pick.vertex_id
            
            # Vertices to Coordinates
            project_opengl = self.opengl_project_data[project_id]
            sub_project_opengl = project_opengl.getSubProjects()[sub_project_id]
            sub_project = sub_project_opengl.project
            
            # Dense
            if object_id == 0:
                vertices = sub_project_opengl.geometry_dense.vertices.data
                _, sparse_id_nearest = sub_project_opengl.tree_sparse.query([[vertices[point_id * 3], vertices[point_id * 3 + 1], vertices[point_id * 3 + 2]]], k=1)
                
                # Set for next Step in Sparse
                object_id = 1
                point_id = sparse_id_nearest[0][0]
                object_id = 1
            
            # Sparse
            if object_id == 1:
                point3D_array = sub_project_opengl.tree_sparse_coords[point_id]
                _, point3d_id_nearest = sub_project_opengl.tree_point3d.query([point3D_array], k=1)
                point3d_id_nearest = point3d_id_nearest[0][0]
                
                # World to Image
                point3d_id = sub_project_opengl.tree_point3d_ids[point3d_id_nearest]
                point3D = sub_project_opengl.tree_point3d_points[point3d_id_nearest]
                
                if point3d_id == None:
                    print("point3d_id not found")
                    self.lines.clearLines()
                    return
                
                for _, image in sub_project.pycolmap.images.items():
                    if not image.has_point3D(point3d_id):
                        continue
                    
                    image_id = image.image_id
                    camera_id = image.camera_id
                    
                    camera = sub_project.pycolmap.cameras[camera_id]
                    
                    vertices = sub_project_opengl.geometry_cameras[image_id].vertices.data
                    point3D_camera = glm.vec3(vertices[0], vertices[1], vertices[2])
            
                    # Create OpenGL Lines
                    self.lines.addLine(glm.vec3(point3D_array[0], -point3D_array[1], -point3D_array[2]), glm.vec3(point3D_camera.x, -point3D_camera.y, -point3D_camera.z))
                    
                    # Add To Result Window
                    piig_list.append([sub_project, camera, image, point3D, point3d_id])
                
            # Camera/Images
            elif object_id >= 2:
                selected_image = None
                image = None
                
                i = 0
                for image_id, img in sub_project.reconstruction.images.items():
                    if i == object_id - 2:
                        selected_image = img
                    i += 1
                
                for image_id, img in sub_project.pycolmap.images.items():
                    if image_id == selected_image.id:
                        image = img
                
                camera_id = image.camera_id
                camera = sub_project.pycolmap.cameras[camera_id]
                
                psiig_list.append([sub_project, camera, image])
        
        if piig_list:
            # Add Tab (Run Later in Qt-Thread)
            def lambda_window_tab(piig_list=piig_list):
                piig = PointInImageWidget()
                point_id = None
                
                for piig_arg in piig_list:
                    piig.addImage(piig_arg[0], piig_arg[1], piig_arg[2], piig_arg[3])
                    point_id = piig_arg[4]
                    
                window.ui.tabs.addTab(piig, f"ProjectName - {point_id}")
            QtFunctions.runLater(lambda_window_tab)
        
        if psiig_list:
            # Add Tab (Run Later in Qt-Thread)
            def lambda_window_tab(psiig_list=psiig_list):
                for piig_arg in psiig_list:
                    piig = PointsInImageWidget()
                    piig.addImage(piig_arg[0], piig_arg[1], piig_arg[2])
                    window.ui.tabs.addTab(piig, f"ProjectName - {piig_arg[2].name}")
            QtFunctions.runLater(lambda_window_tab)
    
    def addProject(self, project: Project):
        # Add Project to OpenGL
        def __addProjectGL(project = project):
            cogl = ColmapProjectOpenGL(project)
            cogl.create(self.repaint)
            project_id = len(self.opengl_project_data)
            self.opengl_project_data.append(cogl)
            
            
            render_collection_project: RenderCollection = RenderCollection()
            render_collection_project.name = f"Project: {project.getProjectName()}"
            self.root_collection.childs.append(render_collection_project)
            
            sub_project_id = 0
            for sub_projects in cogl.getSubProjects():
                render_collection_sp: RenderCollection = RenderCollection()
                render_collection_sp.name = f"Subproject [{sub_project_id}]"
                render_collection_project.childs.append(render_collection_sp)
                
                def run_point_size():
                    return self.rw.point_size
                
                render_mesh: RenderModel = RenderModel()
                render_mesh.name = "Sparse Pointcloud"
                render_mesh.model = sub_projects.point_cloud_sparse
                render_mesh.shader_id = "point_cloud_sparse"
                render_mesh.shader_uniforms["point_size"] = run_point_size
                render_mesh.shader_uniforms["project_id"] = project_id
                render_mesh.shader_uniforms["sub_project_id"] = sub_project_id
                render_mesh.shader_uniforms["object_id"] = 1
                render_collection_project.childs.append(render_mesh)
                
                render_mesh: RenderModel = RenderModel()
                render_mesh.name = "Dense Pointcloud"
                render_mesh.model = sub_projects.point_cloud_dense
                render_mesh.shader_id = "point_cloud_dense"
                render_mesh.shader_uniforms["point_size"] = run_point_size
                render_mesh.shader_uniforms["project_id"] = project_id
                render_mesh.shader_uniforms["sub_project_id"] = sub_project_id
                render_mesh.shader_uniforms["object_id"] = 0
                render_collection_project.childs.append(render_mesh)
                
                
                render_collection_camera: RenderCollection = RenderCollection()
                render_collection_camera.name = f"Cameras"
                
                render_setting = RenderGuiSetting()
                render_setting.name = "Camera"
                render_setting.qt_create_gui = ModelSettingCameraWidget
                render_collection_camera.settings_gui.append(render_setting)
                
                render_collection_camera.values["sub_project"] = sub_projects
                
                render_collection_sp.childs.append(render_collection_camera)
                
                
                for camera_id in range(len(sub_projects.cameras)):
                    render_collection_camera_x: RenderCollection = RenderCollection()
                    render_collection_camera_x.name = f"Camera: {camera_id}"
                    render_collection_camera.childs.append(render_collection_camera_x)
                    
                    render_mesh: RenderModel = RenderModel()
                    render_mesh.name = f"Camera"
                    render_mesh.model = sub_projects.cameras[camera_id]
                    render_mesh.shader_id = "camera"
                    render_mesh.shader_uniforms["project_id"] = project_id
                    render_mesh.shader_uniforms["sub_project_id"] = sub_project_id
                    render_mesh.shader_uniforms["object_id"] = camera_id + 2
                    render_collection_camera_x.childs.append(render_mesh)
                    
                    render_mesh: RenderModel = RenderModel()
                    render_mesh.name = f"Image"
                    render_mesh.model = sub_projects.images[camera_id]
                    render_mesh.shader_id = "images"
                    render_mesh.shader_uniforms["project_id"] = project_id
                    render_mesh.shader_uniforms["sub_project_id"] = sub_project_id
                    render_mesh.shader_uniforms["object_id"] = camera_id + 2
                    render_collection_camera_x.childs.append(render_mesh)
            
                sub_project_id += 1
            
            self.rw.renderStructureChanged.emit(self.root_collection)
        
        self.runnables.append(__addProjectGL)
    
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
        self.__visit_queue = queue.Queue()
        
        # Create Context
        self.context = QOpenGLContext()
        self.context.setFormat(self.format)
        self.context.setShareContext(self.context.globalShareContext())
        self.context.create()
        
        self.context.makeCurrent(self.surface)
        
        # OpenGL
        self.camera = OpenGLCamera()
        
        
        
        # Geometries
        coordinate_system = Model()
        buffer_group = OpenGLBufferGroup.createBufferGroup(CoordinateSystem()) # TODO store coordinate_system buffer: global
        coordinate_system.addMeshes(OpenGLMesh(buffer_group))
        coordinate_system.getModelMatrix().scale(1000.0)
        
        
        render_model: RenderModel = RenderModel()
        render_model.name = "Coordinate System"
        render_model.model = coordinate_system
        render_model.shader_id = "coordinate_system"
        def run() -> bool:
            return self.rw.setting_show_coordinate_system
        render_model.visible = run
        self.render_model_coordinate_system = render_model
        self.root_collection_background.childs.append(render_model)
        
        # Point3D to Camera Lines
        self.lines = SelectionLines()
        
        render_model: RenderModel = RenderModel()
        render_model.name = "Lines"
        render_model.model = self.lines.model
        render_model.shader_id = "coordinate_system"
        self.root_collection.childs.append(render_model)
        
        
        self.rw.renderStructureChanged.emit(self.root_collection)
        
        
        # FrameBuffer
        self.framebuffer: FrameBuffer = OpenGLFrameBuffer()
        self.framebuffer.bind()
        
        # Texture: Output of the (3D-)View
        texture_data: TextureData = TextureData(TextureInternalFormat.RGBA, TextureFormat.RGBA, TextureType.UNSIGNED_BYTE, self.width, self.height, None)
        texture_data.setUseMipmap(False)
        texture_data.setRepeatImage(False)
        texture_data.setUnpackAlignment(False)
        texture_data.setPoorFiltering(True)
        
        self.outputTexture = OpenGLTexture()
        self.outputTexture.upload(texture_data)
        self.framebuffer.addTexture(self.outputTexture)
        
        # Texture: Output of the MousePicking Color Texture
        texture_data: TextureData = TextureData(TextureInternalFormat.RGBA32UI, TextureFormat.RGBA_INTEGER, TextureType.UNSIGNED_INT, self.width, self.height, None)
        texture_data.setUseMipmap(False)
        texture_data.setRepeatImage(False)
        texture_data.setUnpackAlignment(False)
        texture_data.setPoorFiltering(True)
        
        self.outputMousePickingTexture = OpenGLTexture()
        self.outputMousePickingTexture.upload(texture_data)
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
        # Resize
        if self.sizeChanged:
            self.sizeChanged = False
            self.framebuffer.resize(self.width, self.height)
            glViewport(0, 0, self.width, self.height)
        
        # Update Objects
        self.camera.update()
        
        # Run Runnables
        while len(self.runnables) > 0:
            run = self.runnables.pop()
            run()
    
    def __render(self):
        # Start Binding
        self.framebuffer.bind()
        glViewport(0, 0, self.width, self.height)
        
        # Clear OpenGL Frame
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Enable OpenGL Settings
        glFrontFace(GL_CCW)
        glCullFace(GL_BACK)
        #glEnable(GL_CULL_FACE)
        
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ZERO)
        
        self.__visit_queue.put(self.root_collection_background)
        self.__visit_queue.put(self.root_collection)
        
        tmp_render_structure: dict = {}
        
        while not self.__visit_queue.empty():
            render_object = self.__visit_queue.get()
            
            if not render_object.isVisible():
                continue
            
            if isinstance(render_object, RenderCollection):
                for child in render_object.childs:
                    self.__visit_queue.put(child)
            elif isinstance(render_object, RenderModel):
                model = render_object.model
                shader = render_object.getShader()
                
                if model == None or shader == None:
                    continue
                
                if not (shader in tmp_render_structure):
                    tmp_render_structure[shader] = {}
                
                if not (model in tmp_render_structure[shader]):
                    tmp_render_structure[shader][model] = []
                
                tmp_render_structure[shader][model].append(render_object)
            elif isinstance(render_object, RenderMesh):
                mesh = render_object.mesh
                shader = render_object.getShader()
                
                if model == None or shader == None:
                    continue
                
                if not (shader in tmp_render_structure):
                    tmp_render_structure[shader] = {}
                
                if not (mesh in tmp_render_structure[shader]):
                    tmp_render_structure[shader][mesh] = []
                
                tmp_render_structure[shader][mesh].append(render_object)
        
        
        for shader, ms in tmp_render_structure.items():
            shader.bind()
            self.camera.updateShaderUniform(shader)
            
            for m, render_objects in ms.items():
                if isinstance(render_object, RenderModel):
                    m.bind(shader)
                elif isinstance(render_object, RenderMesh):
                    m.bind()
                
                for render_object in render_objects:
                    render_object.setShaderUniforms()
                
                m.draw()
                m.unbind()
            
            shader.unbind()
        
        # Disable OpenGL Settings
        glDisable(GL_BLEND)
        glDisable(GL_CULL_FACE)
        glDisable(GL_VERTEX_PROGRAM_POINT_SIZE)
        glDisable(GL_DEPTH_TEST)
        
        # Finish Draw
        self.framebuffer.unbind()
        glFlush() # Start Rendering if it is not happend yet
        glFinish() # Wait for finished rendering
        
        if self.snapshot == True:
            self.snapshot = False
            self.saveImage(GL_COLOR_ATTACHMENT0, 0)
            self.saveImage(GL_COLOR_ATTACHMENT1, 1)
        
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
            
            for a1 in data:
                for a2 in a1:
                    if a2[0] != 0 or a2[1] != 0 or a2[2] != 0:
                        a2[3] = 255
            
            data = data.astype(np.ubyte)
        
        self.framebuffer.unbind()
        
        image = Image.frombytes("RGBA", (self.width, self.height), data)
        image = ImageOps.flip(image)
        
        screenshot_folder = Path(ConfigDirectories.getConfigDirectories().getConfigFolder()).joinpath("screenshots")
        screenshot_folder.mkdir(parents=True, exist_ok=True)
        screenshot_file = None
        i = 0
        
        while screenshot_folder.is_file() or screenshot_file == None:
            if index == 0:
                screenshot_file = screenshot_folder.joinpath(f"image{i}.png")
            elif index > 0:
                screenshot_file = screenshot_folder.joinpath(f"image{i} - RenderBuffer ({index}).png")
            
            i += 1
        
        image.save(f"{str(screenshot_file)}", 'PNG')
        