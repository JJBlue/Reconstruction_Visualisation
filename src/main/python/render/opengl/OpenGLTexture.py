from OpenGL.GL import *

from PIL import Image, ImageFont, ImageDraw

class OpenGLTexture:
    def __init__(self):
        super().__init__()
        self.id: GL_INT = None
    
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
        glBindTexture(GL_TEXTURE_2D)
    
    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, 0)
    
    def upload(self):
        # Load Image from file
        
        
        # Upload Image
        self.id = glGenTextures(1)
        glBindTexture(self.id)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR if self.mipmap else GL_LINEAR)
        
        glTexImage2D(GL_TEXTURE_2D, 0, internal_format, width, height, 0, format, type, data) # TODO
        
        if self.mipmap:
            glGenerateMipmap(GL_TEXTURE_2D)
        
        glBindTexture(GL_TEXTURE_2D, 0)
    
    def resize(self):
        glBindTexture(GL_TEXTURE_2D, id)
        glTexImage2D(GL_TEXTURE_2D, 0, internal_format, width, height, 0, format, type, None) # TODO
        glBindTexture(GL_TEXTURE_2D, 0)