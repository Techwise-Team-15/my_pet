import pygame
import spritesheet
from enum import Enum
import Config


class Pet_Rock():
    def __init__(self,input_pygame,screen) -> None:
        self.animation_lists = [] 
        self.animation_steps = 8
        self.animation_cooldown = 500
        self.FRAME = [8,8,2,8,6,8,8,7,8]
        self.ANIMATION_HEIGHT = [0,96,192,288,384,480,576,672,768]
        self.last_update = pygame.time.get_ticks()
        self.my_pygame = input_pygame
        self.rock_screen = screen
        self.rock_sprites =  self.my_pygame.image.load(Config.ROCK_PATH).convert_alpha()
        self.rocks = spritesheet.SpiteSheet(self.rock_sprites)
        self.run = True
    
    def animation(self,action):
        for x in range(self.FRAME[action]):
            self.animation_lists.append(self.rocks.get_image(x,self.ANIMATION_HEIGHT[action] ,96, 96, 2, Config.BLACK))
        frame = 0 
        while self.run:
            self.rock_screen.fill(Config.BLACK)  # Replace (0, 0, 0) with your desired background color
            current_time = self.my_pygame.time.get_ticks()
            if current_time - self.last_update >= self.animation_cooldown:
                frame += 1
                self.last_update = current_time
                if frame >= len(self.animation_lists):
                    frame = 0

            self.rock_screen.blit(self.animation_lists[frame], (350, 150))

            for event in self.my_pygame.event.get():
                if event.type == self.my_pygame.QUIT:
                    self.run = False

            self.my_pygame.display.update()

        self.my_pygame.quit()