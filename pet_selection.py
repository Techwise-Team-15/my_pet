import pygame
from game_util import PetConfig as Config
from pets import PetRaccoon, PetRock, PetMudskipper
from assets import Table


class PetSelection():
    def __init__(self) -> None:
        self.pet_pygame = pygame
        self.pet_pygame.init()
        self.screen = self.pet_pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.pet_pygame.display.set_caption('SpriteSheets')
        self.last_update = self.pet_pygame.time.get_ticks()
        self.animation_cooldown = 100
        self.run = True


    
    def create_pet_screen(self, action):
        # Create the raccoon
        My_Raccoon = PetRaccoon(input_pygame= self.pet_pygame, screen=self.screen)
        My_Raccoon.set_current_animation(action)
        My_Raccoon.set_location(300,200)
        #raccoon_animation_list = My_Raccoon.get_animation_lists(action)
        # Create the rock
        My_rock = PetRock(input_pygame= self.pet_pygame, screen=self.screen)
        My_rock.set_location(100,200)
        My_rock.set_current_animation(action)
        #rock_animation_list = My_rock.get_animation_lists(action)
        # Create the mudskipper
        My_mudskipper = PetMudskipper(input_pygame= self.pet_pygame, screen=self.screen)
        My_mudskipper.set_current_animation(action)
        My_mudskipper.set_location(600,200)
        
        my_table = Table(my_pygame=self.pet_pygame, screen=self.screen, x=800, y=200)
        my_table.set_current_selected_animation(Config.TableActions.lamp.value) # lamp and vase are the only two options

        
        while self.run:
            self.screen.fill(Config.BLACK)  # Replace (0, 0, 0) with your desired background color

            # Animation of the pets on the screen
            #self.screen.blit(rock_animation_list[frame], (0, 150))
            self.screen.blit(My_rock.get_current_frame(), My_rock.get_location())
            My_rock.updated_frame()
            self.screen.blit(My_Raccoon.get_current_frame(), My_Raccoon.get_location())
            My_Raccoon.updated_frame()
            self.screen.blit(My_mudskipper.get_current_frame(), My_mudskipper.get_location())
            My_mudskipper.updated_frame()
            self.screen.blit(my_table.get_current_frame(), my_table.get_location())
            #my_table.update()
            
            #self.screen.blit(raccoon_animation_list[frame], (350, 150))
            #self.screen.blit(mudskipper_animation_list[frame], (350, 350))

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


"""
sprite_sheet_images = [
    pygame.image.load('../Sprites/racoonpet.png').convert_alpha(),
    pygame.image.load('../Sprites/rockpet.png').convert_alpha(),
    pygame.image.load('../Sprites/petmudskipper.png').convert_alpha()
]

sprite_sheets = [
    spritesheet.SpiteSheet(sprite_sheet_images[0]),
    spritesheet.SpiteSheet(sprite_sheet_images[1]),
    spritesheet.SpiteSheet(sprite_sheet_images[2])
]

animation_lists = [[] for _ in range(3)] 
animation_steps = 3
animation_cooldown = 100


for sheet_index, sprite_sheet in enumerate(sprite_sheets):
    for x in range(animation_steps):
        for _ in range(animation_steps):
            animation_lists[sheet_index].append(sprite_sheet.get_image(x, 96, 96, 2, BLACK))


frames = [0, 0, 0]
last_update = [pygame.time.get_ticks() for _ in range(3)]

run = True
while run:
    screen.fill(BG)

    current_time = pygame.time.get_ticks()


    for sheet_index in range(3):
        if current_time - last_update[sheet_index] >= animation_cooldown:
            frames[sheet_index] += 1
            last_update[sheet_index] = current_time
            if frames[sheet_index] >= len(animation_lists[sheet_index]):
                frames[sheet_index] = 0

        screen.blit(animation_lists[sheet_index][frames[sheet_index]], (100 + sheet_index * 250, 150))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()import pygame
from game_util import PetConfig as Config
from pets import PetRaccoon, PetRock, PetMudskipper


class PetSelection():
    def __init__(self) -> None:
        self.pet_pygame = pygame
        self.pet_pygame.init()
        self.screen = self.pet_pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.pet_pygame.display.set_caption('SpriteSheets')
        self.last_update = self.pet_pygame.time.get_ticks()
        self.animation_cooldown = 100
        self.run = True

    
    def create_pet_screen(self, action):
        # Create the raccoon
        My_Raccoon = PetRaccoon(input_pygame= self.pet_pygame, screen=self.screen)
        raccoon_animation_list = My_Raccoon.get_animation_lists(action)
        # Create the rock
        My_rock = PetRock(input_pygame= self.pet_pygame, screen=self.screen)
        My_rock.set_current_animation(action)
        #rock_animation_list = My_rock.get_animation_lists(action)
        # Create the mudskipper
        My_muudskipper = PetMudskipper(input_pygame= self.pet_pygame, screen=self.screen)
        mudskipper_animation_list = My_muudskipper.get_animation_lists(action)
        
        
        while self.run:
            self.screen.fill(Config.BLACK)  # Replace (0, 0, 0) with your desired background color

            # Animation of the pets on the screen
            #self.screen.blit(rock_animation_list[frame], (0, 150))
            self.screen.blit(My_rock.get_current_frame(), My_rock.get_location())
            My_rock.updated_frame()
            #self.screen.blit(raccoon_animation_list[frame], (350, 150))
            #self.screen.blit(mudskipper_animation_list[frame], (350, 350))

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


"""