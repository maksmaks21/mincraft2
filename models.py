from ursina import*
from perlin_noise import PerlinNoise
from ursina.shaders import basic_lighting_shader
from numpy import floor

class Block(Button):
    def __init__(self, block_type, pos,**kwaegs):
        super().__init__(
            parent=scene,
            model='cube',
            texture='grass',
            position=pos,
            scale=1,
            collider='box',
            origin_y=0.5,
            color=color.color(0,0,random.uniform(0.9,1)),
            shader= basic_lighting_shader,
            **kwaegs
        )


class Map(Entity):
    def __init__(self, **kwargs):
        super().__init__(model=None, collider=None, **kwargs)
        bedrock=Entity(model='plane',collider='box',scale=100 , texture='grass',texture_scale=(4,4),position=(0,-3,0))
        self.blocks = {}
        self.noise = PerlinNoise(octaves=4, seed=-329329)

    def new_map(self):
        for x in range(60):
            for z in range(60):
                y = floor(self.noise([x/24, z/24])*6)
                block = Block(0,(x,y,z))


