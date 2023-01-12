from __future__ import annotations

import glm

from enum import Enum
from typing import overload


class AngleType(Enum):
    RADIANS = 0
    DEGREES = 1
    
    @staticmethod
    def convert(value: float, from_type: AngleType, to_type: AngleType):
        if from_type == to_type:
            return value
        
        if from_type == AngleType.RADIANS:
            if to_type == AngleType.DEGREES:
                return value * 180 / glm.pi()
            else:
                raise NotImplementedError()
        elif from_type == AngleType.DEGREES:
            if to_type == AngleType.RADIANS:
                return value * glm.pi() / 180
            else:
                raise NotImplementedError()
        
        raise NotImplementedError()

class Position:
    def __init__(self, x = 0, y = 0, z = 0):
        self.position: glm.vec3 = glm.fvec3(x, y, z)
        self.model: glm.mat4x4 = glm.fmat4x4(1.0)
        self.updateModel()
    
    def getX(self) -> float:
        return self.position.x
    
    def setX(self, x: float):
        self.position.x = x
        self.updateModel()
    
    def getY(self) -> float:
        return self.position.y
    
    def setY(self, y: float):
        self.position.y = y
        self.updateModel()
    
    def getZ(self) -> float:
        return self.position.z
    
    def setZ(self, z: float):
        self.position.z = z
        self.updateModel()
    
    def move(self, direction: glm.vec3):
        self.position += direction
        self.updateModel()
    
    def getPosition(self) -> glm.vec3:
        return self.position
    
    def setPosition(self,position: glm.vec3):
        self.position = position
        self.updateModel()
    
    def setPositionClass(self, position: Position):
        self.position = position.getPosition()
        self.updateModel()
    
    def getModel(self) -> glm.mat4x4:
        return self.model
    
    def updateModel(self, model = glm.fmat4x4(1.0)):
        model = glm.translate(model, self.position)
        self.model = model

class Location(Position):
    def __init__(self, x = 0, y = 0, z = 0, pitch = 0, yaw = 0, roll = 0):
        self.orientation = glm.fvec3(pitch, yaw, roll)
        super().__init__(x, y, z)
    
    def getPitch(self) -> float:
        return self.orientation.y
    
    def setPitch(self, pitch: float, angle_type = AngleType.RADIANS):
        self.orientation.y = AngleType.convert(pitch, angle_type, AngleType.RADIANS)
        self.updateModel()
    
    def getYaw(self) -> float:
        return self.orientation.z
    
    def setYaw(self, yaw: float, angle_type = AngleType.RADIANS):
        self.orientation.z = AngleType.convert(yaw, angle_type, AngleType.RADIANS)
        self.updateModel()
    
    def getRoll(self) -> float:
        return self.orientation.x
    
    def setRoll(self, roll: float, angle_type = AngleType.RADIANS):
        self.orientation.x = AngleType.convert(roll, angle_type, AngleType.RADIANS)
        self.updateModel()
    
    def getOrientation(self) -> glm.vec3:
        return self.orientation
    
    def setOrientation(self, orientation: glm.vec3):
        self.orientation = orientation
        self.updateModel()
    
    def setLocation(self, location: Location):
        self.setPositionClass(location)
        self.orientation = location.orientation
        self.updateModel()
    
    def updateModel(self, model = glm.fmat4x4(1.0)):
        if self.orientation != None:
            # pitch
            model = glm.rotate(model, self.orientation.x, glm.fvec3(1.0, 0.0, 0.0))
            # yaw
            model = glm.rotate(model, self.orientation.y, glm.fvec3(0.0, 1.0, 0.0))
            # roll
            model = glm.rotate(model, self.orientation.z, glm.fvec3(0.0, 0.0, 1.0))
        
        super().updateModel(model)
        
class ModelMatrix(Location):
    def __init__(self, x = 0, y = 0, z = 0, pitch = 0, yaw = 0, roll = 0):
        self.__scale: glm.vec3 = glm.fvec3(1.0)
        super().__init__(x, y, z, pitch, yaw, roll)
    
    def scaleX(self, x: float):
        self.__scale.x = x
        self.updateModel()
    
    def scaleY(self, y: float):
        self.__scale.y = y
        self.updateModel()
        
    def scaleZ(self, z: float):
        self.__scale.z = z
        self.updateModel()
    
    @overload
    def scale(self, scale: float):
        pass
    
    @overload
    def scale(self, scale: glm.vec3):
        pass
    
    def scale(self, scale):
        if isinstance(scale, glm.vec3):
            self.__scale = scale
        elif isinstance(scale, float):
            self.__scale *= scale
        
        self.updateModel()
    
    def updateModel(self, model = glm.fmat4x4(1.0)):
        if self.scale != None:
            model = glm.scale(model, self.__scale)
        
        super().updateModel(model)




