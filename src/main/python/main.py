import ba_trees

def startup_main():
    from ba_trees import premain
    premain()
    
    from ba_trees import main
    main()

    from ba_trees import postmain
    postmain()



if __name__ == "__main__":
    startup_main()