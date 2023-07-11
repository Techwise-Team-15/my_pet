import pygame
from game_util import PetConfig as Config
from pets import PetRaccoon, PetRock, PetMudskipper
from assets import Table


class PetSelection():
    def __init__(self) -> None:
        self.pet_pygame = pygame
        self.pet_pygame.init()
        self.screen = self.pet_pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.background = self.pet_pygame.image.load('my_pet/load_game/background_exp.PNG')
        self.bg = self.pet_pygame.transform.scale(self.background, [Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT])
        self.pet_pygame.display.set_caption('SpriteSheets')
        self.last_update = self.pet_pygame.time.get_ticks()
        self.animation_cooldown = 100
        self.run = True


    
    def create_pet_screen(self, action):
        # Create the raccoon
        My_Raccoon = PetRaccoon(input_pygame= self.pet_pygame, screen=self.screen)
        My_Raccoon.set_current_animation(action)
        My_Raccoon.set_location(100,400)
        #raccoon_animation_list = My_Raccoon.get_animation_lists(action)
        # Create the rock
        My_rock = PetRock(input_pygame= self.pet_pygame, screen=self.screen)
        My_rock.set_location(600,600)
        My_rock.set_current_animation(action)
        #rock_animation_list = My_rock.get_animation_lists(action)
        # Create the mudskipper
        My_mudskipper = PetMudskipper(input_pygame= self.pet_pygame, screen=self.screen)
        My_mudskipper.set_current_animation(action)
        My_mudskipper.set_location(1100,400)
        
        #my_table = Table(my_pygame=self.pet_pygame, screen=self.screen, x=800, y=200)
        #my_table.set_current_selected_animation(Config.TableActions.lamp.value) # lamp and vase are the only two options

        
        while self.run:
            #self.screen.fill(Config.BLACK)  # Replace (0, 0, 0) with your desired background color
            self.screen.blit(self.bg, (0,0))
            # Animation of the pets on the screen
            #self.screen.blit(rock_animation_list[frame], (0, 150))
            #character_surface = self.pet_pygame.Surface((, character_image.get_height()), pygame.SRCALPHA)
            self.screen.blit(My_rock.get_current_frame(),My_rock.get_location())
            My_rock.updated_frame()
            self.screen.blit(My_Raccoon.get_current_frame(), My_Raccoon.get_location())
            My_Raccoon.updated_frame()
            self.screen.blit(My_mudskipper.get_current_frame(), My_mudskipper.get_location())
            My_mudskipper.updated_frame()
            #self.screen.blit(my_table.get_current_frame(), my_table.get_location())
            #my_table.update()
            
            #self.screen.blit(raccoon_animation_list[frame], (350, 150))
            #self.screen.blit(mudskipper_animation_list[frame], (350, 350))
            self.pet_pygame.display.flip()
            for event in self.pet_pygame.event.get():
                if event.type == self.pet_pygame.QUIT:
                    self.run = False
            self.pet_pygame.display.update()
        self.pet_pygame.quit()


my_pet_screen = PetSelection()
my_pet_screen.create_pet_screen(Config.RaccoonActions.walking.value)

#My_Raccoon = Pet_Raccoon(input_pygame= pygame, screen=screen)
#My_Raccoon.animation(action=Config.RaccoonActions.clean.value)

#My_Rock = Pet_Rock(input_pygame= pygame, screen=screen)
#My_Rock.animation(action=Config.RockActions.clean.value)

#My_Mudskipper = Pet_Mudskipper(input_pygame= pygame, screen=screen)
#My_Mudskipper.animation(action=Config.MudskipperActions.walking.value)