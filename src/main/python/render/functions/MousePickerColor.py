from glm import vec4, fvec4

class MousePickInfo():
    def __init__(self, mesh_id = 0, primitive_id = 0, vertex_id = 0):
        self.mesh_id = mesh_id
        self.primitive_id = primitive_id
        self.vertex_id = vertex_id
    
    def __str__(self):
        return f"({self.mesh_id}, {self.primitive_id}, {self.vertex_id})"

class MousePickerColor():
    max_size = 32 # rgba: 8bits + 8bits + 8bits + 8bits = 32 bits
    
    mesh_id_size = 0 # Set per uniform
    primitive_id_size = 0 # int gl_PrimitiveID
    vertex_id_size = max_size - primitive_id_size - mesh_id_size # int gl_VertexID
    
    @staticmethod
    def createID(mesh: int, primitive: int, vertex: int) -> vec4:
        if MousePickerColor.mesh_id_size + MousePickerColor.primitive_id_size + MousePickerColor.vertex_id_size > MousePickerColor.max_size:
            raise AttributeError(f"id sizes > {MousePickerColor.max_size}")
        
        value: int = 0
        
        mesh = mesh & MousePickerColor.getOneBits(MousePickerColor.mesh_id_size)
        value = value + mesh
        
        if MousePickerColor.primitive_id_size > 0 or MousePickerColor.vertex_id_size > 0:
            value = value << MousePickerColor.mesh_id_size
        
        
        primitive = primitive & MousePickerColor.getOneBits(MousePickerColor.primitive_id_size)
        value = value + primitive
        
        if MousePickerColor.vertex_id_size > 0:
            value = value << MousePickerColor.primitive_id_size
        
        
        vertex = vertex & MousePickerColor.getOneBits(MousePickerColor.vertex_id_size)
        value = value + vertex
        
        a: float = (value & 0xFF) / 255;
        b: float = ((value >> 8) & 0xFF) / 255;
        g: float = ((value >> 16) & 0xFF) / 255;
        r: float = ((value >> 24) & 0xFF) / 255;
        
        return fvec4(r, g, b, a)
    
    @staticmethod
    def colorToID(color: vec4):
        if MousePickerColor.mesh_id_size + MousePickerColor.primitive_id_size + MousePickerColor.vertex_id_size > MousePickerColor.max_size:
            raise AttributeError(f"id sizes > {MousePickerColor.max_size}")
        
        r: int = int(color.x * 255)
        g: int = int(color.y * 255)
        b: int = int(color.z * 255)
        a: int = int(color.w * 255)
        
        value: int = r << 8
        value = (value + g) << 8
        value = (value + b) << 8
        value = value + a
        
        bit_move = MousePickerColor.max_size - MousePickerColor.mesh_id_size
        mesh_id = (value >> bit_move) & MousePickerColor.getOneBits(MousePickerColor.mesh_id_size)
        
        bit_move -= MousePickerColor.primitive_id_size
        primitive_id = (value >> bit_move) & MousePickerColor.getOneBits(MousePickerColor.primitive_id_size)
        
        bit_move -= MousePickerColor.vertex_id_size
        vertex_id = (value >> bit_move) & MousePickerColor.getOneBits(MousePickerColor.vertex_id_size)
        
        return MousePickInfo(mesh_id, primitive_id, vertex_id)
    
    @staticmethod
    def getOneBits(size: int):
        value: int = 0
        
        for _ in range(size):
            value = value << 1
            value += 1
        
        return value