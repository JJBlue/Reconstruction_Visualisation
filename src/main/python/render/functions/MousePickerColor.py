from glm import vec4, u32vec4


class MousePickInfo():
    def __init__(self):
        pass
    
    def __str__(self):
        attrs = [a for a in dir(self) if not callable(getattr(self, a))]
        #funcs = [a for a in dir(obj) if callable(a)]
        
        tmp_list = []
        for attr in attrs:
            if attr.startswith("_"):
                continue
            tmp_list.append(f"{attr}: {getattr(self, attr)}")
        
        return ', '.join(tmp_list)

class MousePickerColor():
    def __init__(self):
        self.bit_per_channel = 32 # 32 = INTEGER
        self.channels = 3 # Only RGB can be used. Alpha used to blend
        
        self.id_bit_sizes = {
                                "mesh_id": 32,       # Set per uniform
                                "primitive_id": 32,  # int gl_PrimitiveID
                                "vertex_id": 32     # int gl_VertexID
                            }
    
    def createID(self, info: MousePickInfo) -> vec4:
        if not self.__check_settings():
            return None
        
        max_value: int = MousePickerColor.getOneBits(self.bit_per_channel)
        value: int = 0
        last_bit_size: int = 0
        
        for name, bit_size in self.id_bit_sizes.items():
            value = value << last_bit_size
            v_value = getattr(info, name)
            value += v_value
            last_bit_size = bit_size
        
        b: float = value & max_value
        g: float = (value >> self.bit_per_channel) & max_value
        r: float = (value >> (2 * self.bit_per_channel)) & max_value
        
        return u32vec4(r, g, b, max_value)
    
    def colorToID_list(self, data: list, offset: int):
        return self.colorToID(data[offset], data[offset + 1], data[offset + 2], data[offset + 3])
    
    def colorToID_vec4(self, color: vec4):
        return self.colorToID(int(color.x), int(color.y), int(color.z), int(color.w))
    
    def colorToID(self, r: int, g: int, b: int, a: int):
        if not self.__check_settings():
            return None
        
        # Alpha < 0. No Data found
        if a < 1.0:
            return None
        
        info: MousePickInfo = MousePickInfo()
        
        value: int = r << self.bit_per_channel
        value = (value + g) << self.bit_per_channel
        value = value + b
        
        for name, bit_size in reversed(self.id_bit_sizes.items()):
            value_id = value & MousePickerColor.getOneBits(bit_size)
            value = value >> bit_size
            setattr(info, name, value_id)
        
        return info
    
    def __check_settings(self) -> bool:
        bits: int = 0
        for b in self.id_bit_sizes.values():
            bits += b
        
        if bits > self.bit_per_channel * self.channels:
            raise AttributeError(f"To many bits in id_bit_sizes")
            return False
        return True
    
    @staticmethod
    def getOneBits(size: int):
        value: int = 0
        
        for _ in range(size):
            value = value << 1
            value += 1
        
        return value