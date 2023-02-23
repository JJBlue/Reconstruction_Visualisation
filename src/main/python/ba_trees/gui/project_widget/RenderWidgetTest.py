from pathlib import Path

from OpenGL.GL import *
from PIL import Image
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from colmap_wrapper.visualization.visualization import draw_camera_viewport
import glm

from ba_trees.config.ConfigDirectories import ConfigDirectories
from ba_trees.gui.background.opengl.OpenGLData import OpenGLData
from ba_trees.workspace.colmap.ColmapProject import ColmapProject
import numpy as np
from render.data import Geometry
from render.data.Geometry import GeometryData
from render.data.GeometryO3D import GeometryO3DLineSet, GeometryO3DTriangleMesh
from render.data.PrimitiveTypes import PrimitiveType, Primitves
from render.opengl import OpenGLMesh, OpenGLProgramm, OpenGLCamera, OpenGLBufferGroup, OpenGLShader
from render.render import Model
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
        
        
        subproject = self.project.getProjects()[0]
        
        
        self.images = []
        
        for image in subproject.reconstruction.images.values():
            if len(self.images) >= 2:
                break
            
            data = {}
            self.images.append(data)
            data["image"] = image
            
            #depth_map = image.depth_image_photometric
            depth_map = image.depth_image_geometric
            
            with Image.open(image.path) as img:
                width, height = img.size
                
                data["width"] = width
                data["height"] = height
                
                if len(depth_map) != height or len(depth_map[0]) != width:
                    print(f"Resize Org: {(width, height)} New: {(len(depth_map[0]), len(depth_map))}")
                    img = img.resize((len(depth_map[0]), len(depth_map)))
                
                color = np.asarray(img).astype(np.uint8)
            
            #self.saveImageGrayScale(depth_map, subproject.reconstruction.max_depth_scaler_photometric)
            self.saveImageGrayScale(depth_map, subproject.reconstruction.max_depth_scaler)
            
            
            #color = image.getData(1.0)
            data["color"] = color
            
            
            depth = depth_map
            data["depth"] = depth
            
            extrinsics = image.extrinsics
            intrinsics = image.intrinsics.K
            
            #print(image.name)
            #print(image.extrinsics)
            #print()
            #print(image.intrinsics.K)
            #print()
            
            
            mat_extrinsics = glm.mat4x4(1.0)
            row = 0
            for array_row in subproject.pycolmap.images[image.id].projection_matrix(): # TODO to extrinsics
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
            
            
            #print(mat_extrinsics)
            #print()
            #print(mat_intrinsics)
            #print()
            #print(mat_extrinsics_inverse)
            #print()
            #print(mat_intrinsics_inverse)
            #print()
            
            vec = glm.vec4(-2.02027431, -0.76609883,  0.96236055, 1.0)
            print(f"Vec:\t\t{vec}")
            camera_vec = mat_extrinsics @ vec
            print(f"Camera Vec:\t{camera_vec}")
            image_plane = mat_intrinsics @ camera_vec
            print(f"Image:\t\t{image_plane}")
            depth = image_plane.z
            image_uv = glm.vec2(image_plane.xy) / depth
            print(f"UV:\t\t{image_uv}")
            print()
            
            vec = depth * mat_extrinsics_inverse @ glm.mat4x4(mat_intrinsics_inverse) @ glm.vec4(image_uv.xy, 1.0, 1.0/depth)
            print(f"org:\t\t{vec}")
            print()
        
        #exit(0)
        # (https://www.imatest.com/support/docs/pre-5-2/geometric-calibration-deprecated/projective-camera/)
        # https://medium.com/yodayoda/from-depth-map-to-point-cloud-7473721d3f
    
    # image = depth_photo
    # self.photogrammetry_software.max_depth_scaler_photometric
    def saveImageGrayScale(self, depth_photo, max_depth_scaler):
        import cv2
        import copy
        
        image = copy.deepcopy(depth_photo)
        
        min_depth, max_depth = np.percentile(image, [5, 95])
        image[image < min_depth] = min_depth
        image[image > max_depth] = max_depth
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        image = (image / max_depth_scaler * 255).astype(np.uint8)
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
        image = Image.frombytes("RGBA", (len(image[0]), len(image)), image)
        #image = ImageOps.flip(image)
        
        screenshot_folder = Path(ConfigDirectories.getConfigDirectories().getConfigFolder()).joinpath("screenshots")
        screenshot_folder.mkdir(parents=True, exist_ok=True)
        screenshot_file = None
        i = 0
        
        while screenshot_file == None or screenshot_file.is_file():
            screenshot_file = screenshot_folder.joinpath(f"image{i} - DepthMap.png")
            i += 1
        
        image.save(f"{str(screenshot_file)}", 'PNG')
    
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
            
            width = data["width"]
            height = data["height"]
            
            lists = []
            for u in range(len(depth)):
                for v in range(len(depth[0])):
                    lists.append([v * (width / len(depth[0])), u * (height / len(depth))])
            
            data_uv = GeometryData(2, np.asarray(lists).flatten().astype(np.float32), PrimitiveType.FLOAT)
            data_depth = GeometryData(1, depth.flatten().astype(np.float32), PrimitiveType.FLOAT)
            data_color = GeometryData(3, color.flatten().astype(np.float32), PrimitiveType.FLOAT)
            
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
            
            
            
            
            image_data = np.asarray([], dtype=np.uint8)
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