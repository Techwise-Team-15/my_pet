import pygame, pygame.freetype
from pygame.locals import *
from .sprite_sheet import SpriteSheet as SpriteSheet
from .pet_config import PetConfig as config
import os

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

    def bar_drain_thirst(self):
        if self.hp > 0:
            pygame.time.delay(config.HP_DRAIN_TIME)
            self.hp -= 5
    
    def bar_drain_hunger(self):
        if self.hp > 0:
            pygame.time.delay(config.HP_DRAIN_TIME)
            self.hp -= 3
    
    def bar_drain_happy(self):
        if self.hp > 0:
            pygame.time.delay(config.HP_DRAIN_TIME)
            self.hp -= 7
    
    def bar_drain_health(self):
        if self.hp > 0:
            pygame.time.delay(config.HP_DRAIN_TIME)
            self.hp -= 10
    
    
    
    def bar_fill(self):
        self.hp = self.max_hp

class Icons:
    def __init__(self,pygame, screen) -> None:
        self.pygame = pygame
        self.screen = screen
        self.heart_img = pygame.image.load(config.HEART_PATH).convert_alpha()
        self.heart_img = pygame.transform.scale(self.heart_img, (40, 40))
        self.sprite_sheet = SpriteSheet(pygame.image.load(config.ITEM_PATH).convert_alpha())
        self.watering_can = self.sprite_sheet.get_image(0, 288, 96, 96, 1, config.BG_BLACK)
        self.broccoli = self.sprite_sheet.get_image(0,384,96,96,.75,config.BG_BLACK)
        self.full_cup = self.sprite_sheet.get_image(0,864,96,96,.75,config.BG_BLACK)
        self.ball = self.sprite_sheet.get_image(0, 1248, 96, 96, .75, config.BG_BLACK)

    def get_broccoli_icon(self):
        return self.broccoli
    
    def get_full_cup_icon(self):
        return self.full_cup
    
    def get_ball_icon(self):
        return self.ball
    
    def get_watering_can_icon(self):
        return self.watering_can

    def draw(self):
        self.screen.blit(self.heart_img, (config.SCREEN_WIDTH - 240, 45))
        self.screen.blit(self.full_cup, (config.SCREEN_WIDTH - 260, 80))
        self.screen.blit(self.broccoli, (config.SCREEN_WIDTH - 250, 130))
        self.screen.blit(self.ball, (config.SCREEN_WIDTH - 250, 180))

class Buttons:
    def __init__(self, screen, location, button_text,text_size = 36, button_text_color=config.WHITE):
        self.screen = screen
        self.location = location
        self.font = pygame.font.Font(config.FONT, text_size)
        self.text = self.font.render(button_text, True, button_text_color)
        self.item_rect = self.text.get_rect(topleft=location)
        self.is_mouse_hovering = False
        self.is_mouse_clicking = False
        self.button_width = self.item_rect.width
        self.button_height = self.item_rect.height
    
    def draw(self):
        self.screen.blit(self.text, self.location)

    def is_mouse_selection(self, mouse_pos):
        if mouse_pos[0] >= self.location[0] and mouse_pos[0] <= (self.location[0] + self.button_width):
            if mouse_pos[1] >= self.location[1] and mouse_pos[1] <= (self.location[1] + self.button_height):
                return True
        return False


class RaccoonIcons:
    def __init__(self,pygame, screen) -> None:
        self.pygame = pygame
        self.screen = screen
        self.heart_img = pygame.image.load(config.HEART_PATH).convert_alpha()
        self.heart_img = pygame.transform.scale(self.heart_img, (40, 40))
        self.sprite_sheet = SpriteSheet(pygame.image.load(config.ITEM_PATH).convert_alpha())
        self.soap = self.sprite_sheet.get_image(0, 1728, 96, 96, 1, config.BG_BLACK)
        self.broccoli = self.sprite_sheet.get_image(0,384,96,96,.75,config.BG_BLACK)
        self.full_cup = self.sprite_sheet.get_image(0,864,96,96,.75,config.BG_BLACK)
        self.wand = self.sprite_sheet.get_image(0, 1536, 96, 96, .75, config.BG_BLACK)

    def get_broccoli_icon(self):
        return self.broccoli
    
    def get_full_cup_icon(self):
        return self.full_cup
    
    def get_wand_icon(self):
        return self.wand
    
    def get_soap_icon(self):
        return self.soap

    def draw(self):
        self.screen.blit(self.heart_img, (config.SCREEN_WIDTH - 240, 45))
        self.screen.blit(self.full_cup, (config.SCREEN_WIDTH - 260, 80))
        self.screen.blit(self.broccoli, (config.SCREEN_WIDTH - 250, 130))
        self.screen.blit(self.wand, (config.SCREEN_WIDTH - 250, 180))       

class PetStats:
    health_bar = StatusBar(950, 50, 200, 25, 1000, config.LIGHT_PINK, config.LIGHT_ORANGE)
    thirst_bar = StatusBar(950, 100, 200, 25, 1000, config.LIGHT_BLUE, config.LIGHT_ORANGE)
    hunger_bar = StatusBar(950, 150, 200, 25, 1000, config.LIGHT_GREEN, config.LIGHT_ORANGE)
    happiness_bar = StatusBar(950, 200, 200, 25, 1000, config.LIGHT_PURPLE, config.LIGHT_ORANGE)

    def get_pet_health(self):
        return self.health_bar.hp
    
    def get_pet_thirst(self):
        return self.thirst_bar.hp
    
    def get_pet_hunger(self):
        return self.hunger_bar.hp
    
    def get_pet_happiness(self):
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
        self.thirst_bar.bar_drain_thirst()
        self.hunger_bar.bar_drain_hunger()
        self.happiness_bar.bar_drain_happy()
        if self.hunger_bar.hp == 0 and self.thirst_bar.hp == 0:
            self.health_bar.bar_drain_health()

