import sys

def postmain():
    print("Main initialisation started")
    
    ### Window
    from ba_trees.gui.gui import Application
    
    app = Application()
    app.window.show()
    
    sys.exit(app.getApp().exec())