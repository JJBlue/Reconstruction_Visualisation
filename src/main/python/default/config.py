from __future__ import annotations

# Value can only be a Object or ConfigurationSection
class ConfigurationSection:
    def __init__(self, config: Configuration):
        self._nodes: dict = {}
        self._root = config
        self._seperator = "."
    
    def isSet(self, path: str) -> bool:
        paths: list = path.split(self._seperator)
        size: int = len(paths)
        config: ConfigurationSection = self.__getConfigurationSection(paths, 0, size - 2)
        
        if config == None:
            return False
        
        return path[size - 1] in config._nodes
    
    def set(self, path: str, value: object) -> bool:
        paths: list = path.split(self._seperator)
        size: int = len(paths)
        config: ConfigurationSection = self.__createConfigurationSection(paths, 0, size - 2)
        
        if config == None:
            return False
        
        config._nodes[paths[size - 1]] = value
        return True
    
    def get(self, path: str) -> object:
        paths: list = path.split(self._seperator)
        size: int = len(paths)
        config: ConfigurationSection = self.__getConfigurationSection(paths, 0, size - 2)
        
        if config == None:
            return None
        
        key: str = paths[size - 1]
        
        if not (key in config._nodes):
            return None
        
        return config._nodes[key]
    
    def getKeys(self):
        return self._nodes.keys()
    
    def getRoot(self) -> Configuration:
        return self._root
    
    def createConfigurationSection(self, path: str):
        paths: list = path.split(self._seperator)
        return self.__createConfigurationSection(paths, 0, len(paths) - 1)
        
    def __createConfigurationSection(self, path: list, index: int, end_index: int) -> ConfigurationSection:
        section: str = path[index]
        config: ConfigurationSection = self
        
        while index <= end_index:
            section: str = path[index]
            
            if not (section in config._nodes):
                next_config = ConfigurationSection(config._root)
                config._nodes[section] = next_config
                config = next_config
            else:
                value = config._nodes[section]
            
                if not isinstance(value, ConfigurationSection):
                    return None
                
                config = value
            
            index += 1
        
        return config
    
    def getConfigurationSection(self, path: str):
        paths: list = path.split(self._seperator)
        return self.__getConfigurationSection(paths, 0, len(paths) - 1)
    
    def __getConfigurationSection(self, path: list, index: int, end_index: int) -> ConfigurationSection:
        section: str = path[index]
        config: ConfigurationSection = self
        
        while index <= end_index:
            section: str = path[index]
            
            if not (section in config._nodes):
                return None
            
            value = config._nodes[section]
            
            if not isinstance(value, ConfigurationSection):
                return None
            
            config = value
            
            index += 1
        
        return config
        
class Configuration(ConfigurationSection):
    def __init__(self):
        super().__init__(self)