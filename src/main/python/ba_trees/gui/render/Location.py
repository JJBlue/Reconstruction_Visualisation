import glm

class Position:
    def __init__(self, x = 0, y = 0, z = 0):
        self.position = glm.fvec3(x, y, z)
    
    def getX(self) -> float:
        return self.position.x
    
    def setX(self, x: float):
        self.position.x = x
    
    def getY(self) -> float:
        return self.position.y
    
    def setY(self, y: float):
        self.position.y = y
    
    def getZ(self) -> float:
        return self.position.z
    
    def setZ(self, z: float):
        self.position.z = z
    
    def getPosition(self) -> glm.vec3:
        return self.position

class Location(Position):
    def __init__(self, x = 0, y = 0, z = 0, pitch = 0, yaw = 0, roll = 0):
        super().__init__(x, y, z)
        
        self.pitch: float = pitch
        self.yaw: float = yaw
        self.roll: float = roll
    
    def getPitch(self) -> float:
        return self.pitch
    
    def setPitch(self, pitch: float):
        self.pitch = pitch
    
    def getYaw(self) -> float:
        return self.yaw
    
    def setYaw(self, yaw: float):
        self.yaw = yaw
    
    def getRoll(self) -> float:
        return self.roll
    
    def setRoll(self, roll: float):
        self.roll = roll