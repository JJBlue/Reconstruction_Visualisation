import locale

from configparser import ConfigParser, ExtendedInterpolation
from default import Directories

# Langs
class Language:
    def __init__(self, name: str, code: str):
        self.name: str = name
        self.code: str = code
        self.alias: list = []
    
    def getCode(self):
        return self.code
    
    def getName(self):
        return self.name
    
    def getAlias(self) -> list:
        return self.alias
    
    def addAlias(self, alias: str):
        self.alias.add(alias)
        # TODO add to Languages

    def removeAlias(self, alias: str):
        self.alias.remove(alias)
        # TODO remove from Languages

class Languages:
    static_default_languages = None
    
    def __init__(self):
        self.languages: dict = {}
        self.directories: Directories = None
    
    def getLanguages(self) -> list:
        return self.languages.keys()
    
    def getLanguage(self, code: str) -> Language:
        return self.languages.get(code.lower())
    
    def addLanguage(self, lang: Language) -> bool:
        self.languages.add(lang.code.lower(), lang)
        
        for code in lang.alias :
            self.languages.add(code.lower(), lang)
            
        return True
    
    def removeLanguage(self, code: str) -> bool:
        if not self.languages.containsKey(code) :
            return False
        
        lang = self.languages.get(code.lower())
        self.languages.remove(lang.code.lower())
        
        for code in lang.alias :
            self.languages.remove(code.lower())
    
    @staticmethod
    def getDefaultLanguages():
        if Languages.static_default_languages == None:
            Languages.static_default_languages = Languages()
        return Languages.static_default_languages


# Language Config
class NodeDictionary:
    def __init__(self, directory: Directories = Directories.getDefaultDirectories()):
        self.directories = directory
    
    def get(self, key: str) -> bool:
        raise Exception("Method not implemented")
    
    def set(self, key: str, value: str) -> bool:
        raise Exception("Method not implemented")
    
    def remove(self, key: str) -> bool:
        raise Exception("Method not implemented")

class LanguageDictionary(NodeDictionary):
    def __init__(self):
        self.languages: dict = {} # <Language, Node>
    
    def getLanguages(self) -> list:
        return self.languages.keys()
    
    def addLanguage(self) -> bool:
        pass
    
    def removeLanguage(self) -> bool:
        pass


class Node(NodeDictionary):
    def __init__(self):
        self.dictionary: dict = {}
    
    def getDefinitions(self) -> dict:
        pass
    
    def getNodes(self) -> list:
        pass
    
