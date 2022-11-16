from __future__ import annotations

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
    
    def move(self, direction: glm.vec3):
        self.position += direction
    
    def getPosition(self) -> glm.vec3:
        return self.position
    
    def setPosition(self,position: glm.vec3):
        self.position = position
    
    def setPositionClass(self, position: Position):
        self.position = position.getPosition()

class Location(Position):
    def __init__(self, x = 0, y = 0, z = 0, pitch = 0, yaw = 0, roll = 0):
        super().__init__(x, y, z)
        self.orientation = glm.fvec3(roll, pitch, yaw)
    
    def getPitch(self) -> float:
        return self.orientation.y
    
    def setPitch(self, pitch: float):
        self.orientation.y = pitch
    
    def getYaw(self) -> float:
        return self.orientation.z
    
    def setYaw(self, yaw: float):
        self.orientation.z = yaw
    
    def getRoll(self) -> float:
        return self.orientation.x
    
    def setRoll(self, roll: float):
        self.orientation.x = roll
    
    def getOrientation(self) -> glm.vec3:
        return self.orientation
    
    def setOrientation(self, orientation: glm.vec3):
        self.orientation = orientation
    
    def setLocation(self, location: Location):
        self.setPositionClass(location)
        self.orientation = location.orientation
        