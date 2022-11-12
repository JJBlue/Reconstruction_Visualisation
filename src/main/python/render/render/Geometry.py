import numpy as np

class GeometryData:
    def __init__(self, dimension: int, data: np.ndarray):
        self.dimension: int = dimension
        self.data: np.ndarray = data
        self.size: int = int(len(self.data) / self.dimension)
    
    def getDimension(self) -> int:
        return self.dimension
    
    def getData(self) -> np.ndarray:
        return self.data
    
    def getSize(self) -> int:
        return self.size

class Geometry:
    def __init__(self):
        self.vertices: GeometryData = None
        self.normales: GeometryData = None
        self.indices: GeometryData = None
        
        self.all_vertices: list = []
    
    def getAllVertices(self) -> list:
        return self.all_vertices
    
    def getVertices(self) -> GeometryData:
        return self.vertices
    
    def getNormales(self) -> GeometryData:
        return self.normales
    
    def getIndices(self) -> GeometryData:
        return self.indices

class Cube(Geometry):
    def __init__(self):
        super().__init__()
        
        # GLfloat
        self.vertices = GeometryData(
            3,
            np.array([
                -1, -1,  0.5, #0
                 1, -1,  0.5, #1
                -1,  1,  0.5, #2
                 1,  1,  0.5, #3
                -1, -1, -0.5, #4
                 1, -1, -0.5, #5
                -1,  1, -0.5, #6
                 1,  1, -0.5  #7
            ], dtype='float32')
        )
        self.all_vertices.append(self.vertices)
        
        # GLuint
        self.indices = GeometryData(
            3,
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
            ], dtype='float32')
        )
        