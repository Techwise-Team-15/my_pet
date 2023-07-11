from game_util import sprite_sheet as sprite
from game_util.pet_config import PetConfig as Config

class Table:
    def __init__(self, my_pygame, screen, x, y):
        self.my_pygame = my_pygame
        self.screen = screen
        self.table_location = [x,y]
        self.table_img = self.my_pygame.image.load(Config.TABLE_PATH).convert_alpha()
        self.animation_lists = []
        self.FRAME = [11,11]
        self.ANIMATION_HEIGHT = [0,96]
        self.animation_cooldown = 100
        self.current_frame = 0
        self.last_update = self.my_pygame.time.get_ticks()
        self.table_sprites = sprite.SpriteSheet(self.table_img)
        self.current_selected_animation = 0
        self.table_animation_lists = self.get_animation_lists(self.current_selected_animation)

    def set_location(self, x,y):
        self.table_location = [x,y]

    def get_location(self):
        return self.table_location
    
    def set_current_selected_animation(self, animation):
        self.current_selected_animation = animation
        self.table_animation_lists = self.get_animation_lists(self.current_selected_animation)

    def get_current_frame(self):
        return self.table_animation_lists[self.current_frame]

    def update(self):
        current_time = self.my_pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.current_frame += 1
            self.last_update = current_time
            if self.current_frame >= len(self.table_animation_lists):
                self.current_frame = 0

    def get_animation_lists(self,action):
        for x in range(self.FRAME[action]):
            self.animation_lists.append(self.table_sprites.get_image(x,self.ANIMATION_HEIGHT[action] ,96, 96, 2, Config.BLACK))

        return self.animation_lists
    
    