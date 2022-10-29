###############
### Imports ###
###############

import importlib.util
import os
import subprocess
import sys

from default import confirm_dialog


#################
### Functions ###
#################
def check_installation(packages: list) -> bool:
    not_installed_packages = []

    ### Check for packages
    print("Überprüfe, ob alle Module vorhanden sind.")
    for pkg in packages:
        if pkg in sys.modules:
            print(f"{pkg} already in sys.modules")
        elif (spec := importlib.util.find_spec(pkg)) is not None:
            print(f"Module \"{pkg}\" already installed")
        else:
            print(f"Can't find the {pkg} module")
            not_installed_packages.append(pkg)
    
    print()
            
    if not install_packages(not_installed_packages) :
        return False
    
    # Remove unused/old packages (not used yet)
    
    ### Restart
    if len(not_installed_packages) > 0 :
        restart_program()
    
    return True

def install_packages(packages: list) -> bool:
    if len(packages) == 0:
        print("Alle Module sind vorhanden.")
        return True
    
    print("Folgende Module fehlen und werden installiert:")
    print("\t" + "\n\t".join(packages))
    print()
    
    if not confirm_dialog("Module installieren", True):
        return False
    
    for pkg in packages:
        print(f"Installing Module: {pkg}")
        
        result = subprocess.check_call(["pip", "install", pkg])
        if result > 0 :
            print(f"Module installation failed: {pkg}")
            print(f"Exit Status: {result}")
            return False
        
        print(f"Module installed: {pkg}")
        
        #spec = importlib.util.find_spec(pkg)
        #module = importlib.util.find_spec(spec)
        #sys.modules[pkg] = module
        #spec.loader.exec_module(module)
        #print(f"{pkg!r} has been imported")
        
    return True
    
def remove_packages(packages: list) -> bool:
    if len(packages) == 0:
        print("Keine Module zum deinstallieren gefunden")
        return True
    
    print("Folgende Module werden deinstalliert:")
    print("\t" + "\n\t".join(packages))
    print()
    
    if not confirm_dialog("Module deinstallieren", False):
        return False
    
    for pkg in packages:
        print(f"Deinstall Module: {pkg}")
        
        result = subprocess.check_call(["pip", "uninstall", pkg])
        if result > 0 :
            print(f"Module uninstallation failed: {pkg}")
            print(f"Exit Status: {result}")
            return False
        
        print(f"Module uninstalled: {pkg}")

    return True

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)
    sys.exit(0)