
from game_util import sprite_sheet as sprite
from game_util.pet_config import PetConfig as Config




class PetRaccoon():
    def __init__(self,input_pygame,screen) -> None:
        self.pet_id = "raccoon" # This is the pet id don't change this
        self.pet_name = "Rocket" # This is the pet name can change this
        self.animation_cooldown = Config.PET_ANIMATION_COOLDOWN
        self.FRAME = [5,8,8,4,8,8,8,8,8,3,7]
        self.ANIMATION_HEIGHT = [0,96,192,288,384,480,576,672,768,864,960]
        self.my_pygame = input_pygame
        self.last_update = self.my_pygame.time.get_ticks()
        self.raccoon_screen = screen
        self.raccoon_sprites =  self.my_pygame.image.load(Config.RACCOON_PATH).convert_alpha()
        self.raccoon_img = sprite.SpriteSheet(self.raccoon_sprites)
        self.run = True
        self.current_frame = 0
        self.pet_location = [0,0]
        # The current animation to play
        self.current_selected_animation = 9
        # The lists of frames for the current animation
        self.current_animation_list = []
        self.current_animation_list = self.get_animation_lists(self.current_selected_animation)
        self.is_play_once = False
        self.last_frame = self.current_animation_list[-1]

    def get_mask(self):
        return self.my_pygame.mask.from_surface(self.get_current_frame())

    def get_name(self):
        return self.pet_name
    
    def get_pet_id(self):
        return self.pet_id
        
    def set_location(self, x,y):
        self.pet_location = [x,y]

    def get_location(self):
        return self.pet_location

    def set_play_once(self, is_playing_once):
        self.is_play_once = is_playing_once

    def set_current_animation(self, animation_selected, is_playing_once = False):
        self.current_selected_animation = animation_selected
        self.get_animation_lists(self.current_selected_animation)
        self.current_frame = 0
        self.set_play_once(is_playing_once)


    def get_current_frame(self):
        return self.current_animation_list[self.current_frame]

       #FRAME[self.current_selected_animation] 
    def updated_frame(self):
        if self.is_play_once == True and self.current_animation_list[self.current_frame] == self.last_frame:
            return
        
        current_time = self.my_pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.last_update = current_time
            self.current_frame+=1
            if self.current_frame >= self.FRAME[self.current_selected_animation]:
                self.current_frame = 0 
                
    def did_overlap_with(self, item):
        if self.get_mask().overlap(item.get_mask(), (item.get_item_location()[0] - self.get_location()[0], item.get_item_location()[1] - self.get_location()[1])):
            return True
        return False
    
    def get_animation_lists(self,action)->list:
        self.current_animation_list = []
        for x in range(self.FRAME[action]):
            self.current_animation_list.append(self.raccoon_img.get_image(x,self.ANIMATION_HEIGHT[action] ,96, 96, 2, Config.BG_BLACK))
        self.last_frame = self.current_animation_list[-1]
        return self.current_animation_list

    def is_mouse_selection(self, mouse_pos):
        pet_location = self.get_location()
        pet_width = self.get_current_frame().get_width()
        pet_height = self.get_current_frame().get_height()
        if mouse_pos[0] >= pet_location[0] and mouse_pos[0] <= pet_location[0] + pet_width:
            if mouse_pos[1] >= pet_location[1] and mouse_pos[1] <= pet_location[1] + pet_height:
                return True
        return False



