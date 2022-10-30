import locale

from configparser import ConfigParser, ExtendedInterpolation


class Language:
    name: str = None
    code: str = None
    alias: list = None
    
    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code
    
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
        raise Exception("Method not implemented")

class Languages:
    
    languages: dict = {}
    
    def getLanguages(self) -> list:
        pass # TODO
    
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
        



class NodeDictionary:
    def get(self, key: str) -> bool:
        raise Exception("Method not implemented")
    
    def set(self, key: str, value: str) -> bool:
        raise Exception("Method not implemented")
    
    def remove(self, key: str) -> bool:
        raise Exception("Method not implemented")

class LanguageDictionary(NodeDictionary):
    
    languages: dict = {} # <Language, Node>
    
    def getLanguages(self) -> list:
        pass
    
    def addLanguage(self) -> bool:
        pass
    
    def removeLanguage(self) -> bool:
        pass


class Node(NodeDictionary):
    
    dictionary: dict = {}
    
    def getDefinitions(self) -> dict:
        pass
    
    def getNodes(self) -> list:
        pass
    
