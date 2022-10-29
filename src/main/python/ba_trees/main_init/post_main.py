import sys

def postmain():
    print("Main initialisation started")
    
    from ba_trees import Window
    
    ### Window
    window = Window()
    window.show()
    
    sys.exit(window.getApp().exec())