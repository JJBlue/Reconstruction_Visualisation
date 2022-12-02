import json
from pathlib import Path

from default.config import Configuration, ConfigurationSection


class ConfigJSONFile:
    @staticmethod
    def readConfigFromFile(file: Path, config: Configuration = None) -> ConfigurationSection:
        data: dict = {}
        
        # Load from File
        if file.exists():
            with open(file, encoding="UTF-8") as f:
                data = json.load(f)
        
        return ConfigJSONFile.readConfig(config, config, data)
    
    @staticmethod
    def readConfig(config: Configuration, section: ConfigurationSection, data: dict) -> ConfigurationSection:
        if config == None:
            config = Configuration()
            section = config
        elif section == None:
            section = ConfigurationSection(config)
        
        for key in data.keys():
            tmp = data[key]
            
            if isinstance(tmp, dict):
                section.set(key, ConfigJSONFile.readConfig(config, None, tmp))
            else:
                section.set(key, tmp)
        
        return section
    
    @staticmethod
    def saveConfigToFile(file: Path, config: ConfigurationSection):
        # Save to file
        with open(file, "w+", encoding="UTF-8") as f:
            json.dump(ConfigJSONFile.saveConfig(config), f)
    
    @staticmethod
    def saveConfig(config: ConfigurationSection) -> dict:
        data: dict = {}
        
        for key in config.getKeys():
            tmp = config.get(key)
            
            if isinstance(tmp, ConfigurationSection):
                data[key] = ConfigJSONFile.saveConfig(tmp)
            else:
                data[key] = tmp
        
        return data