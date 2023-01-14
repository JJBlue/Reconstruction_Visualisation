from .PrimitiveTypes import *
from .Location import *
from .Geometry import *
from .TextureData import *
from .RenderBufferData import *

from .GeometryStructures import *

try:
    from .GeometryO3D import *
except:
    print("Can't load GeometryO3D")

try:
    from .TextureDataFile import *
except:
    print("Can't load TextureDataFile")