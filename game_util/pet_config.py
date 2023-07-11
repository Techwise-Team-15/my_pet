from enum import Enum

class PetConfig:
    SCREEN_WIDTH = 1400
    SCREEN_HEIGHT = 800
    FPS = 60

    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BG = (50, 50, 50)


    PET_ANIMATION_COOLDOWN = 100
    
    RACCOON_PATH = '../my_pet/sprites/racoonpet.png'
    ROCK_PATH = '../my_pet/sprites/rockpet.png'
    MUDSKIPPER_PATH = '../my_pet/sprites/petmudskipper.png'
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
