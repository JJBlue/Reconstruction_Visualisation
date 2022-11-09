from ba_trees.gui.render import Location, Position, Entity

class Camera(Entity):
    def __init__(self):
        self.position = Location(0, 0, 3)
        self.target = Position(0, 0, 0)
        self.direction = Position()
        
        self.right_up = Position(0.0, 1.0, 0.0)
        self.right = Position()
        
        self.up = Position()
        
        self.update()
    
    def update(self):
        # self.direction = glm::normalize(self.position - self.target)
        # self.right = glm::normalize(glm::cross(self.right_up, self.direction))
        # self.up = glm::cross(self.direction, self.right)
        
        pass
    
    def getPosition(self):
        return self.position