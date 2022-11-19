from .Workspace import *

try:
    from .colmap import *
except ImportError:
    print("Colmap Workspace couldn't be loaded")