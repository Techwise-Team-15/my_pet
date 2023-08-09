import pygame
from pygame.locals import *
from game_util import PetConfig as Config
from pets import PetRaccoon, PetRock, PetMudskipper
from src import table as Table
from game_util import PetConfig as config, scene_items as scene_item
from pet_selection import PetSelection
from game_over import GameOver
from game_util.sprite_sheet import SpriteSheet
import os



class RaccoonHouse:
    def __init__(self,screen):
        self.house_screen = screen
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.initialize_house()
        self.pet_stats = scene_item.PetStats()
        self.pet_stats_bar_icon = scene_item.RaccoonIcons(pygame, self.screen)
        self.sprite_sheet_img = pygame.image.load(config.ITEM_PATH).convert_alpha() #SpriteSheet('../my_pet/assets/items_sheet.png')
        self.sprite_sheet = SpriteSheet(self.sprite_sheet_img)


        self.last_update = pygame.time.get_ticks()  
        self.animation_cooldown = 100

        self.my_raccoon = PetRaccoon(pygame, self.screen)
        self.my_raccoon.set_location(900, 1100)
        self.my_raccoon.set_current_animation(Config.RaccoonActions.idle.value)

        self.broccoli = self.sprite_sheet.get_image(0,384,96,96,1,config.BG_BLACK)
        self.broccoli_location = [475, 650]
        self.broccoli_item = scene_item.Item(config.ItemID.broccoli, pygame, self.screen, self.broccoli,self.my_raccoon, self.broccoli_location[0], self.broccoli_location[1])
        self.soap = self.sprite_sheet.get_image(0, 1728, 96, 96, 2, config.BG_BLACK)
        self.soap_location = [150, 600]
        self.soap_item = scene_item.Item(config.ItemID.soap, pygame, self.screen, self.soap, self.my_raccoon, self.soap_location[0], self.soap_location[1])
        self.wand = self.sprite_sheet.get_image(0, 1536, 96, 96, 2, config.BG_BLACK)
        self.wand_location = [300,370]
        self.wand_item = scene_item.Item(config.ItemID.wand, pygame, self.screen, self.wand, self.my_raccoon, self.wand_location[0], self.wand_location[1])
        self.bed = self.sprite_sheet.get_image(0,480,96,96,2,config.BG_BLACK)
        self.bed_location = [1100, 600]
        self.bed_item = scene_item.Item(config.ItemID.bed, pygame, self.screen,self.bed,self.my_raccoon, self.bed_location[0],self.bed_location[1],False)
        self.lamp_table_location = [800, 350]
        self.lamp_table = Table.Table(pygame, self.screen, self.lamp_table_location[0], self.lamp_table_location[1])
        self.full_cup = self.sprite_sheet.get_image(0,864,96,96,2, config.BG_BLACK)
        self.cup_item_location = [70, 400]
        self.full_cup_item = scene_item.Item(config.ItemID.full_cup, pygame, self.screen, self.full_cup, self.my_raccoon, self.cup_item_location[0], self.cup_item_location[1])
        # Pet Timer
        self.started_game_time = pygame.time.get_ticks()
        self.dirtiness_start = pygame.time.get_ticks()
        self.not_interacted = False
        self.raccoon_misbehaving_time = 10 #seconds time before raccoon misbehaves
        self.dirtiness_time = 30 #seconds time before raccoon starts getting dirty
        self.game_over = GameOver(pygame, self.screen, self.my_raccoon)

        # Thought bubble
        self.raccoon_thought = scene_item.ThoughtBubble(self.pet_stats)
        self.raccoon_made_a_mess = False
        self.pet_died = False
        self.is_raccoon_dirty = False
        self.is_hungry = False
        self.is_thirsty = False
        self.is_sad = False

    def initialize_house(self):
        self.house_screen.fill(config.BLACK)
        screen_background = pygame.image.load(config.RACCOON_BACKGROUND)
        screen_background = pygame.transform.scale(screen_background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.house_screen.blit(screen_background, (0, 0))
    
    def handle_event(self, is_raccoon_dirty):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if not is_raccoon_dirty:
                self.broccoli_item.handle_event(event,self.broccoli_location, is_raccoon_dirty)
                self.wand_item.handle_event(event, self.wand_location, is_raccoon_dirty)
                self.bed_item.handle_event(event, self.bed_location, is_raccoon_dirty)
                self.full_cup_item.handle_event(event, self.cup_item_location, is_raccoon_dirty)
                
            self.soap_item.handle_event(event, self.soap_location, is_raccoon_dirty)
            if not self.is_raccoon_dirty and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                x_location = config.SCREEN_WIDTH // 2 - self.my_raccoon.get_current_frame().get_width() // 2
                y_location = config.SCREEN_HEIGHT // 2 + self.my_raccoon.get_current_frame().get_height() // 3
                self.my_raccoon.set_location(x_location, y_location)  # Move the raccoon back to the center
                self.my_raccoon.set_current_animation(Config.RaccoonActions.idle.value, True)  # Set the idle animation
                self.not_interacted = False  # Reset the raccoon's interaction flag
                self.started_game_time = pygame.time.get_ticks()  # Reset the game time
            
            if(self.my_raccoon.did_overlap_with(self.soap_item)):
                self.my_raccoon.set_current_animation(Config.RaccoonActions.clean.value, True)
                self.not_interacted = False  
                self.is_raccoon_dirty = False
                self.started_game_time = pygame.time.get_ticks()
            elif(self.my_raccoon.did_overlap_with(self.broccoli_item) and not self.is_raccoon_dirty):
                self.started_game_time = pygame.time.get_ticks()
                self.my_raccoon.set_current_animation(Config.RaccoonActions.eating.value, True)
                self.pet_stats.fill_hunger()
            elif(self.my_raccoon.did_overlap_with(self.wand_item) and not self.is_raccoon_dirty):
                self.started_game_time = pygame.time.get_ticks()
                self.my_raccoon.set_current_animation(Config.RaccoonActions.magic.value, True)
                self.pet_stats.fill_happiness()
            elif(self.my_raccoon.did_overlap_with(self.bed_item) and not self.is_raccoon_dirty):
                self.started_game_time = pygame.time.get_ticks()
                
            elif(self.my_raccoon.did_overlap_with(self.full_cup_item) and not self.is_raccoon_dirty):
                self.started_game_time = pygame.time.get_ticks()
                self.my_raccoon.set_current_animation(Config.RaccoonActions.drinking.value, True)
                self.pet_stats.fill_thirst()

    
    
    def update_pet_stats(self):
        if self.pet_stats.get_pet_hunger()  < 50:
            self.is_hungry = True
        if self.pet_stats.get_pet_hunger()  > 49:
            self.is_hungry = False 
        if self.pet_stats.get_pet_thirst() < 50:
            self.is_thirsty = True
        if self.pet_stats.get_pet_thirst() > 49:
            self.is_thirsty = False
        if self.pet_stats.get_pet_happiness()  < 50:
            self.is_sad = True
        if self.pet_stats.get_pet_happiness() > 49:
            self.is_sad = False
    
    def draw_pet_thought(self):
        if self.is_raccoon_dirty == True:
            self.raccoon_thought.draw_thought_bubble(self.screen, self.my_raccoon.get_location(),self.pet_stats_bar_icon.get_soap_icon())
        if self.is_raccoon_dirty == False and self.is_hungry == True:
            self.raccoon_thought.draw_thought_bubble(self.screen, self.my_raccoon.get_location(),self.pet_stats_bar_icon.get_broccoli_icon())
        if self.is_raccoon_dirty == False and self.is_hungry == False and self.is_thirsty == True:
            self.raccoon_thought.draw_thought_bubble(self.screen, self.my_raccoon.get_location(), self.pet_stats_bar_icon.get_full_cup_icon())
        if self.is_raccoon_dirty == False and self.is_hungry == False and self.is_thirsty == False and self.is_sad == True:
            self.raccoon_thought.draw_thought_bubble(self.screen, self.my_raccoon.get_location(), self.pet_stats_bar_icon.get_wand_icon())

    def display_house_to_screen(self):
        self.screen.blit(self.my_raccoon.get_current_frame(), self.my_raccoon.get_location())
        self.screen.blit(self.soap_item.image,self.soap_item.get_item_location() )
        self.screen.blit(self.broccoli, self.broccoli_item.get_item_location())
        self.screen.blit(self.wand, self.wand_item.get_item_location())
        self.screen.blit(self.bed, self.bed_item.get_item_location())
        self.screen.blit(self.full_cup,self.full_cup_item.get_item_location())
        #self.screen.blit(self.lamp_table.get_current_frame(), self.lamp_table.get_location())

    def manage_pet_dirtiness(self):
        if (self.not_interacted and not self.is_raccoon_dirty) and self.my_raccoon.get_location()[0] < 1100:
            self.my_raccoon.set_location(self.my_raccoon.get_location()[0]+30, self.my_raccoon.get_location()[1])
        elif (self.not_interacted and not self.is_raccoon_dirty) and self.my_raccoon.get_location()[0] >= 1100:
            self.my_raccoon.set_current_animation(Config.RaccoonActions.dirty.value, False)
            self.is_raccoon_dirty = True
        if not self.is_raccoon_dirty and self.dirtiness_start + self.dirtiness_time * 1000 < pygame.time.get_ticks():
            self.my_raccoon.set_current_animation(Config.RaccoonActions.dirty.value, False)
            self.is_raccoon_dirty = True
            self.dirtiness_start = pygame.time.get_ticks() + (self.dirtiness_time*1000)
            
        if self.lamp_table.did_overlap_with(self.my_raccoon):
            self.lamp_table.update()
       # if not self.is_raccoon_dirty and self.started_game_time + self.raccoon_misbehaving_time * 1000 < pygame.time.get_ticks():
          #  self.my_raccoon.set_location(600,350)
           # self.my_raccoon.set_current_animation(Config.RaccoonActions.jumping.value, True)
           # self.started_game_time = pygame.time.get_ticks() + (self.raccoon_misbehaving_time*1000)
          #  self.not_interacted = True

    def main_frames(self):
        if self.pet_stats.get_pet_health() == 0 and not self.pet_died:
            self.my_raccoon.set_current_animation(Config.RaccoonActions.dying.value)
            x_location = config.SCREEN_WIDTH // 2 - self.my_raccoon.get_current_frame().get_width() // 2
            y_location = config.SCREEN_HEIGHT // 2 + self.my_raccoon.get_current_frame().get_height() // 3
            self.my_raccoon.set_location(x_location, y_location )
            self.pet_died = True

        if not self.pet_died:
            self.initialize_house()
            self.pet_stats_bar_icon.draw()
            self.pet_stats.update()
            self.pet_stats.draw(self.screen)
            
            self.display_house_to_screen()
            self.update_pet_stats()
            self.draw_pet_thought()
            self.manage_pet_dirtiness()

            self.my_raccoon.updated_frame()
            self.handle_event(self.is_raccoon_dirty)
            pygame.display.flip()
            
        else:
            self.game_over.main_frames()
        pygame.display.update()