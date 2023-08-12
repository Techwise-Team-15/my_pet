import pygame
from game_util import PetConfig as Config
from pets import PetRaccoon, PetRock, PetMudskipper



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
        self.font = pygame.font.Font(Config.FONT, 36)
        self.headline = "Click on the pet you want to play with today! 😊"
        
        self.pet_description = Config.PET_DESCRIPTIONS

        # Pets:
            # Create the raccoon
        self.My_Raccoon = PetRaccoon(input_pygame=self.pet_pygame, screen=self.screen)
        self.My_Raccoon.set_current_animation(Config.RaccoonActions.idle.value)
        self.My_Raccoon.set_location(Config.SCREEN_WIDTH/16, 400)
            # Create the rock
        self.My_rock = PetRock(input_pygame=self.pet_pygame, screen=self.screen)
        self.My_rock.set_current_animation(Config.RockActions.idle.value)
        self.My_rock.set_location(Config.SCREEN_WIDTH/2 - 30, Config.SCREEN_HEIGHT/2 - 150)
            # Create the mudskipper
        self.My_mudskipper = PetMudskipper(input_pygame=self.pet_pygame, screen=self.screen)
        self.My_mudskipper.set_current_animation(Config.MudskipperActions.idle.value)
        self.My_mudskipper.set_location(Config.SCREEN_WIDTH - 4*(Config.SCREEN_WIDTH/16), 400)

    def add_pet(self, pet):
        self.pets_to_display.append(pet)

    def pet_screen_header(self):
        text_surface = self.font.render(self.headline, True, (255, 255, 255)) 
        text_surface = self.pet_pygame.transform.scale(text_surface, [Config.SCREEN_WIDTH/1.1, Config.SCREEN_HEIGHT/10])
        text_rect = text_surface.get_rect()
        text_rect.center = (Config.SCREEN_WIDTH/2, Config.SCREEN_HEIGHT/10)
        self.screen.blit(text_surface, text_rect)

    def display_pet_names(self):
        y_offset = 10
        x_offset = -160
        prime_meridian = Config.SCREEN_WIDTH/2
        equator = Config.SCREEN_HEIGHT/2
        pet_locations = {
            0: (prime_meridian/2 + x_offset, 600 + y_offset),
            1: (prime_meridian + x_offset, equator + y_offset ),
            2: ((prime_meridian/2 + x_offset)+prime_meridian, 600+ y_offset)
        }
        for pets in range(len(self.pets_to_display)):
            text_surface = self.font.render(self.pets_to_display[pets].get_name(), True, (255, 255, 255))
            text_surface = self.pet_pygame.transform.scale(text_surface, [192, 96])
            text_rect = text_surface.get_rect()
            text_rect.center = pet_locations[pets] #(Config.SCREEN_WIDTH/2, Config.SCREEN_HEIGHT/10 + 50 + pets*100)
            self.screen.blit(text_surface, text_rect)

    def display_pet_descriptions(self):
        y_offset = 70
        x_offset = -20
        prime_meridian = Config.SCREEN_WIDTH/2
        equator = Config.SCREEN_HEIGHT/2
        desc_font = pygame.font.Font(None, 36)
        pet_locations = {
            0: [prime_meridian/2 + x_offset, 600 + y_offset],
            1: [prime_meridian + x_offset, equator + y_offset ],
            2: [(prime_meridian/2 + x_offset)+prime_meridian, 600 + y_offset]
        }
        for pets in range(len(self.pets_to_display)):
            for idx,desc in enumerate(Config.PET_DESCRIPTIONS[self.pets_to_display[pets].get_pet_id()]):
                text_surface = desc_font.render(desc, True, Config.BLACK)
                text_surface = self.pet_pygame.transform.scale(text_surface, [525, 30])
                text_rect = text_surface.get_rect()
                text_rect.center = [pet_locations[pets][0],pet_locations[pets][1] + (idx*25)] #(Config.SCREEN_WIDTH/2, Config.SCREEN_HEIGHT/10 + 50 + pets*100)
                self.screen.blit(text_surface, text_rect)
            


    def initialize_pets(self):
        # Add the raccoon
        self.add_pet(self.My_Raccoon)
        # Add the rock
        self.add_pet(self.My_rock)
        # Add the mudskipper
        self.add_pet(self.My_mudskipper)
    
    def main_frames(self):
        self.screen.blit(self.bg, (0,0))
        self.pet_screen_header()
        self.display_pet_names()
        self.display_pet_descriptions()
        for pet in self.pets_to_display:
            self.screen.blit(pet.get_current_frame(),pet.get_location())
            pet.updated_frame()
        
        self.pet_pygame.display.flip()
    
    

    def handle_events(self):
        for event in self.pet_pygame.event.get():
            if event.type == pygame.QUIT:
                self.pet_pygame.quit()
                return None
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for pet in self.pets_to_display:

                    if pet.is_mouse_selection(mouse_pos):
                        print("You selected the " + pet.get_name() + "!")
                        return pet
        return None
