from __future__ import annotations
from default import ReplaceArgs

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
        args = ReplaceArgs.replaceArgs(*args)
        xprint(args, **kwargs)
    
    @staticmethod
    def getConsole() -> Console:
        if Console.static_console == None:
            Console.static_console = Console()
        return Console.static_console




def print(*args, **kwargs):
    Console.getConsole().write(*args, **kwargs)