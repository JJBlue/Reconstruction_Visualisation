from __future__ import annotations
import os

from pathlib import Path
from default import Args, ArgsEnum

class Directories:
    static_default_directories = None
    
    def __init__(self, working_dir: str):
        self.working_directory: str = working_dir
        self.config_folder: str = Path(self.working_directory).joinpath("config")
    
    def getWorkingDirectory(self) -> str:
        return self.working_directory
    
    def getConfigFolder(self) -> str:
        return self.config_folder
    
    @staticmethod
    def getDirectories() -> Directories:
        if(Directories.static_default_directories == None):
            args: Args = Args.getSystemArgs()
            
            work_dir: str = None
            if(args.hasArg(ArgsEnum.Working_Directory)):
                work_dir = args.getArg(ArgsEnum.Working_Directory)
            else:
                work_dir = os.getcwd()
            
            Path(work_dir).mkdir(parents=True, exist_ok=True)
            Directories.static_default_directories = Directories(work_dir)
        
        return Directories.static_default_directories
        