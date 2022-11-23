import numpy as np
from render.render import PrimitiveType, Primitves


class GeometryData:
    def __init__(self, dimension: int, data: np.ndarray, primitive_type: PrimitiveType = PrimitiveType.FLOAT):
        self.dimension: int = dimension
        self.primitive_type: PrimitiveType = primitive_type
        self.data: np.ndarray = data
        self.size: int = int(len(self.data) / self.dimension)
    
    def getDimension(self) -> int:
        return self.dimension
    
    def getData(self) -> np.ndarray:
        return self.data
    
    def getSize(self) -> int:
        return self.size
    
    def getPrimitiveType(self) -> PrimitiveType:
        return self.primitive_type

class Geometry:
    def __init__(self):
        self.vertices: GeometryData = None
        self.normales: GeometryData = None
        self.indices: GeometryData = None
        
        self.all_vertices: list = []
        
        self.primtive = Primitves.TRIANGLES
    
    def getAllVertices(self) -> list:
        return self.all_vertices
    
    def getVertices(self) -> GeometryData:
        return self.vertices
    
    def getNormales(self) -> GeometryData:
        return self.normales
    
    def getIndices(self) -> GeometryData:
        return self.indices
    
    def getPrimitive(self):
        return self.primtive


##########################
### Default Primitives ###
##########################

class Cube(Geometry):
    def __init__(self):
        super().__init__()
        
        self.primtive = Primitves.TRIANGLES
        
        # GLfloat
        self.vertices = GeometryData(
            3,
            np.array([
                -0.5, -0.5,  0.5, #0     #0 (left bottom front)
                -0.5, -0.5,  0.5, #1
                -0.5, -0.5,  0.5, #2
                 0.5, -0.5,  0.5, #3     #1 (right bottom front)
                 0.5, -0.5,  0.5, #4
                 0.5, -0.5,  0.5, #5
                -0.5,  0.5,  0.5, #6     #2 (left top front)
                -0.5,  0.5,  0.5, #7
                -0.5,  0.5,  0.5, #8
                 0.5,  0.5,  0.5, #9     #3 (right top front)
                 0.5,  0.5,  0.5, #10
                 0.5,  0.5,  0.5, #11
                -0.5, -0.5, -0.5, #12    #4 (left bottom back)
                -0.5, -0.5, -0.5, #13
                -0.5, -0.5, -0.5, #14
                 0.5, -0.5, -0.5, #15    #5 (right bottom back)
                 0.5, -0.5, -0.5, #16
                 0.5, -0.5, -0.5, #17
                -0.5,  0.5, -0.5, #18    #6 (left top back)
                -0.5,  0.5, -0.5, #19
                -0.5,  0.5, -0.5, #20
                 0.5,  0.5, -0.5, #21    #7 (right top back)
                 0.5,  0.5, -0.5, #22
                 0.5,  0.5, -0.5  #23
            ], np.float32),
            PrimitiveType.FLOAT
        )
        self.all_vertices.append(self.vertices)
        
        self.normales = GeometryData(
            3,
            np.array([
                -1.0,  0.0,  0.0, #0 (left bottom front)
                 0.0, -1.0,  0.0,
                 0.0,  0.0,  1.0,
                 1.0,  0.0,  0.0, #1 (right bottom front)
                 0.0, -1.0,  0.0,
                 0.0,  0.0,  1.0,
                -1.0,  0.0,  0.0, #2 (left top front)
                 0.0,  1.0,  0.0,
                 0.0,  0.0,  1.0,
                 1.0,  0.0,  0.0, #3 (right top front)
                 0.0,  1.0,  0.0,
                 0.0,  0.0,  1.0,
                -1.0,  0.0,  0.0, #4 (left bottom back)
                 0.0, -1.0,  0.0,
                 0.0,  0.0, -1.0,
                 1.0,  0.0,  0.0, #5 (right bottom back)
                 0.0, -1.0,  0.0,
                 0.0,  0.0, -1.0,
                -1.0,  0.0,  0.0, #6 (left top back)
                 0.0,  1.0,  0.0,
                 0.0,  0.0, -1.0,
                 1.0,  0.0,  0.0, #7 (right top back)
                 0.0,  1.0,  0.0,
                 0.0,  0.0, -1.0
            ], np.float32),
            PrimitiveType.FLOAT
        )
        self.all_vertices.append(self.normales)
        
        # GLuint
        self.indices = GeometryData(
            1,
            np.array([
                #Top
                7,  10, 22,
                22, 19,  7,
                
                #Bottom
                16,  4,  1,
                 1, 13, 16,
        
                #Left
                18, 12,  0,
                 0,  6, 18,
        
                #Right
                21,  9,  3,
                 3, 15, 21,
        
                #Front
                2, 5, 11,
                11, 8, 2,
                
                #Back
                14, 20, 23,
                23, 17, 14
            ], np.uint32),
            PrimitiveType.UNSIGNED_INT
        )

