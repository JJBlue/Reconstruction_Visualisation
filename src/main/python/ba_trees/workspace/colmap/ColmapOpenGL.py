import glm
import numpy as np

from sklearn.neighbors import KDTree

from colmap_wrapper.colmap.camera import ImageInformation
from colmap_wrapper.visualization import draw_camera_viewport

from ba_trees.gui.background.opengl.OpenGLData import OpenGLData
from ba_trees.status_information import StatusInformation
from ba_trees.status_information.StatusInformation import (StatusInformationChild, Status, StatusInformations)
from ba_trees.workspace.colmap import ColmapProject

from render.data import (GeometryO3DPointCloud, GeometryO3DLineSet, GeometryO3DTriangleMesh, TextureFile)
from render.opengl import OpenGLMesh, OpenGLTexture
from render.opengl.OpenGLBuffer import OpenGLBufferGroup
from render.render import Model, Texture


class ColmapProjectOpenGL:
    def __init__(self, project: ColmapProject):
        self.project = project
        self.sub_projects: list = []
        
        projs = self.project.getProjects()
        
        for sub_project in projs:
            self.sub_projects.append(ColmapSubProjectOpenGL(self, sub_project))
    
    def upload(self):
        pass
    
    def create(self, repaintFunction = None):
        for project in self.sub_projects:
            project.create(repaintFunction)
    
    def delete(self):
        for project in self.sub_projects:
            project.delete()
    
    def getSubProjects(self) -> list:
        return self.sub_projects

