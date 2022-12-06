from OpenGL.GL import *

from render.data import TextureData
from render.data.TextureData import TextureFormat, TextureType, \
    TextureInternalFormat
from render.render import Texture
from typing import overload


class OpenGLTexture(Texture):
    def __init__(self, data: TextureData):
        super().__init__(data)
        self.id: GL_INT = None
        
        self.img_format = None
        self.img_internal_format = None
        self.img_type = None
        
        self.upload()
    
    def __del__(self):
        try:
            self.delete()
        except:
            pass
    
    def delete(self):
        if glIsTexture(self.id):
            glDeleteTextures(1, id)
    
    def bind(self, image_id):
        glActiveTexture(GL_TEXTURE0 + image_id)
        glBindTexture(GL_TEXTURE_2D, self.id)
    
    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, 0)
    
    def upload(self):
        self.id = glGenTextures(1)
        
        if self.image.getUnpackAlignment():
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        
        glBindTexture(GL_TEXTURE_2D, self.id)
        
        if self.image.getRepeatImage():
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        
        if self.image.getPoorFiltering():
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
        else:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR if self.image.getUseMipmap() else GL_LINEAR)
        
        img_format = OpenGLTexture.toOpenGLFormat(self.image.getFormat())
        img_internal_format = OpenGLTexture.toOpenGLInternalFormat(self.image.getInternalFormat())
        img_type = OpenGLTexture.toOpenGLType(self.image.getType())
        
        glTexImage2D(GL_TEXTURE_2D, 0, img_internal_format, self.image.getWidth(), self.image.getHeight(), 0, img_format, img_type, self.image.getData())
        
        if self.image.getUseMipmap():
            glGenerateMipmap(GL_TEXTURE_2D)
        
        glBindTexture(GL_TEXTURE_2D, 0)
    
    @overload
    def resize(self):
        self.resize(self.image.getWidth(), self.image.getHeight())
    
    @overload
    def resize(self, width, height):
        glBindTexture(GL_TEXTURE_2D, id)
        
        img_format = OpenGLTexture.toOpenGLFormat(self.image.getFormat())
        img_internal_format = OpenGLTexture.toOpenGLInternalFormat(self.image.getInternalFormat())
        img_type = OpenGLTexture.toOpenGLType(self.image.getType())
        
        glTexImage2D(GL_TEXTURE_2D, 0, img_internal_format, width, height, 0, img_format, img_type, None)
        
        glBindTexture(GL_TEXTURE_2D, 0)
        
    
    def getID(self):
        return self.id
    
    @staticmethod
    def toOpenGLFormat(img_format: TextureFormat):
        # Missing Formats: GL_RED, GL_RG, GL_BGR, GL_BGRA, GL_RED_INTEGER, GL_RG_INTEGER, GL_RGB_INTEGER, GL_BGR_INTEGER, GL_RGBA_INTEGER, GL_BGRA_INTEGER, GL_STENCIL_INDEX, GL_DEPTH_COMPONENT, GL_DEPTH_STENCIL.
        if img_format == TextureFormat.RGB:
            return GL_RGB
        elif img_format == TextureFormat.RGBA:
            return GL_RGBA
        raise NotImplementedError()
    
    @staticmethod
    def toOpenGLInternalFormat(img_type: TextureInternalFormat):
        if img_type == TextureInternalFormat.DEPTH_COMPONENT:
            return GL_DEPTH_COMPONENT
        if img_type == TextureInternalFormat.DEPTH_STENCIL:
            return GL_DEPTH_STENCIL
        if img_type == TextureInternalFormat.RED:
            return GL_RED
        if img_type == TextureInternalFormat.RG:
            return GL_RG
        if img_type == TextureInternalFormat.RGB:
            return GL_RGB
        if img_type == TextureInternalFormat.RGBA:
            return GL_RGBA
        if img_type == TextureInternalFormat.R8:
            return GL_R8
        if img_type == TextureInternalFormat.R8_SNORM:
            return GL_R8_SNORM
        if img_type == TextureInternalFormat.R16:
            return GL_R16
        if img_type == TextureInternalFormat.R16_SNORM:
            return GL_R16_SNORM
        if img_type == TextureInternalFormat.R16_SNORM:
            return GL_RG8
        if img_type == TextureInternalFormat.RG8_SNORM:
            return GL_RG8_SNORM
        if img_type == TextureInternalFormat.RG16:
            return GL_RG16
        if img_type == TextureInternalFormat.RG16_SNORM:
            return GL_RG16_SNORM
        if img_type == TextureInternalFormat.R3_G3_B2:
            return GL_R3_G3_B2
        if img_type == TextureInternalFormat.RGB4:
            return GL_RGB4
        if img_type == TextureInternalFormat.RGB5:
            return GL_RGB5
        if img_type == TextureInternalFormat.RGB8:
            return GL_RGB8
        if img_type == TextureInternalFormat.RGB8_SNORM:
            return GL_RGB8_SNORM
        if img_type == TextureInternalFormat.RGB10:
            return GL_RGB10
        if img_type == TextureInternalFormat.RGB12:
            return GL_RGB12
        if img_type == TextureInternalFormat.RGB16_SNORM:
            return GL_RGB16_SNORM
        if img_type == TextureInternalFormat.RGBA2:
            return GL_RGBA2
        if img_type == TextureInternalFormat.RGBA4:
            return GL_RGBA4
        if img_type == TextureInternalFormat.RGB5_A1:
            return GL_RGB5_A1
        if img_type == TextureInternalFormat.RGBA8:
            return GL_RGBA8
        if img_type == TextureInternalFormat.RGBA8_SNORM:
            return GL_RGBA8_SNORM
        if img_type == TextureInternalFormat.RGB10_A2:
            return GL_RGB10_A2
        if img_type == TextureInternalFormat.RGB10_A2UI:
            return GL_RGB10_A2UI
        if img_type == TextureInternalFormat.RGBA12:
            return GL_RGBA12
        if img_type == TextureInternalFormat.RGBA16:
            return GL_RGBA16
        if img_type == TextureInternalFormat.SRGB8:
            return GL_SRGB8
        if img_type == TextureInternalFormat.SRGB8_ALPHA8:
            return GL_SRGB8_ALPHA8
        if img_type == TextureInternalFormat.R16F:
            return GL_R16F
        if img_type == TextureInternalFormat.RG16F:
            return GL_RG16F
        if img_type == TextureInternalFormat.RGB16F:
            return GL_RGB16F
        if img_type == TextureInternalFormat.RGBA16F:
            return GL_RGBA16F
        if img_type == TextureInternalFormat.R32F:
            return GL_R32F
        if img_type == TextureInternalFormat.RG32F:
            return GL_RG32F
        if img_type == TextureInternalFormat.RGB32F:
            return GL_RGB32F
        if img_type == TextureInternalFormat.RGBA32F:
            return GL_RGBA32F
        if img_type == TextureInternalFormat.R11F_G11F_B10F:
            return GL_R11F_G11F_B10F
        if img_type == TextureInternalFormat.RGB9_E5:
            return GL_RGB9_E5
        if img_type == TextureInternalFormat.R8I:
            return GL_R8I
        if img_type == TextureInternalFormat.R8UI:
            return GL_R8UI
        if img_type == TextureInternalFormat.R16I:
            return GL_R16I
        if img_type == TextureInternalFormat.R16UI:
            return GL_R16UI
        if img_type == TextureInternalFormat.R32I:
            return GL_R32I
        if img_type == TextureInternalFormat.R32UI:
            return GL_R32UI
        if img_type == TextureInternalFormat.RG8I:
            return GL_RG8I
        if img_type == TextureInternalFormat.RG8UI:
            return GL_RG8UI
        if img_type == TextureInternalFormat.RG16I:
            return GL_RG16I
        if img_type == TextureInternalFormat.RG16UI:
            return GL_RG16UI
        if img_type == TextureInternalFormat.RG32I:
            return GL_RG32I
        if img_type == TextureInternalFormat.RG32UI:
            return GL_RG32UI
        if img_type == TextureInternalFormat.RGB8I:
            return GL_RGB8I
        if img_type == TextureInternalFormat.RGB8UI:
            return GL_RGB8UI
        if img_type == TextureInternalFormat.RGB16UI:
            return GL_RGB16I
        if img_type == TextureInternalFormat.RGB16UI:
            return GL_RGB16UI
        if img_type == TextureInternalFormat.RGB32I:
            return GL_RGB32I
        if img_type == TextureInternalFormat.RGB32UI:
            return GL_RGB32UI
        if img_type == TextureInternalFormat.RGBA8I:
            return GL_RGBA8I
        if img_type == TextureInternalFormat.RGBA8UI:
            return GL_RGBA8UI
        if img_type == TextureInternalFormat.RGBA16I:
            return GL_RGBA16I
        if img_type == TextureInternalFormat.RGBA16UI:
            return GL_RGBA16UI
        if img_type == TextureInternalFormat.RGBA32I:
            return GL_RGBA32I
        if img_type == TextureInternalFormat.RGBA32UI:
            return GL_RGBA32UI
        if img_type == TextureInternalFormat.COMPRESSED_RED:
            return GL_COMPRESSED_RED
        if img_type == TextureInternalFormat.COMPRESSED_RG:
            return GL_COMPRESSED_RG
        if img_type == TextureInternalFormat.COMPRESSED_RGB:
            return GL_COMPRESSED_RGB
        if img_type == TextureInternalFormat.COMPRESSED_RGBA:
            return GL_COMPRESSED_RGBA
        if img_type == TextureInternalFormat.COMPRESSED_SRGB:
            return GL_COMPRESSED_SRGB
        if img_type == TextureInternalFormat.COMPRESSED_SRGB_ALPHA:
            return GL_COMPRESSED_SRGB_ALPHA
        if img_type == TextureInternalFormat.COMPRESSED_RED_RGTC1:
            return GL_COMPRESSED_RED_RGTC1
        if img_type == TextureInternalFormat.COMPRESSED_SIGNED_RED_RGTC1:
            return GL_COMPRESSED_SIGNED_RED_RGTC1
        if img_type == TextureInternalFormat.COMPRESSED_RG_RGTC2:
            return GL_COMPRESSED_RG_RGTC2
        if img_type == TextureInternalFormat.COMPRESSED_SIGNED_RG_RGTC2:
            return GL_COMPRESSED_SIGNED_RG_RGTC2
        if img_type == TextureInternalFormat.COMPRESSED_RGBA_BPTC_UNORM:
            return GL_COMPRESSED_RGBA_BPTC_UNORM
        if img_type == TextureInternalFormat.COMPRESSED_SRGB_ALPHA_BPTC_UNORM:
            return GL_COMPRESSED_SRGB_ALPHA_BPTC_UNORM
        if img_type == TextureInternalFormat.COMPRESSED_RGB_BPTC_SIGNED_FLOAT:
            return GL_COMPRESSED_RGB_BPTC_SIGNED_FLOAT
        if img_type == TextureInternalFormat.COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT:
            return GL_COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT
    
    @staticmethod
    def toOpenGLType(img_type: TextureType):
        if img_type == TextureType.UNSIGNED_BYTE:
            return GL_UNSIGNED_BYTE
        if img_type == TextureType.BYTE:
            return GL_BYTE
        if img_type == TextureType.UNSIGNED_SHORT:
            return GL_UNSIGNED_SHORT
        if img_type == TextureType.SHORT:
            return GL_SHORT
        if img_type == TextureType.UNSIGNED_INT:
            return GL_UNSIGNED_INT
        if img_type == TextureType.INT:
            return GL_INT
        if img_type == TextureType.HALF_FLOAT:
            return GL_HALF_FLOAT
        if img_type == TextureType.FLOAT:
            return GL_FLOAT
        if img_type == TextureType.UNSIGNED_BYTE_3_3_2:
            return GL_UNSIGNED_BYTE_3_3_2
        if img_type == TextureType.UNSIGNED_BYTE_2_3_3_REV:
            return GL_UNSIGNED_BYTE_2_3_3_REV
        if img_type == TextureType.UNSIGNED_SHORT_5_6_5:
            return GL_UNSIGNED_SHORT_5_6_5
        if img_type == TextureType.UNSIGNED_SHORT_5_6_5_REV:
            return GL_UNSIGNED_SHORT_5_6_5_REV
        if img_type == TextureType.UNSIGNED_SHORT_4_4_4_4:
            return GL_UNSIGNED_SHORT_4_4_4_4
        if img_type == TextureType.UNSIGNED_SHORT_4_4_4_4_REV:
            return GL_UNSIGNED_SHORT_4_4_4_4_REV
        if img_type == TextureType.UNSIGNED_SHORT_5_5_5_1:
            return GL_UNSIGNED_SHORT_5_5_5_1
        if img_type == TextureType.UNSIGNED_SHORT_1_5_5_5_REV:
            return GL_UNSIGNED_SHORT_1_5_5_5_REV
        if img_type == TextureType.UNSIGNED_SHORT_1_5_5_5_REV:
            return GL_UNSIGNED_INT_8_8_8_8
        if img_type == TextureType.UNSIGNED_INT_8_8_8_8_REV:
            return GL_UNSIGNED_INT_8_8_8_8_REV
        if img_type == TextureType.UNSIGNED_INT_10_10_10_2:
            return GL_UNSIGNED_INT_10_10_10_2
        if img_type == TextureType.UNSIGNED_INT_2_10_10_10_REV:
            return GL_UNSIGNED_INT_2_10_10_10_REV
        raise NotImplementedError()
    