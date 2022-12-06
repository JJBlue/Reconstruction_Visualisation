from glm import vec2, fvec2, vec3, fvec3, vec4, fvec4, mat4x4
import glm

from render.render import Camera


class MousePicking:
    
    """
        Tutorials:
            https://antongerdelan.net/opengl/raycasting.html
            https://www.youtube.com/watch?v=DLKN0jExRIM
    
        Local Space
            |
            | Model Matrix
            |
        World Space    (My Objects)
            |
            | View Matrix
            |
        Eye Space
            |
            | Projection Matrix
            |
        Homogeneous clip space
            |
            | Perspective Division (OpenGL)
            |
        Normalised Device Space    (Perspective Division)
            |
            | Simple Equation
            |
        Viewport Space
    """
    
    @staticmethod
    def getRayFromCamera(mouse: vec2, frame_size: vec2, camera: Camera) -> vec3:
        return MousePicking.getRay2(mouse, frame_size, camera.getProjection(), camera.getView())
    
    @staticmethod
    def getRay(mouse: vec2, frame_size: vec2, projectionMatrix: mat4x4, viewMatrix: mat4x4) -> vec3:
        """
        mouse:        (x, y)
        frame_size:    (width, height)
        """
        
        inverse_projection_matrix: mat4x4 = glm.inverse(projectionMatrix) # TODO: Maybe store Inverse Matrix in the Camrea
        inverse_view_matrix: mat4x4 = glm.inverse(viewMatrix) # TODO: Maybe store Inverse Matrix in the Camrea
        
        nds: vec2 = MousePicking.toNormalisedDeviceSpace(mouse, frame_size)
        hcs_ray: vec4 = MousePicking.toHomogeneousClipSpaceRay(nds)
        es_ray: vec4 = MousePicking.toEyeSpaceRay(hcs_ray, inverse_projection_matrix)
        ws_ray: vec3 = MousePicking.toWorldSpaceRay(es_ray, inverse_view_matrix)
        
        return ws_ray
    
    @staticmethod
    def toWorldSpaceRay(eye_space: vec4, inverse_view_matrix: mat4x4) -> vec3:
        tmp_ws_ray: vec4 = inverse_view_matrix * eye_space
        
        ws_ray: vec3 = fvec3(tmp_ws_ray.x, tmp_ws_ray.y, tmp_ws_ray.z)
        ws_ray = glm.normalize(ws_ray) # Not necessary
        
        return ws_ray
    
    @staticmethod
    def toEyeSpaceRay(homogeneous_clip_space: vec4, inverse_projection_matrix: mat4x4) -> vec4:
        es_ray: vec4 = inverse_projection_matrix * homogeneous_clip_space
        
        vec4.z = -1.0 # Ray points into the Frame
        vec4.w = 0.0
        
        return es_ray
    
    @staticmethod
    def toHomogeneousClipSpaceRay(normalised_device_space: vec2) -> vec4:
        hcs_ray: vec4 = fvec4(
                            normalised_device_space.x,
                            normalised_device_space.y,
                            -1.0, # Ray points into the Frame
                            1.0
                        )
        return hcs_ray
    
    @staticmethod
    def toNormalisedDeviceSpace(mouse: vec2, frame_size: vec2) -> vec2:
        """
            mouse: (x, y)       x: 0 - width
                                y: 0 - height
                                Mouse Origin (0, 0): Bottom Left
            frame_size: (width, height)
            
            return  x: -1.0 - 1.0
                    y: -1.0 - 1.0
        """
        
        
        nds: vec2 = fvec2(0.0)
        
        nds.x = (2.0 * mouse.x) / frame_size.x - 1.0
        nds.y = (2.0 * mouse.y) / frame_size.y - 1.0 # Eventuell -y in qt
        
        return nds
        