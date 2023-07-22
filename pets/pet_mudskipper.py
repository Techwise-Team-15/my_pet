import pygame
from game_util import sprite_sheet as sprite
from game_util.pet_config import PetConfig as Config


class PetMudskipper():
    def __init__(self,input_pygame,screen) -> None:
        self.pet_id = "mudskipper" # This is the pet id don't change this
        self.pet_name = "Splash" # This is the pet name can change this
        self.my_pygame = input_pygame
        self.mudskipper_screen = screen
        self.animation_cooldown = Config.PET_ANIMATION_COOLDOWN
        self.FRAME = [8,12,10,4,9,12,10,11,9,10]
        self.ANIMATION_HEIGHT = [0,96,192,288,384,480,576,672,768,864]
        self.mudskipper_sprites =  self.my_pygame.image.load(Config.MUDSKIPPER_COLORED_PATH).convert_alpha()
        self.mudskippers = sprite.SpriteSheet(self.mudskipper_sprites)
        self.last_update = self.my_pygame.time.get_ticks()
        self.run = True
        self.current_frame = 0
        self.pet_location = [0,0]
        # The current animation to play
        self.current_selected_animation = 3
        # The lists of frames for the current animation
        self.current_animation_list = []
        self.current_animation_list = self.get_animation_lists(self.current_selected_animation)
        self.is_play_once = False
        self.last_frame = self.current_animation_list[-1]
    
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

    
    def get_animation_lists(self,action):
        self.current_animation_list = []
        for x in range(self.FRAME[action]):
            self.current_animation_list.append(self.mudskippers.get_image(x,self.ANIMATION_HEIGHT[action] ,96, 96, 2, Config.RED))
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
    