import pygame
from game_util import PetConfig as Config
from pets import PetRaccoon, PetRock, PetMudskipper
from game_util import PetConfig as config
from pet_selection import PetSelection
from src import Table

pygame.init()

hp_drain_time = 100
RED = (255, 0, 0)
GREEN = (0, 255, 0)
INDIGO = (75, 0, 130)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255,165,0)
BLACK = (0, 0, 0)
rock_house_background = '..my_pet/assets/rock_img/porch_for_rock.png'
screen_width = config.SCREEN_WIDTH
screen_height = config.SCREEN_HEIGHT
font = config.FONT
screen = pygame.display.set_mode((screen_width, screen_height))




class HouseScreen:
    def __init__(self):
        self.house_screen = screen
        

    def draw(self):
        self.house_screen.fill(BLACK)  
        screen_background = pygame.image.load('../my_pet/assets/rock_img/porch_for_rock.png')
        screen_background = pygame.transform.scale(screen_background, (screen_width, screen_height))
        self.house_screen.blit(screen_background, (0, 0))

class StatusBar():
    def __init__(self, x, y, w, h, max_hp, color, bg_color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp
        self.color = color
        self.bg_color = bg_color

    def draw(self, surface):
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, self.bg_color, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.w * ratio, self.h))

    def bar_drain(self):
        if self.hp > 0:
            pygame.time.delay(hp_drain_time)
            self.hp -= 1


class PetStats():
    health_bar = StatusBar(950, 50, 200, 40, 1000, GREEN, RED)
    thirst_bar = StatusBar(950, 100, 200, 40, 1000, BLUE, RED)
    hunger_bar = StatusBar(950, 150, 200, 40, 1000, ORANGE, RED)
    happiness_bar = StatusBar(950, 200, 200,40,1000, YELLOW, RED)

    def draw(self, surface):
        self.health_bar.draw(surface)
        self.thirst_bar.draw(surface)
        self.hunger_bar.draw(surface)
        self.happiness_bar.draw(surface)

    def update(self):
        self.thirst_bar.bar_drain()
        self.hunger_bar.bar_drain()
        self.happiness_bar.bar_drain()
        if self.health_bar.hp == 0 or self.thirst_bar.hp == 0:
            self.health_bar.bar_drain()
        elif self.health_bar.hp == 0 and self.thirst_bar.hp == 0:
            self.health_bar.bar_drain()

house = HouseScreen()
pet_stats = PetStats()

last_update = pygame.time.get_ticks()
animation_cooldown = 100
#pets_to_display = []

My_rock = PetRock(pygame, screen)
My_rock.set_location(600, 600)
My_rock.set_current_animation(Config.RockActions.jumping.value)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    house.draw()
    pet_stats.update()
    pet_stats.draw(screen)
    screen.blit(My_rock.get_current_frame(),My_rock.get_location())
    My_rock.updated_frame()

    pygame.display.flip()

pygame.quit()