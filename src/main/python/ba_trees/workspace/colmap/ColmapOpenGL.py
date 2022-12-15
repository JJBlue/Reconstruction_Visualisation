import numpy as np

from colmap_wrapper.visualization import draw_camera_viewport

from ba_trees.workspace.colmap import ColmapProject

from render.data import GeometryO3DPointCloud, GeometryO3DLineSet, GeometryO3DTriangleMesh
from render.opengl import OpenGLMesh
from render.render import Model


class ColmapProjectOpenGL:
    def __init__(self, project: ColmapProject):
        self.project = project
        self.sub_projects: list = []
        
        projs = self.project.getProjects()
        if not isinstance(projs, list):
            projs = []
            projs.append(self.project.getProjects())
        
        for sproject in projs:
            self.sub_projects.append(ColmapSubProjectOpenGL(sproject))
    
    def create(self):
        for project in self.sub_projects:
            project.create()
            break # TODO
    
    def delete(self):
        for project in self.sub_projects:
            project.delete()
            break # TODO
    
    def getSubProjects(self):
        return self.sub_projects

class ColmapSubProjectOpenGL:
    def __init__(self, project):
        self.project = project
        
        self.point_cloud_dense = None
        self.point_cloud_sparse = None
        self.image_type = 'image'
        
        self.images: list = []
        self.cameras: list = []
    
    def create(self):
        self.point_cloud_dense = Model()
        self.point_cloud_dense.addMeshes(OpenGLMesh(GeometryO3DPointCloud(self.project.get_dense())))
        
        self.point_cloud_sparse = Model()
        self.point_cloud_sparse.addMeshes(OpenGLMesh(GeometryO3DPointCloud(self.project.get_sparse())))
        
        
        for image_idx in self.project.images.keys():
            image = self.project.images[image_idx]
            #image_data = image.getData(self.project.image_resize)
            image_data = np.asarray([]).astype('uint8')
            
            # line_set: Camera Viewport Outline
            # sphere: ?
            # mesh: Image Plane
            line_set, sphere, mesh = draw_camera_viewport(
                                                            extrinsics=image.extrinsics,
                                                            intrinsics=image.intrinsics.K,
                                                            image=image_data,
                                                            scale=1
                                                         )
            
            
            image_model = Model()
            image_model.addMeshes(OpenGLMesh(GeometryO3DTriangleMesh(mesh)))
            #image_model.addTexture(OpenGLTexture(TextureDataFile(image)))
            self.images.append(image_model)
            
            camera = Model()
            camera.addMeshes(OpenGLMesh(GeometryO3DLineSet(line_set)))
            
            for s in sphere:
                camera.addMeshes(OpenGLMesh(GeometryO3DTriangleMesh(s)))
            
            self.cameras.append(camera)
    
    def delete(self):
        # TODO delete buffers in Model
        del self.images[:]
        self.images.clear()
        
        # TODO delete buffers in Model
        del self.cameras[:]
        self.cameras.clear()