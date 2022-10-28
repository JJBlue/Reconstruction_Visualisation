###############
### Imports ###
###############

import importlib.util
import subprocess
import sys

from default import confirm_dialog

############
### Main ###
############

packages = ["PyQt6"]
not_installed_packages = []

### Check for packages
print("Überprüfe, ob alle Module vorhanden sind.")
for pkg in packages:
    if pkg in sys.modules:
        print(f"{pkg} already in sys.modules")
    elif (spec := importlib.util.find_spec(pkg)) is not None:
        #module = importlib.util.find_spec(spec)
        #sys.modules[pkg] = module
        #spec.loader.exec_module(module)
        #print(f"{pkg!r} has been imported")
        print(f"Modul \"{pkg}\" already installed")
    else:
        print(f"Can't find the {pkg} module")
        not_installed_packages.append(pkg)

print()
        

### Install Packages
if not not_installed_packages:
    print("Alle Module sind vorhanden.")
else:
    print("Folgende Module fehlen:")
    print("\t" + "\n\t".join(not_installed_packages))
    print()
    
    if confirm_dialog("Module installieren"):
        for pkg in not_installed_packages:
            print(f"Installing Module: {pkg}")
            subprocess.check_call(["pip", "install", pkg])
            print(f"Module installed: {pkg}")