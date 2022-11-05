import sys
import os.path

from default import print
from default import check_installation
from default import Args
from default import LanguageFileIni


def premain():
    print("Pre Initalisation started")
    
    print("Read Args")
    Args.getSystemArgs()
    

    
    
    
    
    ### Dependencies
    print("%premain.check_dependencies%")
    
    packages = ["PyQt6", "configparser"] # PyQt6-Qt6, PyQt6-sip, PyQt6
    if not check_installation(packages) :
        print("%installation.failed%")
        sys.exit(1)
    
def loadLanguage():
    print("Load Languages")
    from default import Directories
    lang_folder = os.path.join(Directories.getDefaultDirectories().getWorkingDirectory(), "lang")
    if not os.path.exists(lang_folder):
        os.mkdir(lang_folder)
    
    # Store default settings
    lang_def = os.path.join(lang_folder, "lang.ini")
    if not os.path.exists(lang_def):
        with open(lang_def, 'a') as out:
            out.write(
"""[DEFAULT]
language = en
"""
            )
    
    # Store English settings
    lang_en = os.path.join(lang_folder, "en.ini")
    if not os.path.exists(lang_en):
        with open(lang_en, 'a') as out:
            out.write(
"""[en]
installation.failed=Installation failed
premain.check_dependencies=Check Dependencies
"""
            )
    
    # Load Langauge
    lang_file = LanguageFileIni(lang_def)
    lang_file.load()
    
    
    