from __future__ import annotations

from pathlib import Path

from ba_trees import config
from ba_trees.config.ConfigDirectories import ConfigDirectories
from default import ConfigJSONFile, Configuration


class Config(Configuration):
    __config: config = None
    
    def __init__(self, file: Path):
        super().__init__()
        
        self.file = file
        ConfigJSONFile.readConfigFromFile(file, config)
    
    def save(self):
        print(self.file)
        ConfigJSONFile.saveConfigToFile(self.file, self)
    
    @staticmethod
    def getConfig() -> config:
        if Config.__config == None:
            Config.__config = Config(Path(ConfigDirectories.getConfigDirectories().getWorkingDirectory()).joinpath("config.json"))
        return Config.__config