class Item:
    def __init__(self, item_id, pygame, screen, image, pet, x, y, is_movable = True):
        self.pygame = pygame
        self.screen = screen
        self.image = image
        self.item_rect = self.image.get_rect(topleft=(x, y))
        self.is_dragging = False
        self.is_movable = is_movable
        self.item_id = item_id
        self.interacting_pet = pet
        self.item_location = [x,y]
        self.offset = (0, 0)
        self.is_rock_dirty = False

    def get_mask(self):
        item_mask = pygame.mask.from_surface(self.image)
        
        return item_mask
    def get_item_location(self):
        return self.item_location
    
    def is_mouse_selection(self, mouse_pos):
        item_location = self.item_location
        item_width = self.item_rect.width
        item_height = self.item_rect.height 
        if mouse_pos[0] >= item_location[0] and mouse_pos[0] <= (item_location[0] + item_width):
            if mouse_pos[1] >= item_location[1] and mouse_pos[1] <= (item_location[1] + item_height):
                return True
        return False
        
    def handle_event(self, event, item_loc, is_rock_dirty) :
        if self.is_movable: 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_mouse_selection(event.pos):
                    self.is_dragging = True
                    self.offset = (
                        event.pos[0] - self.item_location[0],
                        event.pos[1] - self.item_location[1]
                    )
            elif event.type == pygame.MOUSEBUTTONUP and self.is_dragging:
                self.item_location[0] = item_loc[0]
                self.item_location[1] = item_loc[1]
                self.is_dragging = False
            elif event.type == pygame.MOUSEMOTION and self.is_dragging:
                self.item_location[0] = event.pos[0] - self.offset[0]
                self.item_location[1] = event.pos[1] - self.offset[1]

        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = self.pygame.mouse.get_pos()
                if self.is_mouse_selection(mouse_pos) and  is_rock_dirty == False:
                    self.interacting_pet.set_location(self.item_location[0],self.item_location[1]+ self.item_rect.height/2.5)
                    if self.interacting_pet.get_pet_id() == "rock":
                        self.interacting_pet.set_current_animation(config.RockActions.sleeping.value, True)
                    elif self.interacting_pet.get_pet_id() == "raccoon":
                        self.interacting_pet.set_current_animation(config.RaccoonActions.sleeping.value, True)
                   # elif self.interacting_pet.get_pet_id() == "mudskipper":
                      #  self.interacting_pet.set_current_animation(config.MudskipperActions.sleeping.value, True)


class Score:
    def __init__(self, pygame, screen):
        self.font = pygame.font.Font(None,36)
        self.pygame = pygame
        self.screen  = screen
        self.score_value = 0
        self.score_increment = 10
        self.time_to_add_score = 5
        self.time_to_add_score_start = pygame.time.get_ticks()
        
    
    def add_score(self):
        current_time = self.pygame.time.get_ticks()
        if current_time >= self.time_to_add_score_start + self.time_to_add_score * 1000:
            self.time_to_add_score_start = current_time + (self.time_to_add_score * 1000)
            self.score_value += self.score_increment
            return self.score_value

    def draw_score_text(self):
        self.score_text = self.font.render(f'Score: {self.score_value}', True, config.BLACK)
        self.screen.blit(self.score_text, (10,10))


class ThoughtBubble:
    def __init__(self, pet_stats):
        self.thought_bubble_radius = 40
        self.thought_bubble_color = config.WHITE
        self.sprite_sheet_img = pygame.image.load(config.ITEM_PATH).convert_alpha() #SpriteSheet('../my_pet/assets/items_sheet.png')
        self.sprite_sheet = SpriteSheet(self.sprite_sheet_img)
        self.pet_stats = pet_stats
    

    def draw_thought_bubble(self,screen, pet_location, icon_to_draw ):
        bubble_offset = (0, 50)  # Offset for the first bubble (above the rock)
        bubble_x = pet_location[0] + bubble_offset[0] - self.thought_bubble_radius
        bubble_y = pet_location[1] + bubble_offset[1] - self.thought_bubble_radius

        # Draw the first bubble (above the rock)
        pygame.draw.circle(screen, self.thought_bubble_color, (bubble_x + self.thought_bubble_radius, bubble_y + self.thought_bubble_radius), self.thought_bubble_radius//2)

        # Update the bubble_offset for the second bubble (below the first bubble)
        bubble_offset = (0, -50)  
        bubble_x = pet_location[0] + bubble_offset[0] - self.thought_bubble_radius
        bubble_y = pet_location[1] + bubble_offset[1] - self.thought_bubble_radius

        # Draw the second bubble (below the first bubble)
        pygame.draw.circle(screen, self.thought_bubble_color, (bubble_x + self.thought_bubble_radius, bubble_y + self.thought_bubble_radius), self.thought_bubble_radius)

        # Draw the broccoli sprite inside the main thought bubble
        item_x = bubble_x + (self.thought_bubble_radius - icon_to_draw.get_width() // 2)
        item_y = bubble_y + (self.thought_bubble_radius - icon_to_draw.get_height() // 2)
        screen.blit(icon_to_draw, (item_x, item_y))