from OpenGL.GL import *

from render.render import Texture, ImageInformation

class OpenGLTexture(Texture):
    def __init__(self, image: ImageInformation = ImageInformation()):
        super().__init__(image)
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
        # Upload Image
        self.id = glGenTextures(1)
        glBindTexture(self.id)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR if self.mipmap else GL_LINEAR)
        
        glTexImage2D(GL_TEXTURE_2D, 0, self.image.internal_format, self.image.width, self.image.height, 0, self.image.img_format, type, self.image.data)
        
        if self.mipmap:
            glGenerateMipmap(GL_TEXTURE_2D)
        
        glBindTexture(GL_TEXTURE_2D, 0)
    
    def resize(self):
        glBindTexture(GL_TEXTURE_2D, id)
        glTexImage2D(GL_TEXTURE_2D, 0, self.image.internal_format, self.image.width, self.image.height, 0, self.image.img_format, type, None)
        glBindTexture(GL_TEXTURE_2D, 0)