import sys

from ba_trees import Window

def main():
    print("Running Application")
    
    window = Window()
    window.show()
    
    sys.exit(window.getApp().exec())


if __name__ == "__main__":
    main()