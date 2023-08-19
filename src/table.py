from game_util import sprite_sheet as sprite
from game_util.pet_config import PetConfig as Config

class Table:
    def __init__(self, my_pygame, screen, x, y):
        self.my_pygame = my_pygame
        self.screen = screen
        self.table_location = [x,y]
        self.table_img = self.my_pygame.image.load(Config.ITEM_PATH).convert_alpha()
       
        #Frame and Animation Height have to be the same
        # These are the animations with 2 frames per frame
        self.double_frame_actions = [Config.TableActions.spray_flower_pink.value, Config.TableActions.spray_tulip.value]
        self.FRAME = [11,11,1,1,1,1,6,6,1,1,1,1,1,1,1,1,1,1,1,1,1,1,11]
        self.ANIMATION_HEIGHT = [0,96,192,288,384,480,576,672,768,864,960,1056,1152,1248,1344,1440,1536,1632,1728,1824,1920,2016,2112,2208]
        self.animation_cooldown = 100
        self.current_frame = 0
        self.last_update = self.my_pygame.time.get_ticks()
        self.table_sprites = sprite.SpriteSheet(self.table_img)
        self.current_selected_animation = 0
        self.animation_lists = self.get_animation_lists(self.current_selected_animation)
        self.table_broken_frame = self.animation_lists[-1]
        self.is_broken = False
        self.is_play_once = False

    def set_play_once(self, is_playing_once):
        self.is_play_once = is_playing_once

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
    
    def set_current_selected_animation(self, animation,is_playing_once=False):
        self.current_selected_animation = animation
        self.get_animation_lists(self.current_selected_animation)
        self.current_frame = 0
        self.set_play_once(is_playing_once)

    def get_current_frame(self):
        return self.animation_lists[self.current_frame]

    def update(self):
        if self.is_broken == True or self.is_play_once:
            return
        current_time = self.my_pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            if(self.animation_lists[self.current_frame] == self.table_broken_frame):
                self.is_broken = True
                return
            self.current_frame += 1
            self.last_update = current_time
            if self.current_frame >= len(self.animation_lists):
                self.is_broken = True
               
                self.current_frame = len(self.animation_lists) -1
    
    def did_overlap_with(self, object):
        if self.get_mask().overlap(object.get_mask(), (object.get_location()[0] - self.get_location()[0], object.get_location()[1] - self.get_location()[1])):
            return True
        return False
    
    def get_animation_lists(self,action):
        self.animation_lists = []
        for x in range(self.FRAME[action]):
            #self.animation_lists.append(self.table_sprites.get_image(x,self.ANIMATION_HEIGHT[action] ,96, 96, 2, Config.BG_BLACK))
            if action in self.double_frame_actions:
                self.animation_lists.append(self.table_sprites.get_image(x,self.ANIMATION_HEIGHT[action], 192, 96,2,Config.BG_BLACK))
            else:
                self.animation_lists.append(self.table_sprites.get_image(x,self.ANIMATION_HEIGHT[action], 96, 96, 2, Config.BG_BLACK))
        self.last_frame = self.animation_lists[-1]

        return self.animation_lists
    
    def is_mouse_selection(self, mouse_pos):
        pet_location = self.get_location()
        pet_width = self.get_current_frame().get_width()
        pet_height = self.get_current_frame().get_height()
        if mouse_pos[0] >= pet_location[0] and mouse_pos[0] <= (pet_location[0] + pet_width):
            if mouse_pos[1] >= pet_location[1] and mouse_pos[1] <= (pet_location[1] + pet_height):
                return True
        return False
    
    def has_animation_ended(self):
        if self.current_frame == self.FRAME[self.current_selected_animation] - 1:
            return True
        return False
    