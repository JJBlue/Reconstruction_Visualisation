import sys
import os.path

from default import print
from default import check_installation
from default import Args

def premain():
    print("Pre Initalisation started")
    
    print("Read Args")
    Args.getSystemArgs()
    
    print("Other")
    
    ### Dependencies
    packages = ["PyQt6", "configparser"] # PyQt6-Qt6, PyQt6-sip, PyQt6
    if not check_installation(packages) :
        print("Installation failed")
        sys.exit(1)
    
def loadLanguage():
    ### Language
    file = ""
    if not os.path.isfile(file):
        return
    
    
    