from enum import Enum
import os
class PetConfig:
    SCREEN_WIDTH = 1400
    SCREEN_HEIGHT = 800
    HP_DRAIN_TIME = 100

    FPS = 60

    #theme items
    BACKGROUND1 = '../my_pet/theme_items/general_background1.PNG'
    BACKGROUND2 = '../my_pet/theme_items/general_background2.png'
    FONT = '../my_pet/theme_items/Starborn.ttf'

    # Colors
    BLACK = (0, 0, 0)
    BG_BLACK =(0,0,5)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BG = (50, 50, 50)
    GRAY = (100, 100, 100)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)
    INDIGO = (75, 0, 130)



    PET_ANIMATION_COOLDOWN = 170 
    ROCK_HOUSE_BG_PATH = '../my_pet/assets/rock_img/porch_for_rock.png'
    RACCOON_PATH = '../my_pet/sprites/racoonpet.png' if os.path.exists('../my_pet/sprites/racoonpet.png') else 'my_pet/sprites/racoonpet.png'
    ROCK_SPRITES_PATH = '../my_pet/sprites/rock_sprites.png' if os.path.exists('../my_pet/sprites/rock_sprites.png') else 'my_pet/sprites/rock_sprites.png'
    MUDSKIPPER_PATH = '../my_pet/sprites/petmudskipper.png' if os.path.exists('../my_pet/sprites/petmudskipper.png') else 'my_pet/sprites/petmudskipper.png'

    # Item Paths
    HEART_PATH = '../my_pet/assets/heart.png' if os.path.exists('../my_pet/assets/heart.png') else 'my_pet/assets/heart.png'
    ITEM_PATH = '../my_pet/assets/items.png' if os.path.exists('../my_pet/assets/items.png') else 'my_pet/assets/items.png' 

    # Sprites with background colors
    RACCOON_COLORED_PATH = '../my_pet/sprites/raccoon.png' if os.path.exists('../my_pet/sprites/raccoon.png') else 'my_pet/sprites/raccoon.png'
    ROCK_COLORED_PATH = '../my_pet/sprites/rock.png' if os.path.exists('../my_pet/sprites/rock.png') else 'my_pet/sprites/rock.png'
    MUDSKIPPER_COLORED_PATH = '../my_pet/sprites/mudskipper.png' if os.path.exists('../my_pet/sprites/mudskipper.png') else 'my_pet/sprites/mudskipper.png'

    # Pet names and descriptions
    
    PET_DESCRIPTIONS = {    
        "raccoon":["Rocket, the adventurous and spirited raccoon, is ready for exciting journeys.",
                    "Care for Rocket's needs, play together, and watch their adventurous spirit soar."],
        "rock":["Pebble, the rockstar of resilience, adds a touch of glamour to your care routine.", 
                     "Create a rockin' environment, spend quality time, and witness Pebble's unwavering charm."],
        "mudskipper":["Splash, the energetic and aquatic marvel, brings a wave of joy to your care routine.", 
                    "Dive into adventures, create a vibrant habitat, and marvel at Splash's agile moves."]
    }
    
    # Pet actions
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
        jumping = 1
        dirty = 2
        clean = 3
        idle = 4
        eating = 5
        dying = 6
        sleeping = 7
        playing = 8
        very_dirty_rolling = 9
        very_dirty_jumping = 10
        very_dirty_dirty = 11
        dirty_idle = 12
        dirty_rolling = 13
        dirty_jumping = 14
        dirty_dirty = 15
        dirt_idle = 16
        dirt_rolling = 17
        dirt_jumping = 18
        dirt_dirt = 19
        very_dirty_bath = 20
        very_dirty_shower = 21
        dirty_bath = 22
        dirty_shower = 23
        dirt_bath = 24
        dirt_shower = 25
        drinking = 26

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

    # Table actions
    class TableActions(Enum):
        lamp = 0
        vase = 1
        sun_flower = 2
        watering_can = 3
        broccoli = 4
        plant = 5 
        spray_flower_pink = 6
        spray_tulip = 7
        water_bucket = 8
        full_cup = 9
        half_cup = 10
        plate = 11
        iris = 12
        ball = 13



    class ItemID(Enum):
        broccoli = "broccoli"
        bed = "bed"
        ball = "ball"
        watering_can = "watering_can"
        full_cup = "full_cup"

