import numpy as np

from pathlib import Path
from PIL import Image

from render.data import TextureData, TextureFormat, TextureType, TextureInternalFormat


class AbstractTexturePILImage(TextureData):
    def __init__(self):
        super().__init__(None, None, None, None, None, None)
        
        self.file_loaded = False
        
        self.use_mipmap: bool = True
        self.repeat_image: bool = True
        self.unpack_alignment: bool = True
        self.poor_filtering = False
        
        self.converted_image = None
        
        self.resize_max_size = None
    
    def load(self):
        pass
    
    def __loadImage(self, img):
        width, height = img.size
        
        mode: str = img.mode
        mode_type: TextureFormat = None
        img_type: TextureType = None
        img_internal_format: TextureInternalFormat = None
        dtype: np.dtype = None
        
        if mode in ["LA", "PA"]:
            img = img.convert("RGBA")
            mode = "RGBA"
            self.converted_image = img
        elif mode in ["1", "L", "P", "CMYK", "YCbCr", "LAB", "HSV"]:
            img = img.convert("RGB")
            mode = "RGB"
            self.converted_image = img
        elif mode in ["RGB", "RGBA", "BGR", "BGRA"]:
            pass
        else:
            raise NotImplementedError()
        
        if mode == "RGB":
            mode_type = TextureFormat.RGB
            dtype = np.uint8
            img_type = TextureType.UNSIGNED_BYTE
            img_internal_format = TextureInternalFormat.RGB8
        elif mode == "RGBA":
            mode_type = TextureFormat.RGBA
            dtype = np.uint8
            img_type = TextureType.UNSIGNED_BYTE
            img_internal_format = TextureInternalFormat.RGBA8
        elif mode == "BGR":
            mode_type = TextureFormat.BGR
            dtype = np.uint8
            img_type = TextureType.UNSIGNED_BYTE
            img_internal_format = TextureInternalFormat.RGB8
        elif mode == "BGRA":
            mode_type = TextureFormat.BGRA
            dtype = np.uint8
            img_type = TextureType.UNSIGNED_BYTE
            img_internal_format = TextureInternalFormat.RGBA8
        
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
    
    def getWidth(self, resize=1.0) -> int:
        self.load()
        return super().getWidth(resize)
    
    def getHeight(self, resize=1.0) -> int:
        self.load()
        return super().getHeight(resize)

    def __getDataImage(self, resize, image) -> np.ndarray:
        self.load()
        
        if self.converted_image:
            image = self.converted_image
        
        if resize != 1.0 and resize != None:
            image = image.resize((self.getWidth(resize), self.getHeight(resize)))
        
        if self.resize_max_size != None:
            image.thumbnail(self.resize_max_size)
            self.width, self.height = image.size
        
        array = np.asarray(image, dtype=self.dtype).flatten()
        return array

class TextureFile(AbstractTexturePILImage):
    def __init__(self, file: Path):
        super().__init__()
        self.file = file

    def load(self):
        if self.file_loaded:
            return
        
        self.file_loaded = True
        
        with Image.open(self.file) as img:
            self._AbstractTexturePILImage__loadImage(img)
    
    def getData(self, resize=1.0) -> np.ndarray:
        with Image.open(self.file) as img:
            return self._AbstractTexturePILImage__getDataImage(resize, img)
        
        return None
        #img = Image.open(self.file)
        #return np.array(list(img.getdata()), self.dtype)

class TexturePILImage(AbstractTexturePILImage):
    def __init__(self, image: Image):
        super().__init__()
        self.image = image
    
    def load(self):
        if self.file_loaded:
            return
        
        self.file_loaded = True
        
        self._AbstractTexturePILImage__loadImage(self.image)
    
    def getData(self, resize=0.3) -> np.ndarray:
        return self._AbstractTexturePILImage__getDataImage(resize, self.image)