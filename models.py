from ursina import*


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
            **kwaegs
        )


