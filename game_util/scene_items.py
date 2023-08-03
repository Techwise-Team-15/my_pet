import pygame, pygame.freetype
from .sprite_sheet import SpriteSheet as SpriteSheet
from .pet_config import PetConfig as config

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
            pygame.time.delay(config.HP_DRAIN_TIME)
            self.hp -= 20 
    
    def bar_fill(self):
        self.hp = self.max_hp

class BarIcons:
    def __init__(self,pygame, screen) -> None:
        self.pygame = pygame
        self.screen = screen
        self.heart_img = pygame.image.load(config.HEART_PATH).convert_alpha()
        self.heart_img = pygame.transform.scale(self.heart_img, (40, 40))
        self.sprite_sheet = SpriteSheet(pygame.image.load(config.ITEM_PATH).convert_alpha())
        self.broccoli = self.sprite_sheet.get_image(0,384,96,96,.75,config.BG_BLACK)
        self.full_cup = self.sprite_sheet.get_image(0,864,96,96,.75,config.BG_BLACK)
        self.ball = self.sprite_sheet.get_image(0, 1248, 96, 96, .75, config.BG_BLACK)

    def draw(self):
        self.screen.blit(self.heart_img, (config.SCREEN_WIDTH - 240, 45))
        self.screen.blit(self.full_cup, (config.SCREEN_WIDTH - 260, 80))
        self.screen.blit(self.broccoli, (config.SCREEN_WIDTH - 250, 130))
        self.screen.blit(self.ball, (config.SCREEN_WIDTH - 250, 180))
        

class PetStats:
    health_bar = StatusBar(950, 50, 200, 40, 1000, config.GREEN, config.RED)
    thirst_bar = StatusBar(950, 100, 200, 40, 1000, config.BLUE, config.RED)
    hunger_bar = StatusBar(950, 150, 200, 40, 1000, config.ORANGE, config.RED)
    happiness_bar = StatusBar(950, 200, 200, 40, 1000, config.YELLOW, config.RED)

    def get_pet_health(self):
        return self.health_bar.hp
    
    def get_pet_thirst(self):
        return self.thirst_bar.hp
    
    def get_pet_hunger(self):
        return self.hunger_bar.hp
    
    def get_pet_happieness(self):
        return self.happiness_bar.hp
    
    def fill_health(self):
        self.health_bar.bar_fill()
    
    def fill_thirst(self):
        self.thirst_bar.bar_fill()

    def fill_hunger(self):
        self.hunger_bar.bar_fill()
    
    def fill_happiness(self):
        self.happiness_bar.bar_fill()

    def draw(self, surface):
        self.health_bar.draw(surface)
        self.thirst_bar.draw(surface)
        self.hunger_bar.draw(surface)
        self.happiness_bar.draw(surface)

    def update(self):
        self.thirst_bar.bar_drain()
        self.hunger_bar.bar_drain()
        self.happiness_bar.bar_drain()
        if self.hunger_bar.hp == 0 and self.thirst_bar.hp == 0:
            self.health_bar.bar_drain()

class Item:
    def __init__(self, item_id, pygame, screen, image, pet, x, y, is_movable = True):
        self.pygame = pygame
        self.screen = screen
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_dragging = False
        self.is_movable = is_movable
        self.item_id = item_id
        self.interacting_pet = pet
        self.item_location = [x,y]
        self.offset = (0, 0)

    def is_mouse_selection(self, mouse_pos):
        item_location = self.item_location
        item_width = self.rect.width
        item_height = self.rect.height 
        if mouse_pos[0] >= item_location[0] and mouse_pos[0] <= (item_location[0] + item_width):
            if mouse_pos[1] >= item_location[1] and mouse_pos[1] <= (item_location[1] + item_height):
                return True
        return False
    
    def get_collision_item(self):
        if self.item_id == config.ItemID.ball and self.rect.collidepoint(self.interacting_pet.get_location()):
            self.interacting_pet.set_current_animation(config.RockActions.playing.value, True)
            return config.ItemID.ball
        elif self.item_id == config.ItemID.broccoli and self.rect.collidepoint(self.interacting_pet.get_location()):
            self.interacting_pet.set_current_animation(config.RockActions.eating.value, True)
            return config.ItemID.broccoli
        elif self.item_id == config.ItemID.full_cup and self.rect.collidepoint(self.interacting_pet.get_location()):
            self.interacting_pet.set_current_animation(config.RockActions.drinking.value, True)
            return config.ItemID.full_cup
        elif self.item_id==config.ItemID.watering_can and self.rect.collidepoint(self.interacting_pet.get_location()):
            self.interacting_pet.set_current_animation(config.RockActions.clean.value,True)
            return config.ItemID.watering_can
        

        
    def handle_event(self, event, item_loc):
        if self.is_movable: 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.is_dragging = True
                    self.offset = (
                        event.pos[0] - self.rect.x,
                        event.pos[1] - self.rect.y
                    )
            elif event.type == pygame.MOUSEBUTTONUP and self.is_dragging:
                self.rect.x = item_loc[0]
                self.rect.y = item_loc[1]
                self.is_dragging = False
            elif event.type == pygame.MOUSEMOTION and self.is_dragging:
                self.rect.x = event.pos[0] - self.offset[0]
                self.rect.y = event.pos[1] - self.offset[1]

        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = self.pygame.mouse.get_pos()
                if self.is_mouse_selection(mouse_pos):
                    self.interacting_pet.set_location(self.item_location[0],self.item_location[1]+ self.rect.height/2.5)
                    self.interacting_pet.set_current_animation(config.RockActions.sleeping.value, True)