


def main():
    # Load Project Default Factories
    from ba_trees.workspace import Projects
    from ba_trees.workspace.colmap.ColmapProject import ColmapProject
    
    Projects.addTypeProject("colmap", lambda folder: ColmapProject(folder))
    
    # Load Config
    from ba_trees.config.Config import Config
    
    Config.getConfig()