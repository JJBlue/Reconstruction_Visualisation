from render.opengl import OpenGLBuffer
from render import Model

class OpenGLModel(Model):
    def __init__(self):
        super().__init__(OpenGLBuffer())