import re

from __future__ import annotations

# Override print Method
xprint = print

# Example:
#    %name%[short=yes,test=no]
#    Hello du %name%[short="yes",test=no] hallo %test% test

class Console:
    static_console = None
    
    def __init__(self):
        pass
    
    def write(self, *args, **kwargs):
        #for arg in ConsoleArg.getMatches(*args)
        xprint(*args, **kwargs)
    
    @staticmethod
    def getConsole() -> Console:
        if Console.static_console == None:
            Console.static_console = Console()
        return Console.static_console

class ConsoleArg:
    
    def __init__(self):
        self.original: str = None
        self.name: str = None
        self.settings: dict = {}
    
    @staticmethod
    def getMatches(text: str) -> list:
        result: list = []
        
        match_args = ConsoleRegex.args.findall(text)
        
        if not match_args:
            return result
        
        # Args
        for arg in match_args:
            carg: ConsoleArg = ConsoleArg()
            carg.original = arg
            
            match_name_settings = ConsoleRegex.arg_name_and_settings.match(arg)
            
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
                match_settings = ConsoleRegex.settings.findall(settings)
                
                if not match_settings:
                    continue
                
                # Settings: Key and Value
                for setting in match_settings:
                    match_key_value = ConsoleRegex.setting_key_and_value.match(setting)
                    
                    if not match_key_value:
                        continue
                    
                    match_key_value_size = len(match_key_value.groups())
                    
                    if match_key_value_size >= 2:
                        setting_name = match_key_value.group(1)
                        setting_value = match_key_value.group(2)
                        carg.settings[setting_name] = setting_value
                    elif match_key_value_size >= 1:
                        setting_name = match_key_value.group(1)
                        carg.settings[setting_name] = None
        
        return result
    
    

class ConsoleRegex:
    # (%\w+%(?:\[.*\])?)
    # "%name%" | "%name%[...]"
    args = re.compile("(%\w+%(?:\[.*\])?)")
    
    # %(\w+)%(?:\[(.*)\])?
    # "%name%[...]" --> "name" & "..."
    arg_name_and_settings = re.compile("%(\w+)%(?:\[(.*)\])?")
    
    # ([^=,\s"]+(?:\s*=\s*"?(?:[^\\",]|(?<=\\)")*"?)?)
    # 'test="test", Test, hello=".", da = 2' --> 'test="test"' & ...
    settings = re.compile("([^=,\\s\"]+(?:\\s*=\\s*\"?(?:[^\\\\\",]|(?<=\\\\)\")*\"?)?)")
    
    # ([^=,\s"]+)(?:\s*=\s*"?((?:[^\\"]|(?<=\\)")*)"?)?
    setting_key_and_value = re.compile("([^=,\\s\"]+)(?:\\s*=\\s*\"?((?:[^\\\\\"]|(?<=\\\\)\")*)\"?)?")
    
    pass


def print(*args, **kwargs):
    Console.getConsole().write(*args, **kwargs)