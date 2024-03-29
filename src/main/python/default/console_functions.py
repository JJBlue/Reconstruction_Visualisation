def confirm_dialog(message: str, default_value: bool = True) -> bool:
    default_string = "[" + ("Y/n" if default_value == True else "y/N") + "]"
    result = input(message + ": " + default_string)
    
    no = ["no", "n", "nein"]
    yes = ["yes", "y", "ja", "j"]
    
    result = result.lower()
    
    if result in no:
        return False
    elif result in yes:
        return True
    return default_value