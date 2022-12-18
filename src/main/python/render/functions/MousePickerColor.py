from glm import vec4, u32vec4

class MousePickInfo():
    def __init__(self, mesh_id = 0, primitive_id = 0, vertex_id = 0):
        self.mesh_id = mesh_id
        self.primitive_id = primitive_id
        self.vertex_id = vertex_id
    
    def __str__(self):
        return f"({self.mesh_id}, {self.primitive_id}, {self.vertex_id})"

class MousePickerColor():
    # Only RGB can be used. Alpha used to blend
    bit_per_channel = 32 # 32 = INTEGER
    
    mesh_id_size = 0 # Set per uniform
    primitive_id_size = 0 # int gl_PrimitiveID
    vertex_id_size = (bit_per_channel * 3) - primitive_id_size - mesh_id_size # int gl_VertexID
    
    @staticmethod
    def createID(mesh: int, primitive: int, vertex: int) -> vec4:
        if MousePickerColor.mesh_id_size + MousePickerColor.primitive_id_size + MousePickerColor.vertex_id_size > MousePickerColor.bit_per_channel * 3:
            raise AttributeError(f"id sizes > {MousePickerColor.max_size}")
        
        max_value: int = MousePickerColor.getOneBits(MousePickerColor.bit_per_channel)
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
        
        b: float = value & max_value
        g: float = (value >> MousePickerColor.bit_per_channel) & max_value
        r: float = (value >> (2*MousePickerColor.bit_per_channel)) & max_value
        
        return u32vec4(r, g, b, max_value)
    
    @staticmethod
    def colorToID_list(data: list, offset: int):
        return MousePickerColor.colorToID(data[offset], data[offset + 1], data[offset + 2], data[offset + 3])
    
    @staticmethod
    def colorToID_vec4(color: vec4):
        return MousePickerColor.colorToID(int(color.x), int(color.y), int(color.z), int(color.w))
    
    @staticmethod
    def colorToID(r: int, g: int, b: int, a: int):
        if MousePickerColor.mesh_id_size + MousePickerColor.primitive_id_size + MousePickerColor.vertex_id_size > MousePickerColor.bit_per_channel * 3:
            raise AttributeError(f"id sizes > {MousePickerColor.max_size}")
        
        # Alpha < 0. No Data found
        if a < 1.0:
            return None
        
        bit_move = MousePickerColor.mesh_id_size + MousePickerColor.primitive_id_size + MousePickerColor.vertex_id_size
        
        mesh_id = 0
        primitive_id = 0
        vertex_id = 0
        
        value: int = r << MousePickerColor.bit_per_channel
        value = (value + g) << MousePickerColor.bit_per_channel
        value = value + b
        
        if MousePickerColor.mesh_id_size > 0:
            bit_move -= MousePickerColor.mesh_id_size
            mesh_id = (value >> bit_move) & MousePickerColor.getOneBits(MousePickerColor.mesh_id_size)
        
        if MousePickerColor.primitive_id_size > 0:
            bit_move -= MousePickerColor.primitive_id_size
            primitive_id = (value >> bit_move) & MousePickerColor.getOneBits(MousePickerColor.primitive_id_size)
        
        if MousePickerColor.vertex_id_size > 0:
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