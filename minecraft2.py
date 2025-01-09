from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

sky=Sky(texture='sky_sunset')
ground=Entity(model='plane',scale=100 , texture='grass',texture_scale=(4,4),position=(0,-3,0))
player=FirstPersonController()

block = Entity(model='cube', texture='grass', position=(2,0,0))

app.run()