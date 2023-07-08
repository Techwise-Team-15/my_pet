import pygame
import spritesheet
from enum import Enum
import Config



class Pet_Raccoon():
    def __init__(self,input_pygame,screen) -> None:
        self.run = True
        self.animation_lists = []
        self.animation_cooldown = 500

        
        self.FRAME = [5,8,8,4,8,8,8,8,8,3]
        self.ANIMATION_HEIGHT = [0,96,192,288,384,480,576,672,768,864]
        self.last_update = pygame.time.get_ticks()
        self.my_pygame = input_pygame
        self.raccoon_screen = screen
        self.raccoon_sprites =  self.my_pygame.image.load(Config.RACCOON_PATH).convert_alpha()
        self.raccoons = spritesheet.SpiteSheet(self.raccoon_sprites)
        
    def get_animation_lists(self,action)->list:
        for x in range(self.FRAME[action]):
            self.animation_lists.append(self.raccoons.get_image(x,self.ANIMATION_HEIGHT[action] ,96, 96, 2, Config.BLACK))
        print(len(self.animation_lists))
        return self.animation_lists
    
    def animation(self):
      
        frame = 0 
        while self.run:
            self.raccoon_screen.fill(Config.BLACK)  # Replace (0, 0, 0) with your desired background color
            current_time = self.my_pygame.time.get_ticks()
            if current_time - self.last_update >= self.animation_cooldown:
                frame += 1
                self.last_update = current_time
                if frame >= len(self.animation_lists):
                    frame = 0

            self.raccoon_screen.blit(self.animation_lists[frame], (350, 150))

            for event in self.my_pygame.event.get():
                if event.type == self.my_pygame.QUIT:
                    self.run = False

            self.my_pygame.display.update()

        self.my_pygame.quit()

