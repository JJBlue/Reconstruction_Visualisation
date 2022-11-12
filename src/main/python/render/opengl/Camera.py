import glm

from OpenGL.GL import *
from render.opengl import Location, Entity


class Camera(Entity):
    def __init__(self):
        super().__init__()
        
        # Camera Variables
        self.near: float = 0.01
        self.far: float = 1000
        self.left: float = -100
        self.right: float = 100
        self.bottom: float = -100
        self.top: float = 100
        
        self.fov: float = 70 # in degree
        
        self.perspective = True
        
        self.view: glm.mat4x4 = None
        self.view_normal: glm.mat4x4 = None
        self.projection: glm.mat4x4 = None
        
        # Camera Vec
        
        self.position = Location(-3, 0, 0)
        self.direction: glm.vec3 = glm.fvec3(1, 0, 0)
        self.up: glm.vec3 = glm.fvec3(0, 1, 0)
        
        # Update
        self.update()
    
    def update(self):
        self.direction = glm.normalize(self.direction)
        self.up = glm.normalize(self.up)
        
        pos: glm.vec3 = self.position.getPosition()
        self.view = glm.lookAt(pos, pos + self.direction, self.up)
        self.view_normal = glm.transpose(glm.inverse(self.view))
        
        if self.perspective:
            self.projection = glm.perspective(self.fov * (glm.pi() / 180), self.getAspectRatio(), self.near, self.far)
        else:
            self.projection = glm.ortho(self.left, self.right, self.bottom, self.top, self.near, self.far)
    
    def getAspectRatio(self):
        viewport = glGetIntegerv(GL_VIEWPORT) # x y width height
        
        width: float = viewport[2]
        height: float = viewport[3]
        
        return width / height
    
    def getPosition(self) -> Location:
        return self.position
    
    def getView(self) -> glm.mat4x4:
        return self.view
    
    def getViewNormal(self) -> glm.mat4x4:
        return self.view_normal
    
    def getProjection(self) -> glm.mat4x4:
        return self.projection