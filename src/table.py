from game_util import sprite_sheet as sprite
from game_util.pet_config import PetConfig as Config

class Table:
    def __init__(self, my_pygame, screen, x, y):
        self.my_pygame = my_pygame
        self.screen = screen
        self.table_location = [x,y]
        self.table_img = self.my_pygame.image.load(Config.ITEM_PATH).convert_alpha()
        self.animation_lists = []
        self.FRAME = [11,11,1,1,1,1,6,6,1,1,1,1,1,1,1,1,1,1,1]
        self.ANIMATION_HEIGHT = [0,96]
        self.animation_cooldown = 100
        self.current_frame = 0
        self.last_update = self.my_pygame.time.get_ticks()
        self.table_sprites = sprite.SpriteSheet(self.table_img)
        self.current_selected_animation = 0
        self.table_animation_lists = self.get_animation_lists(self.current_selected_animation)
        self.table_broken_frame = self.table_animation_lists[-1]
        self.is_broken = False

    def get_mask(self):
        return self.my_pygame.mask.from_surface(self.get_current_frame())
    
    def set_location(self, x,y):
        self.table_location = [x,y]

    def get_location(self):
        return self.table_location
    
    def set_is_broken(self, is_table_broken):
        if is_table_broken == True:
            self.current_frame = self.table_broken_frame
        else:
            self.current_frame = 0
        self.is_broken = is_table_broken
    
    def set_current_selected_animation(self, animation):
        self.current_selected_animation = animation
        self.table_animation_lists = self.get_animation_lists(self.current_selected_animation)

    def get_current_frame(self):
        return self.table_animation_lists[self.current_frame]

    def update(self):
        if self.is_broken == True:
            return
        current_time = self.my_pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            if(self.table_animation_lists[self.current_frame] == self.table_broken_frame):
                self.is_broken = True
                print("Table is broken")
                return
            self.current_frame += 1
            self.last_update = current_time
            if self.current_frame >= len(self.table_animation_lists):
                self.is_broken = True
                print("Table is broken")
                self.current_frame = 4 #(len(self.table_animation_lists)//2) - 1
    
    def did_overlap_with(self, object):
        if self.get_mask().overlap(object.get_mask(), (object.get_location()[0] - self.get_location()[0], object.get_location()[1] - self.get_location()[1])):
            return True
        return False
    
    def get_animation_lists(self,action):
        for x in range(self.FRAME[action]):
            self.animation_lists.append(self.table_sprites.get_image(x,self.ANIMATION_HEIGHT[action] ,96, 96, 2, Config.BG_BLACK))


        return self.animation_lists
    
    