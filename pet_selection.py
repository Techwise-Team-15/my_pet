import pygame
from game_util import PetConfig as Config
from pets import PetRaccoon, PetRock, PetMudskipper
from assets import Table


class PetSelection():
    def __init__(self,in_pygame,in_screen) -> None:
        self.pet_pygame = in_pygame
        self.screen = in_screen
        self.background = self.pet_pygame.image.load('../my_pet/load_game/background_exp.PNG')
        self.bg = self.pet_pygame.transform.scale(self.background, [Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT])
        self.pet_pygame.display.set_caption('Pet Selection')
        self.last_update = self.pet_pygame.time.get_ticks()
        self.animation_cooldown = 100
        self.pets_to_display = []

    def add_pet(self, pet):
        self.pets_to_display.append(pet)
    
    def initialize_pets(self):
        
        # Create the raccoon
        My_Raccoon = PetRaccoon(input_pygame=self.pet_pygame, screen=self.screen)
        My_Raccoon.set_current_animation(Config.RaccoonActions.idle.value)
        My_Raccoon.set_location(100, 400)
        self.add_pet(My_Raccoon)

        # Create the rock
        My_rock = PetRock(input_pygame=self.pet_pygame, screen=self.screen)
        My_rock.set_location(600, 600)
        My_rock.set_current_animation(Config.RockActions.jumping.value)
        self.add_pet(My_rock)

        # Create the mudskipper
        My_mudskipper = PetMudskipper(input_pygame=self.pet_pygame, screen=self.screen)
        My_mudskipper.set_current_animation(Config.MudskipperActions.idle.value)
        My_mudskipper.set_location(1100, 400)
        self.add_pet(My_mudskipper)
    
    def main_frames(self):
        self.screen.blit(self.bg, (0,0))
        for pet in self.pets_to_display:
            self.screen.blit(pet.get_current_frame(),pet.get_location())
            pet.updated_frame()
        self.pet_pygame.display.flip()