from OpenGL.GL import *

from render.render import PrimitiveType, Primitves


class Types:
    @staticmethod
    def PrimitiveTypeToOpenGL(pt: PrimitiveType):
        match pt:
            case PrimitiveType.BYTE:
                return GL_BYTE
            case PrimitiveType.UNSIGNED_BYTE:
                return GL_UNSIGNED_BYTE
            case PrimitiveType.SHORT:
                return GL_SHORT
            case PrimitiveType.UNSIGNED_SHORT:
                return GL_UNSIGNED_SHORT
            case PrimitiveType.INT:
                return GL_INT
            case PrimitiveType.UNSIGNED_INT:
                return GL_UNSIGNED_INT
            case PrimitiveType.FIXED:
                return GL_FIXED
            case PrimitiveType.HALF_FLOAT:
                return GL_HALF_FLOAT
            case PrimitiveType.FLOAT:
                return GL_FLOAT
            case PrimitiveType.DOUBLE:
                return GL_DOUBLE
            case _:
                return None
    
    @staticmethod
    def PrimitivesToOpenGL(pt: Primitves):
        match pt:
            case Primitves.POINTS:
                return GL_POINTS
            case Primitves.LINES:
                return GL_LINES
            case Primitves.LINE_STRIP:
                return GL_LINE_STRIP
            case Primitves.LINE_LOOP:
                return GL_LINE_LOOP
            case Primitves.LINES_ADJACENCY:
                return GL_LINES_ADJACENCY
            case Primitves.LINE_STRIP_ADJACENCY:
                return GL_LINE_STRIP_ADJACENCY
            case Primitves.TRIANGLES:
                return GL_TRIANGLES
            case Primitves.TRIANGLE_STRIP:
                return GL_TRIANGLE_STRIP
            case Primitves.TRIANGLE_FAN:
                return GL_TRIANGLE_FAN
            case Primitves.TRIANGLES_ADJACENCY:
                return GL_TRIANGLES_ADJACENCY
            case Primitves.TRIANGLE_STRIP_ADJACENCY:
                return GL_TRIANGLE_STRIP_ADJACENCY
            case Primitves.QUADS:
                return GL_QUADS
            case Primitves.QUAD_STRIP:
                return GL_QUAD_STRIP
            case Primitves.PATCHES:
                return GL_PATCHES
            case _:
                return None