from enum import Enum

# Game Window Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BG = (50, 50, 50)

class action(Enum):
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