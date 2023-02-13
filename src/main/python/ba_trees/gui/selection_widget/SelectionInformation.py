import glm
import uuid

from pathlib import Path

from PIL import Image as Img
from PyQt6.QtGui import QImage
from colmap_wrapper.colmap.camera import ImageInformation


class Point:
    def __init__(self, position: glm.vec3):
        self.selectionInformation = None
        self.id = uuid.uuid4() # TODO: Should be unique
        self.position: glm.vec3 = position
        self.points: dict = {} # Image: [uv1, uv2]
    
    def add2DPoint(self, image, uv):
        self.points[image] = uv
        image.points.append(self)

class Image:
    def __init__(self, selectionInformation, imageinfo: ImageInformation, pyimage, path: Path):
        self.selectionInformation = selectionInformation
        self.imageinfo: ImageInformation = imageinfo
        self.pyimage = pyimage
        
        self.path: Path = path
        self.width = 0
        self.height = 0
        self.image: QImage = None
        self.preview: QImage = None
        
        self.points: list = [] # Point
        
        
        # Matrix & Depth Map
        self.depth_map = self.imageinfo.depth_image_geometric
        #extrinsics = self.imageinfo.extrinsics
        intrinsics = self.imageinfo.intrinsics.K
        
        self.mat_extrinsics = glm.mat4x4(1.0)
        row = 0
        for array_row in self.selectionInformation.sub_project.pycolmap.images[self.imageinfo.id].projection_matrix(): # TODO to self.imageinfo.extrinsics (Currently broken)
            column = 0
            for value in array_row:
                self.mat_extrinsics[column][row] = value
                column += 1
            row += 1
        
        self.mat_intrinsics = glm.mat3x3(1.0)
        row = 0
        for array_row in intrinsics:
            column = 0
            for value in array_row:
                self.mat_intrinsics[column][row] = value
                column += 1
            row += 1
        
        
        self.mat_extrinsics_inverse = glm.inverse(self.mat_extrinsics)
        self.mat_intrinsics_inverse = glm.mat3x4(glm.inverse(self.mat_intrinsics))
        self.mat_intrinsics = glm.mat4x3(self.mat_intrinsics)
    
    def getImage(self):
        if self.image == None:
            self.image = QImage(str(self.path))
        return self.image
    
    def getPreviewImage(self):
        if self.preview == None:
            with Img.open(self.path) as img:
                width, height = img.size
                
                self.width = width
                self.height = height
                
                img.thumbnail([1920, 1080])
                img2 = img.convert("RGBA")
                data = img2.tobytes("raw", "BGRA")
                self.preview = QImage(data, img2.width, img2.height, QImage.Format.Format_ARGB32)
        
        return self.preview
    
    def getWidth(self):
        if self.width <= 0:
            self.getPreviewImage()
        return self.width
    
    def getHeight(self):
        if self.width <= 0:
            self.getPreviewImage()
        return self.height
    
    def get2DPoints(self):
        ps = [p.points[self] for p in self.points]
        #ps = [item for sublist in ps for item in sublist] # https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists
        return ps
    
    def getSelected2DPoints(self):
        ps = [p.points[self] for p in self.points if p.id in self.selectionInformation.selected_points]
        return ps
    
    def toUV(self, xyz: glm.vec3) -> list:
        image_plane = self.mat_intrinsics @ self.mat_extrinsics @ glm.vec4(xyz, 1.0)
        depth = image_plane.z
        image_uv = glm.vec2(image_plane.xy) / depth
        
        image_uv = glm.vec2(round(image_uv.x), round(image_uv.y))
        
        return image_uv, depth
    
    def toXYZ(self, uv: glm.vec2, depth) -> glm.vec3:
        if depth <= 0:
            return glm.vec3(float('nan'))
        
        return glm.vec3(depth * self.mat_extrinsics_inverse @ glm.mat4x4(self.mat_intrinsics_inverse) @ glm.vec4(uv.xy, 1.0, 1.0/depth))
    
    def toXYZFromDepthMap(self, uv: glm.vec2) -> glm.vec3:
        return self.toXYZ(uv, self.getDepth(uv))
    
    def getDepth(self, uv: glm.vec2) -> float:
        if uv.x < 0 or uv.y < 0 or uv.x >= self.getWidth() or uv.y >= self.getHeight():
            return 0
        
        return self.depth_map[round(uv.y)][round(uv.x)]

class SelectionInformation:
    def __init__(self, sub_project):
        self.sub_project = sub_project
        self.points: dict = {} # Point
        self.images: list = [] # Image
        
        self.selected_points: dict = {}
        
        reconstruction = sub_project.reconstruction
        
        for image_idx in reconstruction.images.keys():
            imageinfo: ImageInformation = reconstruction.images[image_idx]
            pyimage = sub_project.pycolmap.images[image_idx]
            
            # octree = o3d.geometry.Octree(max_depth=8)
            # tree = octree.convert_from_point_cloud(sub_project.reconstruction.get_dense())
            # o3d.visualization.draw_geometries([octree])
            # print(tree)
            
            image_info = Image(self, imageinfo, pyimage, imageinfo.path)
            image_info.getPreviewImage()
            
            self.images.append(image_info)
        
    def selectPoint(self, *points):
        self.selected_points.clear()
        
        for point in points:
            if not (point.id in self.points):
                return
            
            self.selected_points[point.id] = point
    
    def addPoint(self, point: Point, evaluate = True):
        if point.id in self.points:
            return
        
        point.selectionInformation = self
        
        if evaluate:
            position = point.position
            
            for image in self.images:
                uv, _ = image.toUV(position)
                position_in_image = image.toXYZFromDepthMap(uv)
                
                if glm.distance(position, position_in_image) > 0.01:
                    continue
                
                point.add2DPoint(image, [uv.x, uv.y])
                
        else:
            for image, _ in point.points.items():
                image.points.append(point)
        
        self.points[point.id] = point
    
    def removePoint(self, point: Point):
        del self.points[point.id]
        
        for image in point.points.keys():
            image.points.remove(point)