from __future__ import annotations

from enum import Enum

class TextureData:
    def __init__(self, internal_format: TextureInternalFormat, img_format: TextureFormat, img_type: TextureType, width: int, height: int, data: object):
        self.internal_format: TextureInternalFormat = internal_format
        self.img_format: TextureFormat = img_format
        self.img_type: TextureType = img_type
        self.width: int = width
        self.height: int = height
        self.data: object = data
        
        self.use_mipmap: bool = True
        self.repeat_image: bool = True
        self.unpack_alignment: bool = True
        self.poor_filtering = False
    
    def setUseMipmap(self, value: bool):
        self.use_mipmap = value
    
    def getUseMipmap(self):
        return self.use_mipmap
    
    def setRepeatImage(self, value: bool):
        self.repeat_image = value
    
    def getRepeatImage(self):
        return self.repeat_image
    
    def setUnpackAlignment(self, value: bool):
        self.unpack_alignment = value
    
    def getUnpackAlignment(self):
        return self.unpack_alignment
    
    def setPoorFiltering(self, value: bool):
        self.poor_filtering = value
    
    def getPoorFiltering(self):
        return self.poor_filtering
    
    def getInternalFormat(self) -> TextureInternalFormat:
        return self.internal_format
    
    def getFormat(self) -> TextureFormat:
        return self.img_format
    
    def getType(self) -> TextureType:
        return self.img_type
    
    def getWidth(self, resize: float = 1.0) -> int:
        return int(self.width * resize)
    
    def getHeight(self, resize: float = 1.0) -> int:
        return int(self.height * resize)
    
    def getData(self, resize: float = 1.0) -> object:
        return self.data

class TextureFormat(Enum):
    RED = 0
    RG = 1
    RGB = 2
    BGR = 3
    RGBA = 4
    BGRA = 5
    RED_INTEGER = 6
    RG_INTEGER = 7
    RGB_INTEGER = 8
    BGR_INTEGER = 9
    RGBA_INTEGER = 10
    BGRA_INTEGER = 11
    STENCIL_INDEX = 12
    DEPTH_COMPONENT = 13
    DEPTH_STENCIL = 14

class TextureInternalFormat(Enum):
    DEPTH_COMPONENT = 0
    DEPTH_STENCIL = 1
    RED = 2
    RG = 3
    RGB = 4
    RGBA = 5
    R8 = 6
    R8_SNORM = 7
    R16 = 8
    R16_SNORM = 9
    RG8 = 10
    RG8_SNORM = 11
    RG16 = 12
    RG16_SNORM = 13
    R3_G3_B2 = 14
    RGB4 = 15
    RGB5 = 16
    RGB8 = 17
    RGB8_SNORM = 18
    RGB10 = 19
    RGB12 = 20
    RGB16_SNORM = 21
    RGBA2 = 22
    RGBA4 = 23
    RGB5_A1 = 24
    RGBA8 = 25
    RGBA8_SNORM = 26
    RGB10_A2 = 27
    RGB10_A2UI = 28
    RGBA12 = 29
    RGBA16 = 30
    SRGB8 = 31
    SRGB8_ALPHA8 = 32
    R16F = 33
    RG16F = 34
    RGB16F = 35
    RGBA16F = 36
    R32F = 37
    RG32F = 38
    RGB32F = 39
    RGBA32F = 40
    R11F_G11F_B10F = 41
    RGB9_E5 = 42
    R8I = 43
    R8UI = 44
    R16I = 45
    R16UI = 46
    R32I = 47
    R32UI = 48
    RG8I = 49
    RG8UI = 50
    RG16I = 51
    RG16UI = 52
    RG32I = 53
    RG32UI = 54
    RGB8I = 55
    RGB8UI = 56
    RGB16I = 57
    RGB16UI = 58
    RGB32I = 59
    RGB32UI = 60
    RGBA8I = 61
    RGBA8UI = 62
    RGBA16I = 63
    RGBA16UI = 64
    RGBA32I = 65
    RGBA32UI = 66
    COMPRESSED_RED = 67
    COMPRESSED_RG = 68
    COMPRESSED_RGB = 69
    COMPRESSED_RGBA = 70
    COMPRESSED_SRGB = 71
    COMPRESSED_SRGB_ALPHA = 72
    COMPRESSED_RED_RGTC1 = 73
    COMPRESSED_SIGNED_RED_RGTC1 = 74
    COMPRESSED_RG_RGTC2 = 75
    COMPRESSED_SIGNED_RG_RGTC2 = 76
    COMPRESSED_RGBA_BPTC_UNORM = 77
    COMPRESSED_SRGB_ALPHA_BPTC_UNORM = 78
    COMPRESSED_RGB_BPTC_SIGNED_FLOAT = 79
    COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT = 80

class TextureType(Enum):
    UNSIGNED_BYTE = 0
    BYTE = 1
    UNSIGNED_SHORT = 2
    SHORT = 3
    UNSIGNED_INT = 4
    INT = 5
    HALF_FLOAT = 6
    FLOAT = 7
    UNSIGNED_BYTE_3_3_2 = 8
    UNSIGNED_BYTE_2_3_3_REV = 9
    UNSIGNED_SHORT_5_6_5 = 10
    UNSIGNED_SHORT_5_6_5_REV = 11
    UNSIGNED_SHORT_4_4_4_4 = 12
    UNSIGNED_SHORT_4_4_4_4_REV = 13
    UNSIGNED_SHORT_5_5_5_1 = 14
    UNSIGNED_SHORT_1_5_5_5_REV = 15
    UNSIGNED_INT_8_8_8_8 = 16
    UNSIGNED_INT_8_8_8_8_REV = 17
    UNSIGNED_INT_10_10_10_2 = 18
    UNSIGNED_INT_2_10_10_10_REV = 19