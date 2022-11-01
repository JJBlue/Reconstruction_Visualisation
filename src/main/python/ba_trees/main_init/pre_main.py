import sys
import os.path

from default import print
from default import check_installation
from default import Args

def premain():
    print("Pre Initalisation started")
    
    print("Read Args")
    Args.getSystemArgs()
    
    print("Load Languages")
    from default import Directories
    lang_folder = os.path.join(Directories.getDefaultDirectories().getWorkingDirectory(), "lang")
    if not os.path.exists(lang_folder):
        os.mkdir(lang_folder)
    
    print(lang_folder)
    
    lang_en = os.path.join(lang_folder, "en.ini")
    if not os.path.exists(lang_en):
        with open(lang_en, 'a') as out:
            out.write(
            """
            [DEFAULT]
            language = en
            
            
            [en]
            
            
            """
            )
    
    
    
    
    ### Dependencies
    print("Show Dependencies")
    
    packages = ["PyQt6", "configparser"] # PyQt6-Qt6, PyQt6-sip, PyQt6
    if not check_installation(packages) :
        print("Installation failed")
        sys.exit(1)
    
def loadLanguage():
    ### Language
    file = ""
    if not os.path.isfile(file):
        return
    
    
    