import pygame
from pygame.locals import *
from game_util import PetConfig as Config
from pets import PetRaccoon, PetRock, PetMudskipper
from src import table as Table
from game_util import PetConfig as config, scene_items as scene_item, music_player as MP
from pet_selection import PetSelection
from game_over import GameOver
from game_util.sprite_sheet import SpriteSheet
from game_config import GameConfig as gc

import os



class MudskipperHouse:
    def __init__(self,screen,music):
        self.house_screen = screen
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.score_board = scene_item.Score(pygame=pygame, screen=screen)
        self.initialize_house()
        self.pet_stats = scene_item.PetStats()
        self.pet_stats_bar_icon = scene_item.RaccoonIcons(pygame, self.screen)
        self.sprite_sheet_img = pygame.image.load(config.ITEM_PATH).convert_alpha() #SpriteSheet('../my_pet/assets/items_sheet.png')
        self.sprite_sheet = SpriteSheet(self.sprite_sheet_img)
        self.main_music=music
        
      


        self.last_update = pygame.time.get_ticks()  
        self.animation_cooldown = 100

        self.my_mudskipper = PetMudskipper(pygame, self.screen)
        self.my_mudskipper.set_location(900, 1100)
        self.my_mudskipper.set_current_animation(Config.MudskipperActions.idle.value)

        self.broccoli = self.sprite_sheet.get_image(0,384,96,96,1,config.BG_BLACK)
        self.broccoli_location = [475, 650]
        self.broccoli_item = scene_item.Item(config.ItemID.broccoli, pygame, self.screen, self.broccoli,self.my_mudskipper, self.broccoli_location[0], self.broccoli_location[1])
        self.gray_cloud = self.sprite_sheet.get_image(0, 1440, 96, 96, 2, config.BG_BLACK)
        self.gray_cloud_location = [480,0]
        self.ball = self.sprite_sheet.get_image(0, 1248, 96, 96, 2, config.BG_BLACK)
        self.ball_location = [300,400]
        self.ball_item = scene_item.Item( config.ItemID.ball,pygame, self.screen, self.ball,self.my_mudskipper, self.ball_location[0], self.ball_location[1])
        self.gray_cloud_item = scene_item.Item(config.ItemID.wand, pygame, self.screen, self.gray_cloud, self.my_mudskipper, self.gray_cloud_location[0], self.gray_cloud_location[1])
        self.bed = self.sprite_sheet.get_image(0,480,96,96,2,config.BG_BLACK)
        self.bed_location = [1100, 600]
        self.bed_item = scene_item.Item(config.ItemID.bed, pygame, self.screen,self.bed,self.my_mudskipper, self.bed_location[0],self.bed_location[1],False)
        self.lamp_table_location = [800, 350]
        self.lamp_table = Table.Table(pygame, self.screen, self.lamp_table_location[0], self.lamp_table_location[1])
        self.full_cup = self.sprite_sheet.get_image(0,864,96,96,2, config.BG_BLACK)
        self.cup_item_location = [70, 400]
        self.full_cup_item = scene_item.Item(config.ItemID.full_cup, pygame, self.screen, self.full_cup, self.my_mudskipper, self.cup_item_location[0], self.cup_item_location[1])
        # Pet Timer
        self.started_game_time = pygame.time.get_ticks()
        self.dirtiness_start = pygame.time.get_ticks()
        self.not_interacted = False
        self.mudskipper_misbehaving_time = 10 #seconds time before raccoon misbehaves
        self.dirtiness_time = 30 #seconds time before raccoon starts getting dirty
        self.game_over = GameOver(pygame, self.screen, self.my_mudskipper)

        # Thought bubble
        self.mudskipper_thought = scene_item.ThoughtBubble(self.pet_stats)
        self.mudskipper_made_a_mess = False
        self.pet_died = False
        self.is_mudskipper_dirty = False
        self.is_hungry = False
        self.is_thirsty = False
        self.is_sad = False

    def initialize_house(self):
        self.house_screen.fill(config.BLACK)
        screen_background = pygame.image.load(config.MUDSKIPPER_BACKGROUND)
        screen_background = pygame.transform.scale(screen_background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.house_screen.blit(screen_background, (0, 0))
    
    def handle_event(self, is_mudskipper_dirty):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if not is_mudskipper_dirty:
                self.broccoli_item.handle_event(event,self.broccoli_location, is_mudskipper_dirty)
                self.gray_cloud_item.handle_event(event, self.gray_cloud_location, is_mudskipper_dirty)
                self.bed_item.handle_event(event, self.bed_location, is_mudskipper_dirty)
                self.full_cup_item.handle_event(event, self.cup_item_location, is_mudskipper_dirty)
                self.ball_item.handle_event(event,self.ball_location,is_mudskipper_dirty)
                
            
            if(self.my_mudskipper.did_overlap_with(self.gray_cloud_item)):
                self.my_mudskipper.set_current_animation(Config.MudskipperActions.clean.value, True)
                self.not_interacted = False  
                self.is_mudskipper_dirty = False
                self.started_game_time = pygame.time.get_ticks()
            elif(self.my_mudskipper.did_overlap_with(self.broccoli_item) and not self.is_mudskipper_dirty):
                self.started_game_time = pygame.time.get_ticks()
                self.my_mudskipper.set_current_animation(Config.MudskipperActions.eating.value, True)
                self.pet_stats.fill_hunger()
            elif(self.my_mudskipper.did_overlap_with(self.ball_item) and not self.is_mudskipper_dirty):
                self.started_game_time = pygame.time.get_ticks()
                self.my_mudskipper.set_current_animation(Config.MudskipperActions.playing.value, True)
                self.pet_stats.fill_happiness()
            elif(self.my_mudskipper.did_overlap_with(self.bed_item) and not self.is_mudskipper_dirty):
                self.started_game_time = pygame.time.get_ticks()
                
            elif(self.my_mudskipper.did_overlap_with(self.full_cup_item) and not self.is_mudskipper_dirty):
                self.started_game_time = pygame.time.get_ticks()
                self.my_mudskipper.set_current_animation(Config.MudskipperActions.drinking.value, True)
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
        if self.is_mudskipper_dirty == True:
            self.mudskipper_thought.draw_thought_bubble(self.screen, self.my_mudskipper.get_location(),self.pet_stats_bar_icon.get_gray_cloud_icon())
        if self.is_mudskipper_dirty == False and self.is_hungry == True:
            self.mudskipper_thought.draw_thought_bubble(self.screen, self.my_mudskipper.get_location(),self.pet_stats_bar_icon.get_broccoli_icon())
        if self.is_mudskipper_dirty == False and self.is_hungry == False and self.is_thirsty == True:
            self.mudskipper_thought.draw_thought_bubble(self.screen, self.my_mudskipper.get_location(), self.pet_stats_bar_icon.get_full_cup_icon())
        if self.is_mudskipper_dirty == False and self.is_hungry == False and self.is_thirsty == False and self.is_sad == True:
            self.mudskipper_thought.draw_thought_bubble(self.screen, self.my_mudskipper.get_location(), self.pet_stats_bar_icon.get_wand_icon())

    def display_house_to_screen(self):
        self.screen.blit(self.my_mudskipper.get_current_frame(), self.my_mudskipper.get_location())
        self.screen.blit(self.gray_cloud,self.gray_cloud_item.get_item_location() )
        self.screen.blit(self.broccoli, self.broccoli_item.get_item_location())
        self.screen.blit(self.ball, self.ball_item.get_item_location())
        self.screen.blit(self.bed, self.bed_item.get_item_location())
        self.screen.blit(self.full_cup,self.full_cup_item.get_item_location())
        
    def manage_pet_dirtiness(self):
        if (self.not_interacted and not self.is_mudskipper_dirty) and self.my_mudskipper.get_location()[0] < 1100:
            self.my_mudskipper.set_location(self.my_mudskipper.get_location()[0]+30, self.my_mudskipper.get_location()[1])
        elif (self.not_interacted and not self.is_mudskipper_dirty) and self.my_mudskipper.get_location()[0] >= 1100:
            self.my_mudskipper.set_current_animation(Config.MudskipperActions.dirty.value, False)
            self.is_mudskipper_dirty = True
        if not self.is_mudskipper_dirty and self.dirtiness_start + self.dirtiness_time * 1000 < pygame.time.get_ticks():
            self.my_mudskipper.set_current_animation(Config.MudskipperActions.dirty.value, False)
            self.is_mudskipper_dirty = True
            self.dirtiness_start = pygame.time.get_ticks() + (self.dirtiness_time*1000)
            
        if self.lamp_table.did_overlap_with(self.my_mudskipper):
            self.lamp_table.update()
     
    def main_frames(self):
        if self.pet_stats.get_pet_health() == 0 and not self.pet_died:
            self.my_mudskipper.set_current_animation(Config.MudskipperActions.dying.value)
            x_location = config.SCREEN_WIDTH // 2 - self.my_mudskipper.get_current_frame().get_width() // 2
            y_location = config.SCREEN_HEIGHT // 2 + self.my_mudskipper.get_current_frame().get_height() // 3
            self.my_mudskipper.set_location(x_location, y_location )
            self.pet_died = True
            self.main_music.load_track(config.game_over)
            if gc.IS_SOUND_ON:
                 self.main_music.play(True)
            else:
                 self.main_music.stop()
            

        if not self.pet_died:
            self.initialize_house()
            self.pet_stats_bar_icon.draw()
            self.pet_stats.update()
            self.pet_stats.draw(self.screen)
            
            self.display_house_to_screen()
            self.update_pet_stats()
            self.draw_pet_thought()
            self.manage_pet_dirtiness()

            self.my_mudskipper.updated_frame()
            self.handle_event(self.is_mudskipper_dirty)
            self.score_board.draw_score_text()
            self.score_board.add_score()
            pygame.display.flip()
            
        else:
            score = self.score_board.score_value
            self.game_over.main_frames(score)
        pygame.display.update()