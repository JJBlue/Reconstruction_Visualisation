class Programm:
    def bind(self):
        pass
    
    def unbind(self):
        pass
    
    def uniform(self, name: str, value, arg0: int = 0):
        raise Exception(f"Type not found: {type(value)}")
    
    def addShaders(self, *shaders) -> bool:
        raise NotImplementedError()