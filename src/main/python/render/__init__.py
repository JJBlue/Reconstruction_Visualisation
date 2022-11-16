from render.render import *

try:
    from render.opengl import *
except ImportError:
    print("OpenGL Render could not be loaded")