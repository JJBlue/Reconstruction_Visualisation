from pathlib import Path

from OpenGL.raw.GL.VERSION.GL_2_0 import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER

from ba_trees.config.ConfigDirectories import ConfigDirectories
from default.Synchronization import synchronized
from render.functions import RenderDataStorages
from render.opengl import OpenGLShader
from render.render.Shader import ShaderFile, ShaderGroup


class OpenGLData:
    __loaded = False
    
    @staticmethod
    @synchronized
    def load():
        if OpenGLData.__loaded:
            return
        
        # Shaders
        shader_vert = OpenGLShader(OpenGLData.getShaderFile(GL_VERTEX_SHADER, "point_cloud.vert"))
        shader_frag = OpenGLShader(OpenGLData.getShaderFile(GL_FRAGMENT_SHADER, "point_cloud.frag"))
        shader = ShaderGroup(shader_vert, shader_frag)
        RenderDataStorages.getShaders().put("point_cloud", shader)
        
        shader_vert = OpenGLShader(OpenGLData.getShaderFile(GL_VERTEX_SHADER, "images.vert"))
        shader_frag = OpenGLShader(OpenGLData.getShaderFile(GL_FRAGMENT_SHADER, "images.frag"))
        shader = ShaderGroup(shader_vert, shader_frag)
        RenderDataStorages.getShaders().put("images", shader)
        
        shader_vert = OpenGLShader(OpenGLData.getShaderFile(GL_VERTEX_SHADER, "coordinate_system.vert"))
        shader_frag = OpenGLShader(OpenGLData.getShaderFile(GL_FRAGMENT_SHADER, "coordinate_system.frag"))
        shader = ShaderGroup(shader_vert, shader_frag)
        RenderDataStorages.getShaders().put("coordinate_system", shader)
        
        shader_vert = OpenGLShader(OpenGLData.getShaderFile(GL_VERTEX_SHADER, "FrameBufferImage.vert"))
        shader_frag = OpenGLShader(OpenGLData.getShaderFile(GL_FRAGMENT_SHADER, "FrameBufferImage.frag"))
        shader = ShaderGroup(shader_vert, shader_frag)
        RenderDataStorages.getShaders().put("framebuffer_image", shader)
        
        # Finished
        OpenGLData.__loaded = True
    
    @staticmethod
    def getShaderFile(shader_type, file: str) -> ShaderFile:
        if not Path(file).exists():
            dirs = ConfigDirectories.getConfigDirectories()
            file = Path(dirs.getShaderFolder()).joinpath(file)
        
        return ShaderFile(shader_type, file)