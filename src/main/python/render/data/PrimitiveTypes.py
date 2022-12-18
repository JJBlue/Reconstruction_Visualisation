from enum import Enum

class PrimitiveType(Enum):
    BYTE = 0
    UNSIGNED_BYTE = 1
    SHORT = 2
    UNSIGNED_SHORT = 3
    INT = 4
    UNSIGNED_INT = 5
    FIXED = 6
    HALF_FLOAT = 7
    FLOAT = 8
    DOUBLE = 9

class Primitves(Enum):
    POINTS = 0
    LINES = 1
    LINE_STRIP = 2
    LINE_LOOP = 3
    LINES_ADJACENCY = 4
    LINE_STRIP_ADJACENCY = 5
    TRIANGLES = 6
    TRIANGLE_STRIP = 7
    TRIANGLE_FAN = 8
    TRIANGLES_ADJACENCY = 9
    TRIANGLE_STRIP_ADJACENCY = 10
    QUADS = 11
    QUAD_STRIP = 12
    PATCHES = 13