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
            print("Data")
        
        if self.point_cloud.has_normals():
            self.normales: GeometryData = GeometryData(3, np.asarray(self.point_cloud.normals).astype('float32'), PrimitiveType.FLOAT)
            self.all_vertices.append(self.normales)
            print("Normal")
        
        if self.point_cloud.has_colors():
            self.colors: GeometryData = GeometryData(3, np.asarray(self.point_cloud.colors).astype('float32'), PrimitiveType.FLOAT)
            self.all_vertices.append(self.colors)
            print("Color")
        
    def getPointCloud(self) -> o3d.geometry.PointCloud:
        return self.point_cloud