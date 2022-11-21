from __future__ import annotations

import numpy as np

from PIL import Image

class Textures:
    def __init__(self):
        pass
    
    @staticmethod
    def loadFromFile(file: str) -> ImageInformation:
        img = Image.open(file)
        data = np.array(list(img.getdata()), np.int8)
        # TODO
        pass

class Texture:
    def __init__(self, image: ImageInformation):
        self.mipmap: bool = True
        self.image = image
    
    def bind(self, image_id):
        pass
    
    def unbind(self):
        pass

class ImageInformation:
    def __init__(self, internal_format, img_format, width, height, data):
        self.internal_format = internal_format
        self.img_format = img_format
        self.width = width
        self.height = height
        self.data = data