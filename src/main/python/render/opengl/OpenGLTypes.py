from OpenGL.GL import *

from render.data import PrimitiveType, Primitves


class Types:
    @staticmethod
    def PrimitiveTypeToOpenGL(pt: PrimitiveType):
        if pt == PrimitiveType.BYTE:
            return GL_BYTE
        elif pt == PrimitiveType.UNSIGNED_BYTE:
            return GL_UNSIGNED_BYTE
        elif pt == PrimitiveType.SHORT:
            return GL_SHORT
        elif pt == PrimitiveType.UNSIGNED_SHORT:
            return GL_UNSIGNED_SHORT
        elif pt == PrimitiveType.INT:
            return GL_INT
        elif pt == PrimitiveType.UNSIGNED_INT:
            return GL_UNSIGNED_INT
        elif pt == PrimitiveType.FIXED:
            return GL_FIXED
        elif pt == PrimitiveType.HALF_FLOAT:
            return GL_HALF_FLOAT
        elif pt == PrimitiveType.FLOAT:
            return GL_FLOAT
        elif pt == PrimitiveType.DOUBLE:
            return GL_DOUBLE
        
        return None
    
    @staticmethod
    def PrimitivesToOpenGL(pt: Primitves):
        if pt == Primitves.POINTS:
            return GL_POINTS
        elif pt == Primitves.LINES:
            return GL_LINES
        elif pt == Primitves.LINE_STRIP:
            return GL_LINE_STRIP
        elif pt == Primitves.LINE_LOOP:
            return GL_LINE_LOOP
        elif pt == Primitves.LINES_ADJACENCY:
            return GL_LINES_ADJACENCY
        elif pt == Primitves.LINE_STRIP_ADJACENCY:
            return GL_LINE_STRIP_ADJACENCY
        elif pt == Primitves.TRIANGLES:
            return GL_TRIANGLES
        elif pt == Primitves.TRIANGLE_STRIP:
            return GL_TRIANGLE_STRIP
        elif pt == Primitves.TRIANGLE_FAN:
            return GL_TRIANGLE_FAN
        elif pt == Primitves.TRIANGLES_ADJACENCY:
            return GL_TRIANGLES_ADJACENCY
        elif pt == Primitves.TRIANGLE_STRIP_ADJACENCY:
            return GL_TRIANGLE_STRIP_ADJACENCY
        elif pt == Primitves.QUADS:
            return GL_QUADS
        elif pt == Primitves.QUAD_STRIP:
            return GL_QUAD_STRIP
        elif pt == Primitves.PATCHES:
            return GL_PATCHES
        
        return None