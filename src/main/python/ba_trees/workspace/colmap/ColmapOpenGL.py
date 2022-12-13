from colmap_wrapper.visualization import draw_camera_viewport

from ba_trees.workspace.colmap import ColmapProject
from render.data import GeometryO3DPointCloud
from render.data.GeometryO3D import GeometryO3DLineSet, GeometryO3DTriangleMesh
from render.opengl import OpenGLModel


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
        self.point_cloud_dense = OpenGLModel()
        self.point_cloud_dense.addGeometries(GeometryO3DPointCloud(self.project.get_dense()))
        
        self.point_cloud_sparse = OpenGLModel()
        self.point_cloud_sparse.addGeometries(GeometryO3DPointCloud(self.project.get_sparse()))
        
        
        for image_idx in self.project.images.keys():
            image = self.project.images[image_idx]
            #image = image.getData(self.project.image_resize)
            image_data = None
            
            line_set, sphere, mesh = draw_camera_viewport(
                                                            extrinsics=image.extrinsics,
                                                            intrinsics=image.intrinsics.K,
                                                            image=image_data,
                                                            scale=1
                                                         )
            
            
            #image_model = OpenGLModel()
            #image_model.addGeometries(GeometryO3DTriangleMesh(mesh))
            #image_model.addTexture(OpenGLTexture(TextureDataFile(image)))
            #self.images.append(image_model)
            
            camera = OpenGLModel()
            camera.addGeometries(GeometryO3DLineSet(line_set))
            #camera.addGeometries(GeometryO3DTriangleMesh(sphere)) # is list
            
            self.cameras.append(camera)