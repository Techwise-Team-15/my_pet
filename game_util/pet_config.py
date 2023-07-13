from enum import Enum
from game_util import os
class PetConfig:
    SCREEN_WIDTH = 1400
    SCREEN_HEIGHT = 800

    FPS = 60

    #theme items
    BACKGROUND1 = '../my_pet/theme_items/general_background1.PNG'
    BACKGROUND2 = '../my_pet/theme_items/general_background2.png'
    FONT = '../my_pet/theme_items/Starborn.ttf'

    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BG = (50, 50, 50)
    GRAY = (100, 100, 100)



    PET_ANIMATION_COOLDOWN = 100
    
    RACCOON_PATH = '../my_pet/sprites/racoonpet.png' if os.path.exists('../my_pet/sprites/racoonpet.png') else 'my_pet/sprites/racoonpet.png'
    ROCK_PATH = '../my_pet/sprites/rockpet.png' if os.path.exists('../my_pet/sprites/rockpet.png') else 'my_pet/sprites/rockpet.png'
    MUDSKIPPER_PATH = '../my_pet/sprites/petmudskipper.png' if os.path.exists('../my_pet/sprites/petmudskipper.png') else 'my_pet/sprites/petmudskipper.png'
    TABLE_PATH = '../my_pet/sprites/items.png' if os.path.exists('../my_pet/sprites/items.png') else 'my_pet/sprites/items.png' 

    # Sprites with background colors
    RACCOON_COLORED_PATH = '../my_pet/sprites/raccoon.png' if os.path.exists('../my_pet/sprites/raccoon.png') else 'my_pet/sprites/raccoon.png'
    ROCK_COLORED_PATH = '../my_pet/sprites/rock.png' if os.path.exists('../my_pet/sprites/rock.png') else 'my_pet/sprites/rock.png'
    MUDSKIPPER_COLORED_PATH = '../my_pet/sprites/mudskipper.png' if os.path.exists('../my_pet/sprites/mudskipper.png') else 'my_pet/sprites/mudskipper.png'
    class RaccoonActions(Enum):
        walking = 0 
        jumping = 1
        magic = 2
        fighting = 3
        dying = 4
        eating = 5
        dirty = 6
        clean = 7
        sleeping = 8
        idle = 9
            
    class RockActions(Enum):
        rolling = 0 
        fighting = 1
        dirty = 2
        clean = 3
        jumping = 4
        eating = 5
        dying = 6
        sleeping = 7
        playing = 8

    class MudskipperActions(Enum):
        walking = 0
        eating = 1
        fighting = 2
        idle = 3
        jumping = 4
        shooting = 5
        dirty = 6
        playing = 7
        bubble = 8
        clean = 9

    class TableActions(Enum):
        lamp = 0
        vase = 1
