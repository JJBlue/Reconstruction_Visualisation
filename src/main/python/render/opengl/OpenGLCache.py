from render.data import TextureData, Geometry
from render.opengl import OpenGLTexture
from render.opengl.OpenGLMesh import OpenGLMesh


class OpenGLCache:
    __cache_mesh: dict = {}
    __cache_texture: dict = {}
    
    @staticmethod
    def getMesh(geo: Geometry) -> OpenGLMesh:
        if not (geo in OpenGLCache.__cache_mesh):
            return None
        return OpenGLCache.__cache_mesh[geo]
    
    @staticmethod
    def getOrCreateMesh(geo: Geometry) -> OpenGLMesh:
        if not (geo in OpenGLCache.__cache_mesh):
            opengl_geo: OpenGLTexture = OpenGLMesh(geo)
            OpenGLCache.__cache_mesh[geo] = opengl_geo
            return opengl_geo
        return OpenGLCache.__cache_mesh[geo]
    
    @staticmethod
    def getTexture(tex: TextureData) -> OpenGLTexture:
        if not (tex in OpenGLCache.__cache_texture):
            return None
        return OpenGLCache.__cache_texture[tex]
    
    @staticmethod
    def getOrCreateTexture(tex: TextureData) -> OpenGLTexture:
        if not (tex in OpenGLCache.__cache_texture):
            opengl_tex: OpenGLTexture = OpenGLTexture(tex)
            OpenGLCache.__cache_texture[tex] = opengl_tex
            return opengl_tex
        return OpenGLCache.__cache_texture[tex]