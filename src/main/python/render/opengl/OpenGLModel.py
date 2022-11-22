from render.data import ModelData
from render.opengl.OpenGLCache import OpenGLCache
from render.render import Model


class OpenGLModel(Model):
    def __init__(self, data: ModelData):
        super().__init__(data)
        
        for geo in data.getGeometries():
            self.meshes.append(OpenGLCache.getOrCreateMesh(geo))
        
        for tex in data.getTextures():
            self.textures.append(OpenGLCache.getOrCreateTexture(tex))
            # TODO load parallel
            # print(f"Load Image: {image_file}")
            # import multiprocessing as mp
            # pool = mp.Pool(processes=4)
            # results = pool.map(ColmapImage.loadImage, images)
            # self.images = results