from __future__ import annotations

from enum import StrEnum, Enum

from PIL import Image

import numpy as np

# Missing modes from Pillow
# I (32-bit signed integer pixels)
# F (32-bit floating point pixels)
# La (L with premultiplied alpha)
# RGBX (true color with padding)
# RGBa (true color with premultiplied alpha)
# I;16 (16-bit unsigned integer pixels)
# I;16L (16-bit little endian unsigned integer pixels)
# I;16B (16-bit big endian unsigned integer pixels)
# I;16N (16-bit native endian unsigned integer pixels)
# BGR;15 (15-bit reversed true colour)
# BGR;16 (16-bit reversed true colour)
# BGR;24 (24-bit reversed true colour)
# BGR;32 (32-bit reversed true colour)
class TextureFormat(StrEnum):
    BLACK_WHITE_BIT = "1"
    BLACK_WHITE = "L"
    BLACK_WHITE_ALPHA = "LA"
    MAPPED_COLOR_PALETTE = "P"
    MAPPED_COLOR_PALETTE_ALPHA = "PA"
    RGB = "RGB"
    RGBA = "RGBA"
    CMYK = "CMYK"
    YCbCr = "YCbCr"
    LAB = "LAB"
    HSV = "HSV"

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

class TextureData:
    def __init__(self, internal_format: TextureInternalFormat, img_format: TextureFormat, img_type: TextureType, width: int, height: int, data):
        self.internal_format: TextureInternalFormat = internal_format
        self.img_format: TextureFormat = img_format
        self.img_type: TextureType = img_type
        self.width: int = width
        self.height: int = height
        self.data = data
    
    def getInternalFormat(self) -> TextureInternalFormat:
        return self.internal_format
    
    def getFormat(self) -> TextureFormat:
        return self.img_format
    
    def getType(self) -> TextureType:
        return self.img_type
    
    def getWidth(self) -> int:
        return self.width
    
    def getHeight(self) -> int:
        return self.height
    
    def getData(self):
        return self.data
    
class TextureFile(TextureData):
    def __init__(self, file: str):
        super().__init__(None, None, None, None, None, None)
        self.file = file
        self.file_loaded = False
    
    def load(self):
        if self.file_loaded:
            return
        self.file_loaded = True
        
        img = Image.open(self.file)
        
        width, height = img.size
        
        mode: str = img.mode
        mode_type: TextureFormat = None
        img_type: TextureType = None
        img_internal_format: TextureInternalFormat = None
        dtype: np.dtype = None
        
        if mode == "1":
            mode_type = TextureFormat.BLACK_WHITE_BIT
            dtype = np.bit
            raise NotImplementedError()
        elif mode == "L":
            mode_type = TextureFormat.BLACK_WHITE
            dtype = np.int8
            img_type = TextureType.UNSIGNED_BYTE
            raise NotImplementedError()
        elif mode == "P":
            mode_type = TextureFormat.MAPPED_COLOR_PALETTE
            dtype = np.int8
            img_type = TextureType.UNSIGNED_BYTE
            raise NotImplementedError()
        elif mode == "LA":
            mode_type = TextureFormat.BLACK_WHITE_ALPHA
            dtype = np.int8
            img_type = TextureType.UNSIGNED_BYTE
            raise NotImplementedError()
        elif mode == "PA":
            mode_type = TextureFormat.MAPPED_COLOR_PALETTE_ALPHA
            dtype = np.int8
            img_type = TextureType.UNSIGNED_BYTE
            raise NotImplementedError()
        elif mode == "RGB":
            mode_type = TextureFormat.RGB
            dtype = np.int8
            img_type = TextureType.UNSIGNED_BYTE
            img_internal_format = TextureInternalFormat.RGB8
        elif mode == "RGBA":
            mode_type = TextureFormat.RGBA
            dtype = np.int8
            img_type = TextureType.UNSIGNED_BYTE
            img_internal_format = TextureInternalFormat.RGBA8
        elif mode == "CMYK":
            mode_type = TextureFormat.CMYK
            dtype = np.int8
            img_type = TextureType.UNSIGNED_BYTE
            raise NotImplementedError()
        elif mode == "YCbCr":
            mode_type = TextureFormat.YCbCr
            dtype = np.int8
            img_type = TextureType.UNSIGNED_BYTE
            raise NotImplementedError()
        elif mode == "LAB":
            mode_type = TextureFormat.LAB
            dtype = np.int8
            img_type = TextureType.UNSIGNED_BYTE
            raise NotImplementedError()
        elif mode == "HSV":
            mode_type = TextureFormat.HSV
            dtype = np.int8
            img_type = TextureType.UNSIGNED_BYTE
            raise NotImplementedError()
        else:
            raise NotImplementedError()
        
        self.dtype = dtype
        
        self.internal_format: TextureInternalFormat = img_internal_format
        self.img_format: TextureFormat = mode_type
        self.img_type: TextureType = img_type
        self.width: int = width
        self.height: int = height
    
    def getInternalFormat(self) -> TextureInternalFormat:
        self.load()
        return self.internal_format
    
    def getFormat(self) -> TextureFormat:
        self.load()
        return self.img_format
    
    def getType(self) -> TextureType:
        self.load()
        return self.img_type
    
    def getWidth(self) -> int:
        self.load()
        return self.width
    
    def getHeight(self) -> int:
        self.load()
        return self.height
    
    def getData(self) -> np.ndarray:
        self.load()
        img = Image.open(self.file)
        return np.array(list(img.getdata()), self.dtype)