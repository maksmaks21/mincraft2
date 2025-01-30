from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from models import *

app = Ursina()


sky=Sky(texture='sky_sunset')

map = Map()
map.new_map()

player=FirstPersonController()
app.run()