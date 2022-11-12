from OpenGL.GL import *
from render import Camera

class OpenGLCamera(Camera):
    def __init__(self):
        super().__init__()
    
    def getAspectRatio(self):
        viewport = glGetIntegerv(GL_VIEWPORT) # x y width height
        
        width: float = viewport[2]
        height: float = viewport[3]
        
        return width / height