from __future__ import annotations

from enum import Enum


class RenderBufferInternalFormat(Enum):
    RED = 0
    R8 = 1
    
    RED_INTEGER = 2
    R8UI = 3
    R8I = 4
    R16UI = 5
    R16I = 6
    R32UI = 7
    R32I = 8

    RG = 9
    RG8 = 10

    RG_INTEGER = 11
    RG8UI = 12
    RG8I = 13
    RG16UI = 14
    RG16I = 15
    RG32UI = 16
    RG32I = 17
    
    RGB = 18
    RGB8 = 19
    RGB565 = 20
    
    RGBA = 21
    RGBA8 = 22
    SRGB8_ALPHA8 = 23
    RGB5_A1 = 24
    RGBA4 = 25
    RGB10_A2 = 26
    
    RGBA_INTEGER = 27
    RGBA8UI = 28
    RGBA8I = 29
    RGB10_A2UI = 30
    RGBA16UI = 31
    RGBA16I = 32
    RGBA32I = 33
    RGBA32UI = 34
    
    DEPTH_COMPONENT = 35
    DEPTH_COMPONENT16 = 36
    DEPTH_COMPONENT24 = 37
    DEPTH_COMPONENT32F = 38
    
    DEPTH_STENCIL = 39
    DEPTH24_STENCIL8 = 40
    DEPTH32F_STENCIL8 = 41
    
    STENCIL = 42
    STENCIL_INDEX8 = 43