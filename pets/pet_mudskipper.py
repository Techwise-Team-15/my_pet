import pygame
from game_util import sprite_sheet as sprite
from game_util.pet_config import PetConfig as Config


class PetMudskipper():
    def __init__(self,input_pygame,screen) -> None:
        self.my_pygame = input_pygame
        self.mudskipper_screen = screen
        self.animation_lists = [] 
        self.animation_cooldown = 500
        self.FRAME = [8,12,10,4,9,12,10,11,9,10]
        self.ANIMATION_HEIGHT = [0,96,192,288,384,480,576,672,768,864]
        self.mudskipper_sprites =  self.my_pygame.image.load(Config.MUDSKIPPER_PATH).convert_alpha()
        self.mudskippers = sprite.SpriteSheet(self.mudskipper_sprites)
        self.run = True
        self.last_update = pygame.time.get_ticks()
    
    def get_animation_lists(self,action):
        for x in range(self.FRAME[action]):
            self.animation_lists.append(self.mudskippers.get_image(x,self.ANIMATION_HEIGHT[action] ,96, 96, 2, Config.BLACK))

        return self.animation_lists

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