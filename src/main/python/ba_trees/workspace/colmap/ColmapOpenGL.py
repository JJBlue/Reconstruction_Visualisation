import numpy as np
import glm

from colmap_wrapper.colmap.camera import ImageInformation
from colmap_wrapper.visualization import draw_camera_viewport

from ba_trees.workspace.colmap import ColmapProject

from render.data import (GeometryO3DPointCloud, GeometryO3DLineSet, GeometryO3DTriangleMesh, TextureFile)
from render.opengl import OpenGLMesh, OpenGLTexture
from render.render import Model, Texture
from render.opengl.OpenGLBuffer import OpenGLBufferGroup


class ColmapProjectOpenGL:
    def __init__(self, project: ColmapProject):
        self.project = project
        self.sub_projects: list = []
        
        projs = self.project.getProjects()
        
        for sproject in projs:
            self.sub_projects.append(ColmapSubProjectOpenGL(sproject))
    
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
        
        self.point_cloud_dense = None
        self.point_cloud_sparse = None
        self.image_type = 'image'
        
        self.images: list = []
        self.cameras: list = []
        
        self.geometry_sparse = None
        self.geometry_cameras = {}
    
    def __del__(self):
        self.delete()
    
    def upload(self):
        pass
    
    def create(self):
        self.point_cloud_dense = Model()
        self.point_cloud_dense.getModelMatrix().scale(glm.fvec3(1, -1, -1))
        point_cloud_mesh = OpenGLMesh(OpenGLBufferGroup.createBufferGroup(GeometryO3DPointCloud(self.project.get_dense())))
        self.point_cloud_dense.addMeshes(point_cloud_mesh)
        
        self.point_cloud_sparse = Model()
        self.point_cloud_sparse.getModelMatrix().scale(glm.fvec3(1, -1, -1))
        self.geometry_sparse = GeometryO3DPointCloud(self.project.get_sparse()) # Saved for later usage (for example: Information for MouseClick)
        point_cloud_mesh = OpenGLMesh(OpenGLBufferGroup.createBufferGroup(self.geometry_sparse))
        self.point_cloud_sparse.addMeshes(point_cloud_mesh)
        
        
        for image_idx in self.project.images.keys():
            if image_idx % 10 == 0:
                print(f"Load Image: {image_idx}")
            
            image: ImageInformation = self.project.images[image_idx]
            image_data = np.asarray([], dtype=np.uint8)
            
            # line_set: Camera Viewport Outline
            # sphere: Camera Location
            # mesh: Image Plane
            line_set, sphere, mesh = draw_camera_viewport(
                                                            extrinsics=image.extrinsics,
                                                            intrinsics=image.intrinsics.K,
                                                            image=image_data,
                                                            scale=1
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
    
    def delete(self):
        # TODO delete buffers in Model
        del self.images[:]
        self.images.clear()
        
        # TODO delete buffers in Model
        del self.cameras[:]
        self.cameras.clear()