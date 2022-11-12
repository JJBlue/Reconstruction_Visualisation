from pathlib import Path

from ba_trees.config.ConfigDirectories import ConfigDirectories
from render import ShaderFile


class Shaders:
    @staticmethod
    def getShaderFile(shader_type, file: str) -> ShaderFile:
        if not Path(file).exists():
            dirs = ConfigDirectories.getDefaultConfigDirectories()
            file = Path(dirs.getShaderFolder()).joinpath(file)
        
        return ShaderFile(shader_type, file)