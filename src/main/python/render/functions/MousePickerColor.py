from glm import vec2, vec4

class MousePickInfo():
    def __init__(self, mesh_id = 0, primitive_id = 0, vertex_id = 0):
        self.mesh_id = mesh_id
        self.primitive_id = primitive_id
        self.vertex_id = vertex_id

class MousePickerColor():
    max_size = 32 # rgba: 8bits + 8bits + 8bits + 8bits = 32 bits
    
    mesh_id_size = 0 # Set per uniform
    primitive_id_size = 0 # int gl_PrimitiveID
    vertex_id_size = max_size - primitive_id_size - mesh_id_size # int gl_VertexID
    
    @staticmethod
    def createID() -> vec2:
        pass
    
    @staticmethod
    def colorToID(color: vec4):
        if MousePickerColor.mesh_id_size + MousePickerColor.primitive_id_size + MousePickerColor.vertex_id_size > MousePickerColor.max_size:
            raise AttributeError(f"id sizes > {MousePickerColor.max_size}")
        
        value: int = color.x << 8
        value = (value + color.y) << 8
        value = (value + color.z) << 8
        value = value + color.w
        
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