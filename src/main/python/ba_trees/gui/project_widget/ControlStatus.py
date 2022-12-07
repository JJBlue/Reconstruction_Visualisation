from Demos.security.security_enums import Enum

class ControlStatus(Enum):
    CAMERA_MOVE = 0
    
    MODEL_MOVE = 10
    MODEL_MOVE_X = 11
    MODEL_MOVE_Y = 12
    MODEL_MOVE_Z = 13
    
    MODEL_ROTATE = 20
    MODEL_ROTATE_X = 21
    MODEL_ROTATE_Y = 22
    MODEL_ROTATE_Z = 23
    
    MODEL_SCALE = 30
    MODEL_SCALE_X = 31
    MODEL_SCALE_Y = 32
    MODEL_SCALE_Z = 33