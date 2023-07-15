import pygame
from game_util import sprite_sheet as sprite
from game_util.pet_config import PetConfig as Config


class PetMudskipper():
    def __init__(self,input_pygame,screen) -> None:
        self.pet_id = "mudskipper"
        self.my_pygame = input_pygame
        self.mudskipper_screen = screen
        self.animation_lists = [] 
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
        self.current_animation_list = self.get_animation_lists(self.current_selected_animation)
        self.pet_name = "Splash"
    
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
        for x in range(self.FRAME[action]):
            self.animation_lists.append(self.mudskippers.get_image(x,self.ANIMATION_HEIGHT[action] ,96, 96, 2, Config.RED))

        return self.animation_lists

    def is_mouse_selection(self, mouse_pos):
        pet_location = self.get_location()
        pet_width = self.get_current_frame().get_width()
        pet_height = self.get_current_frame().get_height()
        if mouse_pos[0] >= pet_location[0] and mouse_pos[0] <= pet_location[0] + pet_width:
            if mouse_pos[1] >= pet_location[1] and mouse_pos[1] <= pet_location[1] + pet_height:
                return True
        return False
    
    def animation(self):
        frame = 0 
        while self.run:
            self.mudskipper_screen.fill(Config.BLACK)  # Replace (0, 0, 0) with your desired background color
            current_time = self.my_pygame.time.get_ticks()
            if current_time - self.last_update >= self.animation_cooldown:
                frame += 1
                self.last_update = current_time
                if frame >= len(self.animation_lists):
                    frame = 0

            self.mudskipper_screen.blit(self.animation_lists[frame], (350, 150))

            for event in self.my_pygame.event.get():
                if event.type == self.my_pygame.QUIT:
                    self.run = False

            self.my_pygame.display.update()

        self.my_pygame.quit()