class ColmapSubProjectOpenGL:
    def __init__(self, parent, project):
        self.parent = parent
        self.project = project
        
        self.image_type = 'image'
        
        self.mesh_images = {} # Meshes
        self.images: list = [] # Model
        
        self.geometry_cameras = {} # O3D GeometryData
        self.mesh_cameras = {} # Meshes
        self.cameras: list = [] # Model
        self.camera_scale = 0.4
        
        self.geometry_dense = None # O3D GeometryData
        self.point_cloud_dense = None # Model
        
        self.geometry_sparse = None # O3D GeometryData
        self.point_cloud_sparse = None # Model
        
        
        self.tree_sparse = None
        self.tree_sparse_coords = []
        
        self.tree_point3d = None
        self.tree_point3d_coords = []
        self.tree_point3d_points = []
        self.tree_point3d_ids = []
    
    def __del__(self):
        self.delete()
    
    def upload(self):
        pass
    
    def create(self, repaintFunction = None):
        reconstruction = self.project.reconstruction
        pycolmap = self.project.pycolmap
        
        
        status = StatusInformation()
        status.text = f"Upload OpenGL Data: {self.parent.project.getProjectName()}"
        
        status_dense_cloud = StatusInformationChild()
        status.add(status_dense_cloud)
        
        status_sparse_cloud = StatusInformationChild()
        status.add(status_sparse_cloud)
        
        status_images = StatusInformationChild()
        status.add(status_images)
        
        status_textures = StatusInformationChild()
        status.add(status_textures)
        
        StatusInformations.addStatus(status)
        
        # Create PyColmap Point3D KD-Tree
        self.tree_point3d_coords = []
        self.tree_point3d_points = []
        self.tree_point3d_ids = []
        for i, p in pycolmap.points3D.items():
            self.tree_point3d_coords.append([p.x, p.y, p.z])
            self.tree_point3d_points.append(p)
            self.tree_point3d_ids.append(i)
        
        self.tree_point3d = KDTree(self.tree_point3d_coords, leaf_size=2)


        
        # Dense Cloud
        status2 = StatusInformation()
        status2.text = f"Upload DenseCloud: {self.parent.project.getProjectName()}"
        status2.add(status_dense_cloud)
        StatusInformations.addStatus(status2)
        status_dense_cloud.setStatus(Status.STARTED)
        
        self.point_cloud_dense = Model()
        self.point_cloud_dense.getModelMatrix().scale(glm.fvec3(1, -1, -1))
        self.geometry_dense = GeometryO3DPointCloud(reconstruction.get_dense())
        point_cloud_mesh = OpenGLMesh(OpenGLBufferGroup.createBufferGroup(self.geometry_dense))
        self.point_cloud_dense.addMeshes(point_cloud_mesh)
        
        # https://towardsdatascience.com/5-step-guide-to-generate-3d-meshes-from-point-clouds-with-python-36bad397d8ba
        # http://www.open3d.org/docs/release/python_api/open3d.geometry.TriangleMesh.html
        #point_cloud = reconstruction.get_dense()
        #poisson_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(point_cloud, depth=8, width=0, scale=1.1, linear_fit=False)[0]
        #bbox = point_cloud.get_axis_aligned_bounding_box()
        #p_mesh_crop = poisson_mesh.crop(bbox)
        
        #opengl_mesh = OpenGLMesh(OpenGLBufferGroup.createBufferGroup(GeometryO3DTriangleMesh(p_mesh_crop)))
        #self.point_cloud_dense.addMeshes(opengl_mesh)
        
        status_dense_cloud.setStatus(Status.FINISHED)
        
        
        # Sparse Cloud
        status2 = StatusInformation()
        status2.text = f"Upload SparseCloud: {self.parent.project.getProjectName()}"
        status2.add(status_sparse_cloud)
        StatusInformations.addStatus(status2)
        status_sparse_cloud.setStatus(Status.STARTED)
        
        # Create KD-Tree
        self.tree_sparse_coords = np.asarray(reconstruction.get_sparse().points)
        self.tree_sparse = KDTree(self.tree_sparse_coords, leaf_size=2)
        
        # Create OpenGL
        self.point_cloud_sparse = Model()
        self.point_cloud_sparse.getModelMatrix().scale(glm.fvec3(1, -1, -1))
        self.geometry_sparse = GeometryO3DPointCloud(reconstruction.get_sparse()) # Saved for later usage (for example: Information for MouseClick)
        point_cloud_mesh = OpenGLMesh(OpenGLBufferGroup.createBufferGroup(self.geometry_sparse))
        self.point_cloud_sparse.addMeshes(point_cloud_mesh)
        
        status_sparse_cloud.setStatus(Status.FINISHED)
        
        
        # Textures / Images / Cameras
        status2 = StatusInformation()
        status2.text = f"Upload Camera / Image: {self.parent.project.getProjectName()}"
        status2.add(status_images)
        StatusInformations.addStatus(status2)
        status_images.setStatus(Status.STARTED)
        
        status_texture = StatusInformation()
        status_texture.text = f"Upload Texture {self.parent.project.getProjectName()}"
        
        for image_idx in reconstruction.images.keys():
            image: ImageInformation = reconstruction.images[image_idx]
            image_data = np.asarray([], dtype=np.uint8)
            
            # line_set: Camera Viewport Outline
            # sphere: Camera Location
            # mesh: Image Plane
            line_set, sphere, mesh = draw_camera_viewport(
                                                            extrinsics=image.extrinsics,
                                                            intrinsics=image.intrinsics.K,
                                                            image=image_data,
                                                            scale=self.camera_scale
                                                         )
            
            texture: Texture = OpenGLTexture()
            
            status_texture_child = StatusInformationChild()
            status_texture.add(status_texture_child)
            def uploadTexture(texture = texture, repaintFunction = repaintFunction, status_texture_child = status_texture_child):
                status_texture_child.setStatus(Status.STARTED)
                #from pathlib import Path
                #from PIL import Image
                #from colmap_wrapper.colmap import read_array
                #from render.data import TexturePILImage
                #import cv2
                
                #path = Path(image.path.parent.parent, f"stereo/depth_maps/{image.name}.photometric.bin")
                
                #image_data = read_array(path)
                
                #min_depth, max_depth = np.percentile(image_data, [5, 95])
                #image_data[image_data < min_depth] = min_depth
                #image_data[image_data > max_depth] = max_depth
                #image_data = cv2.cvtColor(image_data, cv2.COLOR_GRAY2BGR)
                #image_data = (image_data / reconstruction.max_depth_scaler_photometric * 255).astype(np.uint8)
                #image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)
                #img = Image.fromarray(image_data, "RGB")
                
                #texture.upload(TexturePILImage(img))
                texture.upload(TextureFile(image.path))
                status_texture_child.setStatus(Status.FINISHED)
                
                if status_texture.isFinished():
                    status_textures.setStatus(Status.FINISHED)
                
                if repaintFunction:
                    repaintFunction()
            OpenGLData.runLater(uploadTexture)
            
            image_model = Model()
            image_model.getModelMatrix().scale(glm.fvec3(1, -1, -1))
            image_mesh = OpenGLMesh(OpenGLBufferGroup.createBufferGroup(GeometryO3DTriangleMesh(mesh)))
            self.mesh_images[image_idx] = image_mesh
            image_model.addMeshes(image_mesh)
            image_model.addTexture(texture)
            self.images.append(image_model)
            
            camera = Model()
            camera.getModelMatrix().scale(glm.fvec3(1, -1, -1))
            geometry_lines = GeometryO3DLineSet(line_set)
            self.geometry_cameras[image_idx] = geometry_lines
            camera_mesh = OpenGLMesh(OpenGLBufferGroup.createBufferGroup(geometry_lines))
            self.mesh_cameras[image_idx] = camera_mesh
            camera.addMeshes(camera_mesh)
            
            for s in sphere:
                camera.addMeshes(OpenGLMesh(OpenGLBufferGroup.createBufferGroup(GeometryO3DTriangleMesh(s))))
            
            self.cameras.append(camera)
        
        status_images.setStatus(Status.FINISHED)
        StatusInformations.addStatus(status_texture)
        
    def reupload(self, camera_scale = 0.4):
        if self.camera_scale == camera_scale:
            return
        
        self.camera_scale = camera_scale
        reconstruction = self.project.reconstruction
        
        for image_idx in reconstruction.images.keys():
            image: ImageInformation = reconstruction.images[image_idx]
            image_data = np.asarray([], dtype=np.uint8)
            
            # line_set: Camera Viewport Outline
            # sphere: Camera Location
            # mesh: Image Plane
            line_set, _, mesh = draw_camera_viewport(
                                                            extrinsics=image.extrinsics,
                                                            intrinsics=image.intrinsics.K,
                                                            image=image_data,
                                                            scale=camera_scale
                                                         )
            
            # image_model reupload
            mesh_image = self.mesh_images[image_idx]
            OpenGLBufferGroup.reupload_GeometryToMesh(mesh_image, GeometryO3DTriangleMesh(mesh))
            
            # camera.mesh reupload
            mesh_camera = self.mesh_cameras[image_idx]
            geometry_lines = GeometryO3DLineSet(line_set)
            self.geometry_cameras[image_idx] = geometry_lines
            OpenGLBufferGroup.reupload_GeometryToMesh(mesh_camera, geometry_lines)
    
    def getCameraScale(self) -> float:
        return self.camera_scale
    
    def delete(self):
        # TODO delete buffers in Model
        del self.images[:]
        self.images.clear()
        
        # TODO delete buffers in Model
        del self.cameras[:]
        self.cameras.clear()