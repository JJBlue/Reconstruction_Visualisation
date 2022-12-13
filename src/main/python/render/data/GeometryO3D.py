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
            self.vertices: GeometryData = GeometryData(3, np.asarray(self.point_cloud.points).astype('float32'), PrimitiveType.FLOAT)
            self.all_vertices.append(self.vertices)
        
        if self.point_cloud.has_normals():
            self.normales: GeometryData = GeometryData(3, np.asarray(self.point_cloud.normals).astype('float32'), PrimitiveType.FLOAT)
            self.all_vertices.append(self.normales)
        
        if self.point_cloud.has_colors():
            self.colors: GeometryData = GeometryData(3, np.asarray(self.point_cloud.colors).astype('float32'), PrimitiveType.FLOAT)
            self.all_vertices.append(self.colors)
        
    def getPointCloud(self) -> o3d.geometry.PointCloud:
        return self.point_cloud

class GeometryO3DTriangleMesh(Geometry):
    def __init__(self, triangle_mesh: o3d.geometry.TriangleMesh = None):
        super().__init__()
        
        self.triangle_mesh = triangle_mesh
        self.primtive = Primitves.TRIANGLES
        
        if self.triangle_mesh.has_vertices():
            self.vertices: GeometryData = GeometryData(3, np.asarray(self.triangle_mesh.vertices).astype('float32'), PrimitiveType.DOUBLE)
            self.all_vertices.append(self.vertices)
        
        if self.triangle_mesh.has_triangle_normals():
            self.normales: GeometryData = GeometryData(3, np.asarray(self.triangle_mesh.vertex_normals).astype('float32'), PrimitiveType.DOUBLE)
            self.all_vertices.append(self.normales)
        
        if self.triangle_mesh.has_vertex_colors():
            self.colors: GeometryData = GeometryData(3, np.asarray(self.triangle_mesh.vertex_colors).astype('float32'), PrimitiveType.DOUBLE)
            self.all_vertices.append(self.colors)
        
        if self.triangle_mesh.has_triangle_uvs():
            self.uvs: GeometryData = GeometryData(3, np.asarray(self.triangle_mesh.triangle_uvs).astype('float32'), PrimitiveType.DOUBLE)
            self.all_vertices.append(self.uvs)

class GeometryO3DLineSet(Geometry):
    def __init__(self, line_set: o3d.geometry.LineSet = None):
        super().__init__()
        
        self.line_set = line_set
        self.primtive = Primitves.LINES
        
        # TODO: has_points
        
        if self.line_set.has_lines():
            self.vertices: GeometryData = GeometryData(3, np.asarray(self.line_set.lines).astype('float32'), PrimitiveType.DOUBLE)
            self.all_vertices.append(self.vertices)
        
        if self.line_set.has_colors():
            self.colors: GeometryData = GeometryData(3, np.asarray(self.line_set.colors).astype('float32'), PrimitiveType.DOUBLE)
            self.all_vertices.append(self.colors)