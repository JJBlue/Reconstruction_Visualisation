import glm

from render.data import Location
from render.data.Location import ModelMatrix


class Camera:
    def __init__(self):
        self.position = ModelMatrix()
        
        # Camera Variables
        self.near: float = 0.01 # Default: 0.01
        self.far: float = 1000
        self.left: float = -100
        self.right: float = 100
        self.bottom: float = -100
        self.top: float = 100
        
        self.fov: float = 90 # in degree: default 70
        
        self.perspective = True
        
        self.view: glm.mat4x4 = None
        self.view_normal: glm.mat4x4 = None
        self.projection: glm.mat4x4 = None
        
        # Camera Vec
        
        self.position = Location(1.0, 2.0, 3.0)
        self.direction: glm.vec3 = glm.fvec3(0.0, -1.0, -1.0)
        self.up: glm.vec3 = glm.fvec3(0.0, 1.0, 0.0)
        
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
    
    # Must be implemented
    def getAspectRatio(self):
        raise NotImplementedError()
    
    def getPosition(self) -> Location:
        return self.position
    
    def getView(self) -> glm.mat4x4:
        return self.view
    
    def getViewNormal(self) -> glm.mat4x4:
        return self.view_normal
    
    def getProjection(self) -> glm.mat4x4:
        return self.projection
    
    # Movement
    def forward(self, amount: float):
        self.position.move(amount * self.direction)
        
    def backward(self, amount: float):
        self.position.move(-amount * self.direction)
    
    def rightward(self, amount: float):
        self.position.move(amount * glm.cross(self.direction, self.up))
    
    def leftward(self, amount: float):
        self.position.move(-amount * glm.cross(self.direction, self.up))
    
    def upward(self, amount: float):
        self.position.move(amount * glm.normalize(glm.cross(glm.cross(self.direction, self.up), self.direction)))
    
    def downward(self, amount: float):
        self.position.move(-amount * glm.normalize(glm.cross(glm.cross(self.direction, self.up), self.direction)))
    
    def pitch(self, degree: float):
        self.direction = glm.normalize(glm.rotate(self.direction, degree * glm.pi() / 180.0, glm.normalize(glm.cross(self.direction, self.up))))
    
    def yaw(self, degree: float):
        self.direction = glm.normalize(glm.rotate(self.direction, degree * glm.pi() / 180.0, self.up))
    
    def roll(self, degree: float):
        self.up = glm.normalize(glm.rotate(self.up, degree * glm.pi() / 180.0, self.direction))