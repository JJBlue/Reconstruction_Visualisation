from PIL import Image

import numpy as np
from render.data import TextureData, TextureFormat, TextureType, TextureInternalFormat, ImageFormat


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
        image_type: ImageFormat = None
        mode_type: TextureFormat = None
        img_type: TextureType = None
        img_internal_format: TextureInternalFormat = None
        dtype: np.dtype = None
        
        if mode == "1":
            image_type = ImageFormat.BLACK_WHITE_BIT
            dtype = np.bit
            raise NotImplementedError()
        elif mode == "L":
            image_type = ImageFormat.BLACK_WHITE
            dtype = np.int8
            img_type = TextureType.UNSIGNED_BYTE
            raise NotImplementedError()
        elif mode == "P":
            image_type = ImageFormat.MAPPED_COLOR_PALETTE
            dtype = np.int8
            img_type = TextureType.UNSIGNED_BYTE
            raise NotImplementedError()
        elif mode == "LA":
            image_type = ImageFormat.BLACK_WHITE_ALPHA
            dtype = np.int8
            img_type = TextureType.UNSIGNED_BYTE
            raise NotImplementedError()
        elif mode == "PA":
            image_type = ImageFormat.MAPPED_COLOR_PALETTE_ALPHA
            dtype = np.int8
            img_type = TextureType.UNSIGNED_BYTE
            raise NotImplementedError()
        elif mode == "RGB":
            image_type = ImageFormat.RGB
            mode_type = TextureFormat.RGB
            dtype = np.int8
            img_type = TextureType.UNSIGNED_BYTE
            img_internal_format = TextureInternalFormat.RGB8
        elif mode == "RGBA":
            image_type = ImageFormat.RGBA
            mode_type = TextureFormat.RGBA
            dtype = np.int8
            img_type = TextureType.UNSIGNED_BYTE
            img_internal_format = TextureInternalFormat.RGBA8
        elif mode == "CMYK":
            image_type = ImageFormat.CMYK
            dtype = np.int8
            img_type = TextureType.UNSIGNED_BYTE
            raise NotImplementedError()
        elif mode == "YCbCr":
            image_type = ImageFormat.YCbCr
            dtype = np.int8
            img_type = TextureType.UNSIGNED_BYTE
            raise NotImplementedError()
        elif mode == "LAB":
            image_type = ImageFormat.LAB
            dtype = np.int8
            img_type = TextureType.UNSIGNED_BYTE
            raise NotImplementedError()
        elif mode == "HSV":
            image_type = ImageFormat.HSV
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