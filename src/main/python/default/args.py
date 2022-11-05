from __future__ import annotations
import sys

from enum import StrEnum

class ArgsEnum(StrEnum):
    Working_Directory = "workdir"


class Args:
    Systemargs = None
    
    def __init__(self, args: list):
        ### Variablen
        self.arguments: dict = {}
        
        ### Read Args
        key: str = None
        tmp: list = []
        
        for arg in args:
            if arg.startswith("-"):
                if key != None:
                    if not tmp:
                        self.arguments[key] = None
                    elif len(tmp) == 1:
                        self.arguments[key] = tmp[0]
                    else:
                        self.arguments[key] = tmp
                
                tmp.clear()
                
                key = arg
                while key.startswith("-"):
                    key = key[1:]
                
            else:
                tmp.append(arg)
                
        
        if key != None:
            if not tmp:
                self.arguments[key] = None
            elif len(tmp) == 1:
                self.arguments[key] = tmp[0]
            else:
                self.arguments[key] = tmp
        
    
    def hasArg(self, key: str):
        return key in self.arguments
    
    def getArg(self, key: str):
        return self.arguments[key]
    
    def getArgs(self):
        return self.arguments.keys()
    
    def setArg(self, key: str, value):
        self.arguments[key] = value
    
    @classmethod
    def read(cls, args: list):
        return Args(args)
    
    @staticmethod
    def getSystemArgs():
        if Args.Systemargs == None:
            Args.Systemargs = Args(sys.argv)
        return Args.Systemargs
    
    @staticmethod
    def loadArgs(args: Args):
        return None