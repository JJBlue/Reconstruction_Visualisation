import glm
import numpy as np

from colmap_wrapper.colmap.camera import ImageInformation
from colmap_wrapper.visualization import draw_camera_viewport

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
            self.sub_projects.append(ColmapSubProjectOpenGL(sub_project))
    
    def upload(self):
        pass
    
    def create(self):
        for project in self.sub_projects:
            project.create()
            break # TODO
    
    def delete(self):
        for project in self.sub_projects:
            project.delete()
            break # TODO
    
    def getSubProjects(self) -> list:
        return self.sub_projects

class ColmapSubProjectOpenGL:
    def __init__(self, project):
        self.project = project
        
        self.image_type = 'image'
        
        self.mesh_images = {} # Meshes
        self.images: list = [] # Model
        
        self.geometry_cameras = {} # O3D GeometryData
        self.mesh_cameras = {} # Meshes
        self.cameras: list = [] # Model
        
        self.geometry_dense = None # O3D GeometryData
        self.point_cloud_dense = None # Model
        
        self.geometry_sparse = None # O3D GeometryData
        self.point_cloud_sparse = None # Model
        
        
    
    def __del__(self):
        self.delete()
    
    def upload(self):
        pass
    
    def create(self):
        reconstruction = self.project.reconstruction
        
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
        
        
        self.point_cloud_sparse = Model()
        self.point_cloud_sparse.getModelMatrix().scale(glm.fvec3(1, -1, -1))
        self.geometry_sparse = GeometryO3DPointCloud(reconstruction.get_sparse()) # Saved for later usage (for example: Information for MouseClick)
        point_cloud_mesh = OpenGLMesh(OpenGLBufferGroup.createBufferGroup(self.geometry_sparse))
        self.point_cloud_sparse.addMeshes(point_cloud_mesh)
        
        
        for image_idx in reconstruction.images.keys():
            if image_idx % 10 == 0:
                print(f"Load Image: {image_idx}")
            
            image: ImageInformation = reconstruction.images[image_idx]
            image_data = np.asarray([], dtype=np.uint8)
            
            # line_set: Camera Viewport Outline
            # sphere: Camera Location
            # mesh: Image Plane
            line_set, sphere, mesh = draw_camera_viewport(
                                                            extrinsics=image.extrinsics,
                                                            intrinsics=image.intrinsics.K,
                                                            image=image_data,
                                                            scale=0.4
                                                         )
            
            texture: Texture = OpenGLTexture(TextureFile(image.path))
            
            image_model = Model()
            image_model.getModelMatrix().scale(glm.fvec3(1, -1, -1))
            image_model.addMeshes(OpenGLMesh(OpenGLBufferGroup.createBufferGroup(GeometryO3DTriangleMesh(mesh))))
            image_model.addTexture(texture)
            self.images.append(image_model)
            
            camera = Model()
            camera.getModelMatrix().scale(glm.fvec3(1, -1, -1))
            geometry_lines = GeometryO3DLineSet(line_set)
            self.geometry_cameras[image_idx] = geometry_lines
            camera.addMeshes(OpenGLMesh(OpenGLBufferGroup.createBufferGroup(geometry_lines)))
            
            for s in sphere:
                camera.addMeshes(OpenGLMesh(OpenGLBufferGroup.createBufferGroup(GeometryO3DTriangleMesh(s))))
            
            self.cameras.append(camera)
    
    def reupload(self, camera_scale = 0.4):
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
            mesh_image = self.mesh_images[image_idx] # TODO set self.mesh_images
            OpenGLBufferGroup.reupload_GeometryToMesh(mesh_image, GeometryO3DTriangleMesh(mesh))
            
            # camera.mesh reupload
            mesh_camera = self.mesh_cameras[image_idx] # TODO set self.mesh_cameras
            geometry_lines = GeometryO3DLineSet(line_set)
            self.geometry_cameras[image_idx] = geometry_lines
            OpenGLBufferGroup.reupload_GeometryToMesh(mesh_camera, geometry_lines)
    
    def delete(self):
        # TODO delete buffers in Model
        del self.images[:]
        self.images.clear()
        
        # TODO delete buffers in Model
        del self.cameras[:]
        self.cameras.clear()