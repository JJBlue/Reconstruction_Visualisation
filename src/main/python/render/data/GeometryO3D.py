import numpy as np
import open3d as o3d

from render.data import Geometry, GeometryData
from render.render import PrimitiveType, Primitves


class GeometryO3DPointCloud(Geometry):
    def __init__(self, point_cloud: o3d.geometry.PointCloud = None):
        super().__init__()
        
        self.point_cloud: o3d.geometry.PointCloud = point_cloud
        self.primtive = Primitves.POINTS
        
        if self.point_cloud.has_points():
            self.vertices: GeometryData = GeometryData(3, np.asarray(self.point_cloud.points, dtype=np.float32).flatten(), PrimitiveType.FLOAT)
            self.all_vertices.append(self.vertices)
        
        if self.point_cloud.has_normals():
            self.normales: GeometryData = GeometryData(3, np.asarray(self.point_cloud.normals, dtype=np.float32).flatten(), PrimitiveType.FLOAT)
            self.all_vertices.append(self.normales)
        
        if self.point_cloud.has_colors():
            self.colors: GeometryData = GeometryData(3, np.asarray(self.point_cloud.colors, dtype=np.float32).flatten(), PrimitiveType.FLOAT)
            self.all_vertices.append(self.colors)
        
    def getPointCloud(self) -> o3d.geometry.PointCloud:
        return self.point_cloud

class GeometryO3DTriangleMesh(Geometry):
    def __init__(self, triangle_mesh: o3d.geometry.TriangleMesh = None):
        super().__init__()
        
        self.triangle_mesh = triangle_mesh
        self.primtive = Primitves.TRIANGLES
        
        #self.triangle_mesh.has_adjacency_list()
        #self.triangle_mesh.has_textures()
        #self.triangle_mesh.has_triangle_material_ids()
        
        if self.triangle_mesh.has_vertices():
            self.vertices: GeometryData = GeometryData(3, np.asarray(self.triangle_mesh.vertices, dtype=np.float32).flatten(), PrimitiveType.FLOAT)
            self.all_vertices.append(self.vertices)
        
        
        if self.triangle_mesh.has_vertex_normals():
            self.vertex_normales: GeometryData = GeometryData(3, np.asarray(self.triangle_mesh.vertex_normals, dtype=np.float32).flatten(), PrimitiveType.FLOAT)
            self.all_vertices.append(self.vertex_normales)
        
        if self.triangle_mesh.has_triangle_normals():
            self.triangle_normales: GeometryData = GeometryData(3, np.asarray(self.triangle_mesh.triangle_normals, dtype=np.float32).flatten(), PrimitiveType.FLOAT)
            self.all_vertices.append(self.triangle_normales)
        
        
        if self.triangle_mesh.has_vertex_colors():
            self.colors: GeometryData = GeometryData(3, np.asarray(self.triangle_mesh.vertex_colors, dtype=np.float32).flatten(), PrimitiveType.FLOAT)
            self.all_vertices.append(self.colors)
        
        if self.triangle_mesh.has_triangle_uvs():
            self.uvs: GeometryData = GeometryData(3, np.asarray(self.triangle_mesh.triangle_uvs, dtype=np.float32).flatten(), PrimitiveType.FLOAT)
            self.all_vertices.append(self.uvs)
        
        
        if self.triangle_mesh.has_triangles():
            self.indices: GeometryData = GeometryData(1, np.asarray(self.triangle_mesh.triangles, dtype=np.uint32).flatten(), PrimitiveType.INT)

class GeometryO3DLineSet(Geometry):
    def __init__(self, line_set: o3d.geometry.LineSet = None):
        super().__init__()
        
        self.line_set = line_set
        self.primtive = Primitves.LINES
        
        if self.line_set.has_points():
            self.vertices: GeometryData = GeometryData(3, np.asarray(self.line_set.points, np.float32).flatten(), PrimitiveType.FLOAT)
            self.all_vertices.append(self.vertices)
        
        if self.line_set.has_colors():
            self.colors: GeometryData = GeometryData(3, np.asarray(self.line_set.colors, np.float32).flatten(), PrimitiveType.FLOAT)
            self.all_vertices.append(self.colors)
        
        if self.line_set.has_lines():
            self.indices: GeometryData = GeometryData(1, np.asarray(self.line_set.lines, np.uint32).flatten(), PrimitiveType.INT)