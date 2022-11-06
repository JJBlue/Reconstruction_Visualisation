from __future__ import annotations
import re

from default.language import Language, Languages, LanguageDictionary



class ReplaceArgs:
    @staticmethod
    def replaceArgs(text: str) -> str:
        for arg in ReplaceArgs.getArgs(text):
            if arg.result == None:
                continue
            
            text = text.replace(arg.original, arg.result)
            
        return text
    
    @staticmethod
    def getArgs(text: str) -> list:
        args: list = ReplaceArg.getMatches(text)
        
        for arg in args:
            lang: Language = Languages.getDefaultLanguage()
            ld: LanguageDictionary = LanguageDictionary.getDefaultLanguageDictionary()
            
            arg.result = ld.get(lang, arg.name)
            
        return args

class ReplaceArg:
    
    def __init__(self):
        self.original: str = None
        self.name: str = None
        self.settings: dict = {}
        self.result: str = None
    
    @staticmethod
    def getMatches(text: str) -> list:
        result: list = []
        
        match_args = ReplaceRegex.args.findall(text)
        
        if not match_args:
            return result
        
        # Args
        for arg in match_args:
            carg: ReplaceArg = ReplaceArg()
            carg.original = arg
            
            match_name_settings = ReplaceRegex.arg_name_and_settings.match(arg)
            
            if not match_name_settings:
                continue
            
            match_name_settings_size = len(match_name_settings.groups())
            
            # Name
            if match_name_settings_size >= 1:
                name = match_name_settings.group(1)
                carg.name = name
                result.append(carg)
            
            # Settings
            if match_name_settings_size >= 2:
                settings = match_name_settings.group(2)
                
                if settings == None:
                    continue
                
                match_settings = ReplaceRegex.settings.findall(settings)
                
                if not match_settings:
                    continue
                
                # Settings: Key and Value
                for setting in match_settings:
                    match_key_value = ReplaceRegex.setting_key_and_value.match(setting)
                    
                    if not match_key_value:
                        continue
                    
                    match_key_value_size = len(match_key_value.groups())
                    
                    if match_key_value_size >= 2 and match_key_value_size.group(2) != None:
                        setting_name = match_key_value.group(1)
                        setting_value = match_key_value.group(2)
                        carg.settings[setting_name] = setting_value
                    elif match_key_value_size >= 1:
                        setting_name = match_key_value.group(1)
                        carg.settings[setting_name] = None
        
        return result
    
    

class ReplaceRegex:
    # (%\w+%(?:\[.*\])?)
    # "%name%" | "%name%[...]"
    args = re.compile("(%(?:\w|.)+%(?:\[.*\])?)")
    
    # %(\w+)%(?:\[(.*)\])?
    # "%name%[...]" --> "name" & "..."
    arg_name_and_settings = re.compile("%((?:\w|.)+)%(?:\[(.*)\])?")
    
    # ([^=,\s"]+(?:\s*=\s*"?(?:[^\\",]|(?<=\\)")*"?)?)
    # 'test="test", Test, hello=".", da = 2' --> 'test="test"' & ...
    settings = re.compile("([^=,\\s\"]+(?:\\s*=\\s*\"?(?:[^\\\\\",]|(?<=\\\\)\")*\"?)?)")
    
    # ([^=,\s"]+)(?:\s*=\s*"?((?:[^\\"]|(?<=\\)")*)"?)?
    setting_key_and_value = re.compile("([^=,\\s\"]+)(?:\\s*=\\s*\"?((?:[^\\\\\"]|(?<=\\\\)\")*)\"?)?")