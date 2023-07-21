
from game_util import sprite_sheet as sprite
from game_util.pet_config import PetConfig as Config


class PetRock():
    def __init__(self,input_pygame,screen) -> None:
        self.pet_id = "rock"
        self.animation_cooldown = Config.PET_ANIMATION_COOLDOWN
        self.FRAME = [8,8,2,8,6,8,8,7,8]
        self.ANIMATION_HEIGHT = [0,96,192,288,384,480,576,672,768]
        self.my_pygame = input_pygame
        self.last_update = self.my_pygame.time.get_ticks()
        self.rock_screen = screen
        self.rock_sprites =  self.my_pygame.image.load(Config.ROCK_COLORED_PATH).convert_alpha()
        self.rocks = sprite.SpriteSheet(self.rock_sprites)
        self.run = True
        self.current_frame = 0
        self.pet_location = [0,0]
        # The current animation to play
        self.current_selected_animation = Config.RockActions.idle.value
        # The lists of frames for the current animation
        self.current_animation_list = []
        self.current_animation_list = self.get_animation_lists(self.current_selected_animation)
        self.pet_name = "Pebble"
        
    def get_name(self):
        return self.pet_name

    def get_pet_id(self):
        return self.pet_id
    
    def set_location(self, x,y):
        self.pet_location = [x,y]
    
    def get_location(self):
        return self.pet_location

    def set_current_animation(self, animation_selected):
        self.current_selected_animation = animation_selected
        self.get_animation_lists(self.current_selected_animation)


    def get_current_frame(self):
        return self.current_animation_list[self.current_frame]

       #FRAME[self.current_selected_animation] 
    def updated_frame(self):
        current_time = self.my_pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.last_update = current_time
            self.current_frame+=1
            if self.current_frame >= self.FRAME[self.current_selected_animation]:
                self.current_frame = 0 

    def get_animation_lists(self,action):
        self.current_animation_list = []
        for x in range(self.FRAME[action]):
            self.current_animation_list.append(self.rocks.get_image(x,self.ANIMATION_HEIGHT[action] ,96, 96, 2, Config.RED))

        return self.current_animation_list
    
    def is_mouse_selection(self, mouse_pos):
        pet_location = self.get_location()
        pet_width = self.get_current_frame().get_width()
        pet_height = self.get_current_frame().get_height()
        if mouse_pos[0] >= pet_location[0] and mouse_pos[0] <= (pet_location[0] + pet_width):
            if mouse_pos[1] >= pet_location[1] and mouse_pos[1] <= (pet_location[1] + pet_height):
                return True
        return False
    