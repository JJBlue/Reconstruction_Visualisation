from pathlib import Path

from OpenGL.raw.GL.VERSION.GL_2_0 import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER

from ba_trees.config.ConfigDirectories import ConfigDirectories
from default.Synchronization import synchronized
from render.data.GeometryStructures import CoordinateSystem
from render.functions import RenderDataStorage
from render.opengl import OpenGLShader, OpenGLMesh
from render.render.Shader import ShaderFile


class OpenGLData:
    __loaded = False
    
    @staticmethod
    @synchronized
    def load():
        if OpenGLData.__loaded:
            return
        
        # Shaders
        shader = OpenGLShader()
        shader.addShaderSource(
            OpenGLData.getShaderFile(GL_VERTEX_SHADER, "point_cloud.vert"),
            OpenGLData.getShaderFile(GL_FRAGMENT_SHADER, "point_cloud.frag")
        )
        RenderDataStorage.getShaders().put("point_cloud", shader)
        
        shader = OpenGLShader()
        shader.addShaderSource(
            OpenGLData.getShaderFile(GL_VERTEX_SHADER, "images.vert"),
            OpenGLData.getShaderFile(GL_FRAGMENT_SHADER, "images.frag")
        )
        RenderDataStorage.getShaders().put("images", shader)
        
        shader = OpenGLShader()
        shader.addShaderSource(
            OpenGLData.getShaderFile(GL_VERTEX_SHADER, "coordinate_system.vert"),
            OpenGLData.getShaderFile(GL_FRAGMENT_SHADER, "coordinate_system.frag")
        )
        RenderDataStorage.getShaders().put("coordinate_system", shader)
        
        
        # Meshes
        mesh = OpenGLMesh(CoordinateSystem())
        RenderDataStorage.getMeshes().put("coordinate_system", mesh)
        
        # Finished
        OpenGLData.__loaded = True
    
    @staticmethod
    def getShaderFile(shader_type, file: str) -> ShaderFile:
        if not Path(file).exists():
            dirs = ConfigDirectories.getConfigDirectories()
            file = Path(dirs.getShaderFolder()).joinpath(file)
        
        return ShaderFile(shader_type, file)