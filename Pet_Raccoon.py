import pygame
import spritesheet


class Pet_Raccoon():
    HEIGHT = 96
    WIDTH = 96
    FRAME = [5,8,8,4,8,8,8,8,8,3]
    last_update = pygame.time.get_ticks()
    BLACK = (0, 0, 0)
    #my_pet\Sprites\racoonpet.png C:\Users\Ruth Ann\OneDrive\Desktop\pygame.raccons - Copy\my_pet\Sprites\racoonpet.png
    
    run = True
    animation_lists = [] 
    animation_steps = 8
    animation_cooldown = 500
    my_pygame = pygame
    raccoon_screen = my_pygame.display
    ANIMATION_HEIGHT = 192
   
    def __init__(self,input_pygame,screen) -> None:
        self.my_pygame = input_pygame
        self.raccoon_screen = screen
        raccoon_sprites =  self.my_pygame.image.load('../my_pet/Sprites/racoonpet.png').convert_alpha()
        raccoons = spritesheet.SpiteSheet(raccoon_sprites)
        for x in range(self.animation_steps):
            self.animation_lists.append(raccoons.get_image(x, 96, 96, 2, self.BLACK))
    
    def walking(self,screen_color = (0, 0, 0)):
        frame = 0 
        while self.run:
            self.raccoon_screen.fill(screen_color)  # Replace (0, 0, 0) with your desired background color
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

   