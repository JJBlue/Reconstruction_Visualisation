from ba_trees.gui.render.Location import Location

class Entity:
    def __init__(self):
        self.position = Location()
    
    def getPosition(self):
        return self.position
    
    def getView(self):
        # view = glm::lookAt(   glm::vec3(0.0, 0.0, 3.0)
        #                glm::vec3(0.0, 0.0, 0.0)
        #                glm::vec3(0.0, 1.0, 0.0))
        pass