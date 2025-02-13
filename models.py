from ursina import*
from perlin_noise import PerlinNoise
from ursina.prefabs.first_person_controller import FirstPersonController

from ursina.shaders import basic_lighting_shader
from numpy import floor
import os 
import random
import pickle

block_textures = []
BASE_DIR = os.getcwd()
BLOCKS_DIR = os.path.join(BASE_DIR, 'assets/blocks')

file_list =  os.listdir(BLOCKS_DIR)
for image in file_list:
    texture = load_texture('assets/blocks' + os.sep + image)
    block_textures.append(texture)

class Tree (Button): 
    def __init__(self, pos, **kwargs): 
        super().__init__( 
            parent=scene, #батький об'єкт сцена гри 
            model='assets/minecrafttree/scene.gltf', #модель куба 
            position=pos, #координати блока 
            scale=5, #pозмір 
            collider='box', #колайдер для зіткнень з гравцем 
            origin_y=0.5, #рівень землі 
            color=color.color(0,0, random.uniform(0.9, 1)), 
            shader=basic_lighting_shader, 
            **kwargs
        )
        scene.trees[(self.x,self.y,self.z)] = self

class Flover (Button): 
    def __init__(self, pos, **kwargs): 
        super().__init__( 
            parent=scene, #батький об'єкт сцена гри 
            model='assets/flover/scene.gltf', #модель куба 
            position=pos, #координати блока 
            scale=1, #pозмір 
            origin_y=0, #рівень землі 
            color=color.color(0,0, random.uniform(0.9, 1)), 
            shader=basic_lighting_shader, 
            **kwargs
        )
        scene.flovers[(self.x,self.y,self.z)] = self

class Torch (Button): 
    def __init__(self, pos, **kwargs): 
        super().__init__( 
            parent=scene, #батький об'єкт сцена гри 
            model='/assets/minecrafttorch/scene.gltf', #модель куба 
            position=pos, #координати блока 
            scale=1, #pозмір 
            origin_y=0, #рівень землі 
            color=color.color(0,0, random.uniform(0.9, 1)), 
            shader=basic_lighting_shader, 
            **kwargs
        )
        scene.torchs[(self.x,self.y,self.z)] = self

class Block(Button):
    current=0
    def __init__(self, block_type, pos,**kwargs):
        super().__init__(
            parent=scene,
            model='cube',
            texture=block_textures[block_type],
            position=pos,
            scale=1,
            collider='box',
            origin_y=-0.5,
            color=color.color(0,0,random.uniform(0.9,1)),
            shader= basic_lighting_shader,
            **kwargs,
        )
        self.id = block_type
        scene.blocks[(self.x,self.y,self.z)] = self

class Map(Entity):
    def __init__(self, **kwargs):
        super().__init__(model=None, collider=None, **kwargs)
        bedrock=Entity(model='plane',collider='box',scale=100 , texture='grass',texture_scale=(4,4),position=(0,-3,0))
        scene.blocks = {}
        scene.trees = {}
        scene.flovers = {}
        scene.torchs = {}
        self.noise = PerlinNoise(octaves=4, seed=-329329)
        self.player=Player()

    def new_map(self, size=30):
        for x in range(size):
            for z in range(size):
                y = floor(self.noise([x/24, z/24])*6)
                block = Block(0,(x,y,z))
                rand_num=random.randint(1, 100)
                if rand_num == 71:
                    Tree((x,y+1,z))

                rand_num=random.randint(1, 50)
                if rand_num == 25:
                    Flover((x,y+1,z))

                rand_num=random.randint(1, 50)
                if rand_num == 25:
                    Torch((x,y+1,z))

    def save(self):
        game_data= {
            "player_pos": (self.player.x, self.player.y, self.player.z),
            "blocks":[],
            "trees":[],
            "flovers":[],
            "torchs":[]
        }

        for block_pos, block, in scene.blocks.items():
            game_data['blocks'].append((block_pos,block.id))
        for tree_pos, tree in scene.trees.items():
            game_data["trees"].append(tree_pos)
        for flover_pos, flover in scene.flovers.items():
            game_data["flovers"].append(flover_pos)
        for torch_pos, torch in scene.torchs.items():
            game_data["torchs"].append(torch_pos)

        with open("seve.dat", 'wb') as f:
            pickle.dump(game_data, f)

    def load(self):
        with open("seve.dat", 'rb') as f :
            game_data = pickle.load(f)
            for block_pos, block_id in game_data["blocks"]:
                Block(block_id, block_pos)
            for tree_pos in game_data["trees"]:
                Tree(tree_pos)
            for flover_pos in game_data["flovers"]:
                Flover(flover_pos)
            self.player.position = game_data["player_pos"]

    def input(self,key):
        if key == 'g':
            self.save()
            



class Player(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.build_sount = Audio(sound_file_name='assets/audio/wood-effect-254997.mp3',
                                 autoplay=False,volume=0.5)

        self.destroi_sount = Audio(sound_file_name='assets/audio/stone-effect-254998.mp3',
                                 autoplay=False,volume=0.5)

        self.hand_block = Entity(parent=camera.ui,model='cube',
                                texture=block_textures[Block.current],scale=0.2, position=(0.6, -0.42),
                                shader=basic_lighting_shader, rotation=Vec3(30,-30,10))

    def input(self, key):
        super().input(key)

        if key =='scroll up':
            Block.current +=1
            if Block.current >=len(block_textures):
                Block.current = 0
            self.hand_block.texture=block_textures[Block.current]

        if key =='scroll down':
            Block.current -=1
            if Block.current <0:
                Block.current =len(block_textures)-1
            self.hand_block.texture=block_textures[Block.current]


        if key == 'left mouse down' and mouse.hovered_entity:
            destroy(mouse.hovered_entity)
            self.destroi_sount.play()

        if key == 'right mouse down' and mouse.hovered_entity:
            hit_info = raycast(camera.world_position, camera.forward, distance=5)
            if hit_info.hit:
                Block(Block.current, hit_info.entity.position + hit_info.normal)
                self.build_sount.play()

    def update(self):
        super().update()
        if held_keys['control']:
            self.speed = 10
        else: self.speed = 5

        if held_keys['shift']:
            self.speed = 3
            self.height = 1
        else: 
            self.speed=5
            self.height = 2
            



    