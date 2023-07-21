import pygame
from game_util import PetConfig as Config
from pets import PetRaccoon, PetRock, PetMudskipper
from game_util import PetConfig as config
from pet_selection import PetSelection
from game_over import GameOver
from pygame.locals import *

pygame.init()

hp_drain_time = 100
RED = (255, 0, 0)
GREEN = (0, 255, 0)
INDIGO = (75, 0, 130)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
rock_house_background = '../my_pet/assets/rock_img/porch_for_rock.png'
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


class StatusBar:
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
            self.hp -= 20


class PetStats:
    health_bar = StatusBar(950, 50, 200, 40, 1000, GREEN, RED)
    thirst_bar = StatusBar(950, 100, 200, 40, 1000, BLUE, RED)
    hunger_bar = StatusBar(950, 150, 200, 40, 1000, ORANGE, RED)
    happiness_bar = StatusBar(950, 200, 200, 40, 1000, YELLOW, RED)

    def get_pet_health(self):
        return self.health_bar.hp
    

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


class SpriteSheet:
    def __init__(self, image_path):
        self.sheet = pygame.image.load(image_path).convert_alpha()
        self.image_path = image_path

    def get_image(self, frame, animation_height, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), (frame * width, animation_height, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
        return image


class Item:
    def __init__(self, pygame, screen, image, x, y):
        self.pygame = pygame
        self.screen = screen
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_dragging = False
        self.offset = (0, 0)

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_dragging = True
                self.offset = (
                    event.pos[0] - self.rect.x,
                    event.pos[1] - self.rect.y
                )
        elif event.type == MOUSEBUTTONUP:
            if self.is_dragging:
                self.is_dragging = False
        elif event.type == MOUSEMOTION:
            if self.is_dragging:
                self.rect.x = event.pos[0] - self.offset[0]
                self.rect.y = event.pos[1] - self.offset[1]


class RockHouse:
    def __init__(self):
        self.house = HouseScreen()
        self.pet_stats = PetStats()
        self.sprite_sheet = SpriteSheet('../my_pet/assets/items_sheet.png')

        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 100
        #pets_to_display = []

        self.my_rock = PetRock(pygame, screen)
        self.my_rock.set_location(600, 600)
        self.my_rock.set_current_animation(Config.RockActions.idle.value)

        self.brocolli = self.sprite_sheet.get_image(0,384,96,96,1,RED)
        self.broccli_item = Item(pygame, screen, self.brocolli, 475, 175)
        self.watering_can = self.sprite_sheet.get_image(0, 288, 96, 96, 2, RED)
        self.watering_can_item = Item(pygame, screen, self.watering_can, 150, 600)
        self.ball = self.sprite_sheet.get_image(2, 288, 96, 96, 2, RED)
        self.ball_item = Item(pygame,screen, self.ball, 300, 300)
        self.bed = self.sprite_sheet.get_image(0,480,96,96,3,RED)
        self.bed_item = Item(pygame,screen,self.ball,850,500)



        self.game_over = GameOver(pygame, screen, self.my_rock)

        self.pet_died = False
        self.running = True
        self.moving = False
        self.clock = pygame.time.Clock()

    def main_frames(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if self.pet_stats.get_pet_health() == 0 and not self.pet_died:
            print("pet died")
            self.my_rock.set_current_animation(Config.RockActions.dying.value)
            self.pet_died = True

        if not self.pet_died:
            self.house.draw()
            self.pet_stats.update()
            self.pet_stats.draw(screen)
            screen.blit(self.my_rock.get_current_frame(), self.my_rock.get_location())
            screen.blit(self.watering_can_item.image, self.watering_can_item.rect.topleft)
            screen.blit(self.brocolli, self.broccli_item.rect.topleft)
            screen.blit(self.ball, self.ball_item.rect.topleft)
            screen.blit(self.bed, self.bed_item.rect.topleft)
            self.my_rock.updated_frame()
            pygame.display.flip()
            self.clock.tick(60)
        else:
            self.game_over.main_frames()
        pygame.display.update()