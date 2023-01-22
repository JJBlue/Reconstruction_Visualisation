from pathlib import Path

from OpenGL.GL import *
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from colmap_wrapper.visualization.visualization import draw_camera_viewport
import glm
import numpy
from numpy.array_api._data_type_functions import astype

from ba_trees.gui.background.opengl.OpenGLData import OpenGLData
from ba_trees.workspace.colmap.ColmapProject import ColmapProject
from render.data import Geometry
from render.data.Geometry import GeometryData
from render.data.GeometryO3D import GeometryO3DLineSet, GeometryO3DTriangleMesh
from render.data.GeometryStructures import Cube
from render.data.PrimitiveTypes import PrimitiveType, Primitves
from render.functions import RenderDataStorages
from render.opengl import OpenGLMesh, OpenGLProgramm, OpenGLCamera, OpenGLBufferGroup, \
    OpenGLShader
from render.render import Texture, Model
from render.render.Shader import ShaderGroup


class RenderWidgetTest(QOpenGLWidget):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        
        # Widget Settings
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus) # Must be set for keyPressEvent to work
        self.setMouseTracking(True) # To track Mouse Move without click event
        
        # Settings
        self.mouse_pressed: bool = False
        self.mouse_x: float = -1
        self.mouse_y: float = -1
        
        self.projects: list = []
        
        self.setting_show_coordinate_system = True
        self.point_size = 1.0
        
        self.camera_speed: float = 0.1
        self.camera_enable_movement_speed: bool = True
        
        self.project = ColmapProject(Path("J:/Codes/git/BA_Trees/config/workspace/bunny"))
        self.project.open()
        self.project.load()
        
        
        subproject = self.project.getProjects()[0].reconstruction
        
        
        self.images = []
        
        for image in subproject.images.values():
            if len(self.images) >= 2:
                break
            
            data = {}
            self.images.append(data)
            data["image"] = image
            
            color = image.getData(1.0)
            data["color"] = color
            
            #depth = self.image.depth_image_photometric
            depth = image.depth_image_geometric
            data["depth"] = depth
            
            extrinsics = image.extrinsics
            intrinsics = image.intrinsics.K
            
            
            #print(image.name)
            #print(image.extrinsics)
            #print()
            #print(image.intrinsics.K)
            #print()
            
            # Extrinsic parameters
            #R, t = extrinsics[:3, :3], extrinsics[:3, 3]
            # intrinsic points
            #fx, fy, cx, cy = intrinsics[0, 0], intrinsics[1, 1], intrinsics[0, 2], intrinsics[1, 2]
            
            
            
            
            mat_extrinsics = glm.mat4x4(1.0)
            row = 0
            for array_row in extrinsics:
                column = 0
                for value in array_row:
                    mat_extrinsics[column][row] = value
                    column += 1
                row += 1
            
            mat_intrinsics = glm.mat3x3(1.0)
            row = 0
            for array_row in intrinsics:
                column = 0
                for value in array_row:
                    mat_intrinsics[column][row] = value
                    column += 1
                row += 1
            
            
            mat_extrinsics_inverse = glm.inverse(mat_extrinsics)
            data["mat_extrinsics_inverse"] = mat_extrinsics_inverse
            
            mat_intrinsics_inverse = glm.mat3x4(glm.inverse(mat_intrinsics))
            data["mat_intrinsics_inverse"] = mat_intrinsics_inverse
            
            mat_intrinsics = glm.mat4x3(mat_intrinsics)
            
            
            print(mat_extrinsics)
            print()
            print(mat_intrinsics)
            print()
            #print(mat_extrinsics_inverse)
            #print()
            #print(mat_intrinsics_inverse)
            #print()
            
            #R, t = extrinsics[:3, :3], extrinsics[:3, 3]
            
            # -0.20903162 0.69027902 0.59727322
            # ~ 464 311
            
            
            #vec = glm.vec4(-0.20903162, 0.69027902, 0.59727322, 1.0)
            #vec = glm.vec4(-0.08, 0.39, 0.38, 1.0)
            #print(f"Vec:\t\t{vec}")
            #camera_vec = mat_extrinsics * vec
            #print(f"Camera Vec:\t{camera_vec}")
            #image_plane = mat_intrinsics * camera_vec
            #print(f"Image:\t\t{image_plane}")
            #print()
            
            
            #camera_vec = mat_intrinsics_inverse * image_plane
            #print(f"org1:\t\t{camera_vec}")
            #vec = mat_extrinsics_inverse * glm.vec4(camera_vec.xyz, 1.0)
            #print(f"org2:\t\t{vec}")
            #exit(0)
        
    
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
        
        if self.camera != None:
            self.camera.forward(delta * self.camera_speed)
            self.repaint()
    
    def mousePickingTextureChanged(self, texture):
        self.mousePickingTexture = texture
    
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
    
    ##############
    ### OpenGL ###
    ##############
    def repaintObject(self, value):
        self.outputTexture = value
        self.repaint()
    
    def initializeGL(self)->None:
        super().initializeGL()
        
        self.camera = OpenGLCamera()
        
        # Shaders
        shader_vert = OpenGLShader(OpenGLData.getShaderFile(GL_VERTEX_SHADER, "camera.vert"))
        shader_frag = OpenGLShader(OpenGLData.getShaderFile(GL_FRAGMENT_SHADER, "camera.frag"))
        shadergroup = ShaderGroup(shader_vert, shader_frag)
        self.shader_cam = OpenGLProgramm(shadergroup)
        
        shader_vert = OpenGLShader(OpenGLData.getShaderFile(GL_VERTEX_SHADER, "depth.vert"))
        shader_frag = OpenGLShader(OpenGLData.getShaderFile(GL_FRAGMENT_SHADER, "depth.frag"))
        shadergroup = ShaderGroup(shader_vert, shader_frag)
        self.shader = OpenGLProgramm(shadergroup)
        
        
        for data in self.images:
            depth = data["depth"]
            color = data["color"]
            image = data["image"]
            
            lists = []
            for u in range(len(depth)):
                for v in range(len(depth[0])):
                    lists.append([v, u])
            
            data_uv = GeometryData(2, numpy.asarray(lists).flatten().astype(numpy.float32), PrimitiveType.FLOAT)
            data_depth = GeometryData(1, depth.flatten().astype(numpy.float32), PrimitiveType.FLOAT)
            data_color = GeometryData(3, color.flatten().astype(numpy.float32), PrimitiveType.FLOAT)
            
            geo = Geometry()
            geo.primtive = Primitves.POINTS
            
            geo.uv = data_uv
            geo.all_vertices.append(geo.uv)
            
            geo.depth = data_depth
            geo.all_vertices.append(geo.depth)
            
            geo.color = data_color
            geo.all_vertices.append(geo.color)
            
            mesh = OpenGLMesh(OpenGLBufferGroup.createBufferGroup(geo))
            data["mesh"] = mesh
            
            
            
            
            image_data = numpy.asarray([], dtype=numpy.uint8)
            line_set, sphere, _ = draw_camera_viewport(
                                                                extrinsics=image.extrinsics,
                                                                intrinsics=image.intrinsics.K,
                                                                image=image_data,
                                                                scale=1.0
                                                             )
            
            cam = Model()
            #cam.getModelMatrix().scale(glm.fvec3(1, -1, -1))
            camera_mesh = OpenGLMesh(OpenGLBufferGroup.createBufferGroup(GeometryO3DLineSet(line_set)))
            cam.addMeshes(camera_mesh)
            
            for s in sphere:
                cam.addMeshes(OpenGLMesh(OpenGLBufferGroup.createBufferGroup(GeometryO3DTriangleMesh(s))))
            data["cam"] = cam
        
    
    def paintGL(self):
        super().paintGL()
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glFrontFace(GL_CCW)
        glCullFace(GL_BACK)
        glEnable(GL_CULL_FACE)
        
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ZERO)
        
        glPointSize(1.0)
        
        self.camera.update()
        
        self.shader_cam.bind()
        self.camera.updateShaderUniform(self.shader_cam)
        for data in self.images:
            cam = data["cam"]
            cam.bind(self.shader_cam)
            cam.draw()
            cam.unbind()
            
        self.shader_cam.unbind()
        
        
        
        self.shader.bind()
        self.camera.updateShaderUniform(self.shader)
        for data in self.images:
            mesh = data["mesh"]
            mat_extrinsics_inverse = data["mat_extrinsics_inverse"]
            mat_intrinsics_inverse = data["mat_intrinsics_inverse"]
            
            #self.shader.uniform("extrinsics", self.mat_extrinsics)
            #self.shader.uniform("intrinsics", self.mat_intrinsics)
            self.shader.uniform("extrinsics", mat_extrinsics_inverse)
            self.shader.uniform("intrinsics", mat_intrinsics_inverse)
            
            mesh.bind()
            mesh.draw()
            mesh.unbind()
        
        self.shader.unbind()