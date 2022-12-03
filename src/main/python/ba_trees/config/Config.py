from __future__ import annotations

from pathlib import Path

from ba_trees.config.ConfigDirectories import ConfigDirectories
from default import ConfigJSONFile, Configuration


class Config(Configuration):
    __config: Config = None
    
    def __init__(self, file: Path):
        super().__init__()
        
        self.file = file
        ConfigJSONFile.readConfigFromFile(file, self)
    
    def save(self):
        print(self.file)
        ConfigJSONFile.saveConfigToFile(self.file, self)
    
    @staticmethod
    def getConfig() -> Config:
        if Config.__config == None:
            Config.__config = Config(Path(ConfigDirectories.getConfigDirectories().getConfigFolder()).joinpath("config.json"))
        return Config.__config