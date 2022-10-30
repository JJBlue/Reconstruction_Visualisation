import sys

from default import check_installation

def premain():
    print("Pre Initalisation started")
    
    ### Dependencies
    packages = ["PyQt6", "configparser"] # PyQt6-Qt6, PyQt6-sip, PyQt6
    if not check_installation(packages) :
        print("Installation failed")
        sys.exit(1)
    