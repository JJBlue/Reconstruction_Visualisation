from __future__ import annotations
#import locale

from configparser import ConfigParser
from default import Configuration, ConfigurationSection
from default import Directories
from pathlib import Path

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
        
        # Not efficent
        Languages.getDefaultLanguages().removeLanguage(self)
        Languages.getDefaultLanguages().addLanguage(self)

    def removeAlias(self, alias: str):
        self.alias.remove(alias)
        
        # Not efficent
        Languages.getDefaultLanguages().removeLanguage(self)
        Languages.getDefaultLanguages().addLanguage(self)

class Languages:
    static_default_languages = None
    static_default_language = None
    
    def __init__(self):
        self.languages: dict = {}
        self.directories: Directories = None
    
    def getLanguages(self) -> list:
        return self.languages.keys()
    
    def getLanguage(self, code: str) -> Language:
        return self.languages[code.lower()]
    
    def createOrGetLanguage(self, code: str) -> Language:
        lang: Language = self.getLanguage(code)
        
        if lang != None:
            return lang
        
        lang = Language(code, code)
        self.addLanguage(lang)
        return lang
    
    def addLanguage(self, lang: Language) -> bool:
        self.languages[lang.code.lower()] = lang
        
        for code in lang.alias :
            self.languages[code.lower()] = lang
            
        return True
    
    def removeLanguage(self, code: str) -> bool:
        if not self.languages.containsKey(code) :
            return False
        
        lang = self.languages.get(code.lower())
        self.languages.remove(lang.code.lower())
        
        for code in lang.alias :
            self.languages.remove(code.lower())
    
    @staticmethod
    def getDefaultLanguages() -> Languages:
        if Languages.static_default_languages == None:
            Languages.static_default_languages = Languages()
            langs: Languages = Languages.static_default_languages
            
            lang: Language = Language("English", "en")
            langs.addLanguage(lang)
            Languages.static_default_language = lang
            
            lang: Language = Language("Deutsch", "de")
            langs.addLanguage(lang)
            
        return Languages.static_default_languages
    
    @staticmethod
    def getDefaultLanguage() -> Language:
        if Languages.static_default_language == None:
            Languages.getDefaultLanguages()
        return Languages.static_default_language


# Language Config
class LanguageDictionary:
    static_default_language_dictionary = None
    
    def __init__(self):
        self._main = Configuration()
        self._languages: dict = {} # <Language, Configuration>
    
    ### Languages
    
    def getLanguages(self) -> list:
        return self._languages.keys()
    
    def getLanguage(self, lang: Language) -> Configuration:
        if not (lang in self._languages):
            return None
        
        return self._languages[lang]
    
    def addLanguage(self, lang: Language) -> bool:
        if lang in self._languages:
            return False
    
        self._languages[lang] = Configuration()
        
        return True
    
    def removeLanguage(self, lang: Language) -> bool:
        if not (lang in self._languages):
            return False
        
        del self._languages[lang]
        return True
    
    ### Configuration
    def isSet(self, lang: Language, path: str) -> bool:
        config: ConfigurationSection = self.getConfigurationSection(lang)
        
        if config == None:
            return False
        
        return config.isSet(path)
    
    def set(self, lang: Language, path: str, value: object) -> bool:
        config: ConfigurationSection = self.getConfigurationSection(lang)
        
        if config == None:
            return None
        
        return config.set(path, value)
    
    def get(self, lang: Language, path: str) -> object:
        config: ConfigurationSection = self.getConfigurationSection(lang)
        
        if config == None:
            return None
        
        return config.get(path)
    
    def getConfigurationSection(self, lang: Language, path: str = None):
        config: ConfigurationSection = self.getLanguage(lang)
        
        if config == None:
            return None
        
        if path != None:
            return config.getConfigurationSection(path)
        
        return config
    
    ### Getter und Setter
    
    def getMain(self) -> ConfigurationSection:
        return self._main
    
    @staticmethod
    def getDefaultLanguageDictionary() -> LanguageDictionary:
        if LanguageDictionary.static_default_language_dictionary == None:
            LanguageDictionary.static_default_language_dictionary = LanguageDictionary()
        return LanguageDictionary.static_default_language_dictionary
    
# Lang Files
class LanguageFile:
    def __init__(self, file: str):
        self.file = file
    
    def load(self) -> bool:
        raise Exception("Method not implemented")
    
    def loadIntoDictionary(self, ld: LanguageDictionary) -> bool:
        raise Exception("Method not implemented")
    
    def save(self) -> bool:
        raise Exception("Method not implemented")
    
    def getFile(self) -> str:
        return self.file

class LanguageFileIni(LanguageFile):
    def __init__(self, file: str):
        super().__init__(file)
        self.config = None
    
    def load(self) -> bool:
        self.config = ConfigParser()
        self.config.read(self.file)
        
        return True
    
    def loadIntoDictionary(self, ld: LanguageDictionary) -> bool:
        self.load()
        
        for section in self.config.sections():
            name: str = section.title().lower()
            config: ConfigurationSection
            
            if name == "main":
                config = ld.getMain()
            else:
                lang: Language = Languages.getDefaultLanguages().createOrGetLanguage(name)
                ld.addLanguage(lang)
                config = ld.getLanguage(lang)
            
            for key, value in self.config.items(section):
                config.set(key, value)
        
        return True
    
    def save(self):
        raise Exception("Method not implemented")
    
        myfile = Path(self.file)
        config = ConfigParser()
        config.read(myfile)
        # config.set(..., ..., ...)
        config.write(myfile.open("w"))
        
        return False
        