class CubeWithoutNormals(Geometry):
    def __init__(self):
        super().__init__()
        
        self.primtive = Primitves.TRIANGLES
        
        self.vertices = GeometryData(
            3,
            np.array([
                -0.5, -0.5,  0.5, #0
                 0.5, -0.5,  0.5, #1
                -0.5,  0.5,  0.5, #2
                 0.5,  0.5,  0.5, #3
                -0.5, -0.5, -0.5, #4
                 0.5, -0.5, -0.5, #5
                -0.5,  0.5, -0.5, #6
                 0.5,  0.5, -0.5  #7
            ], np.float32)
        )
        self.all_vertices.append(self.vertices)
        
        self.indices = GeometryData(
            1,
            np.array([
                #Top
                2, 6, 7,
                2, 3, 7,
        
                #Bottom
                0, 4, 5,
                0, 1, 5,
        
                #Left
                0, 2, 6,
                0, 4, 6,
        
                #Right
                1, 3, 7,
                1, 5, 7,
        
                #Front
                0, 2, 3,
                0, 1, 3,
        
                #Back
                4, 6, 7,
                4, 5, 7
            ], np.uint32),
            PrimitiveType.UNSIGNED_INT
        )

class CubeDotCloud(Geometry):
    def __init__(self):
        super().__init__()
        
        size_per_unit: int = 100
        size: int = 1
        
        global_size = size * size_per_unit
        
        tmp_vertices: list = []
        tmp_normal: list = []
        tmp_color: list = []
        
        for tx in range(global_size + 1):
            for ty in range(global_size + 1):
                for tz in range(global_size + 1):
                    x: float = (tx / size_per_unit) - (size / 2.0)
                    y: float = (ty / size_per_unit) - (size / 2.0)
                    z: float = (tz / size_per_unit) - (size / 2.0)
                    
                    tmp_vertices.append(x)
                    tmp_vertices.append(y)
                    tmp_vertices.append(z)
                    
                    # x
                    if tx == 0:
                        tmp_normal.append(-1.0)
                    elif tx == global_size:
                        tmp_normal.append(1.0)
                    else:
                        tmp_normal.append(0.0)
                    
                    if ty == 0:
                        tmp_normal.append(-1.0)
                    elif ty == global_size:
                        tmp_normal.append(1.0)
                    else:
                        tmp_normal.append(0.0)
                    
                    if tz == 0:
                        tmp_normal.append(-1.0)
                    elif tz == global_size:
                        tmp_normal.append(1.0)
                    else:
                        tmp_normal.append(0.0)
                    
                    tmp_color.append(float(tx / global_size))
                    tmp_color.append(float(ty / global_size))
                    tmp_color.append(float(tz / global_size))
        
        self.primtive = Primitves.POINTS
        
        self.vertices = GeometryData(3, np.array(tmp_vertices, np.float32), PrimitiveType.FLOAT)
        self.all_vertices.append(self.vertices)
        
        self.normales = GeometryData(3, np.array(tmp_normal, np.float32), PrimitiveType.FLOAT)
        self.all_vertices.append(self.normales)
        
        self.colors = GeometryData(3, np.array(tmp_color, np.float32), PrimitiveType.FLOAT)
        self.all_vertices.append(self.colors)
    
class Pane(Geometry):
    def __init__(self):
        super().__init__()
        
        self.primtive = Primitves.TRIANGLES
        
        self.vertices = GeometryData(
            3,
            np.array([
                0.0, 0.0, 0.0, #0
                0.0, 1.0, 0.0, #1
                1.0, 0.0, 0.0, #2
                1.0, 1.0, 0.0, #3
            ], np.float32)
        )
        self.all_vertices.append(self.vertices)
        
        self.normales = GeometryData(
            3,
            np.array([
                0.0, 0.0, 1.0,
                0.0, 0.0, 1.0,
                0.0, 0.0, 1.0,
                0.0, 0.0, 1.0,
            ], np.float32)
        )
        self.all_vertices.append(self.normales)
        
        self.indices = GeometryData(
            1,
            np.array([
                0, 2, 1,
                1, 2, 3
            ], np.uint32),
            PrimitiveType.UNSIGNED_INT
        )

class CoordinateSystem(Geometry):
    def __init__(self):
        super().__init__()
        
        self.primtive = Primitves.LINES
        
        self.vertices = GeometryData(
            3,
            np.array([
                -100.0,    0.0,    0.0,
                 100.0,    0.0,    0.0,
                 0.0  ,  100.0,    0.0,
                 0.0  , -100.0,    0.0,
                 0.0  ,    0.0,  100.0,
                 0.0  ,    0.0, -100.0,
            ], np.float32)
        )
        self.all_vertices.append(self.vertices)
        
        self.colors = GeometryData(
            3,
            np.array([
                1.0, 0.0, 0.0,
                1.0, 0.0, 0.0,
                0.0, 1.0, 0.0,
                0.0, 1.0, 0.0,
                0.0, 0.0, 1.0,
                0.0, 0.0, 1.0,
            ], np.float32)
        )
        self.all_vertices.append(self.colors)



















        