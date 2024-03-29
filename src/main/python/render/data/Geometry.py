from render.data import PrimitiveType, Primitves


class GeometryData:
    def __init__(self, dimension: int, data, primitive_type: PrimitiveType = PrimitiveType.FLOAT):
        self.dimension: int = dimension
        self.primitive_type: PrimitiveType = primitive_type
        self.data = data
        self.size: int = int(len(self.data) / self.dimension)
    
    def getDimension(self) -> int:
        return self.dimension
    
    def getData(self):
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