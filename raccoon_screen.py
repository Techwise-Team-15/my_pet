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



class RaccoonHouse:
    def __init__(self,screen,game_menu, music):
        self.house_screen = screen
        self.screen = screen
        self.gm = game_menu
        self.player_name = gc.SAVED_PET_NAMES[0] if len(gc.SAVED_PET_NAMES) > 0 else ''
        self.player_board = scene_item.PlayerName(pygame=pygame, screen=screen, player_name=self.player_name)
        self.score_board = scene_item.Score(pygame=pygame, screen=screen)
        self.kill_pet_button = scene_item.Buttons(self.screen,[50,100],"Kill")
        self.pet_stats = scene_item.PetStats()
        self.pet_stats_bar_icon = scene_item.RaccoonIcons(pygame, self.screen)
        self.sprite_sheet_img = pygame.image.load(config.ITEM_PATH).convert_alpha() #SpriteSheet('../my_pet/assets/items_sheet.png')
        self.sprite_sheet = SpriteSheet(self.sprite_sheet_img)
        self.main_music = music


        self.last_update = pygame.time.get_ticks()  
        self.animation_cooldown = 100

        self.my_raccoon = PetRaccoon(pygame, self.screen)
        self.x_location = 550
        self.y_location = 500
        self.my_raccoon_location = [550,500]
        self.my_raccoon.set_location(0, 0)
        self.my_raccoon.set_current_animation(Config.RaccoonActions.idle.value)

        self.broccoli = self.sprite_sheet.get_image(0,384,96,96,1,config.BG_BLACK)
        self.broccoli_location = [890, 600]
        self.broccoli_item = scene_item.Item(config.ItemID.broccoli, pygame, self.screen, self.broccoli,self.my_raccoon, self.broccoli_location[0], self.broccoli_location[1])
        self.soap = self.sprite_sheet.get_image(0, 1728, 96, 96, .6, config.BG_BLACK)
        self.soap_location = [205, 410]
        self.soap_item = scene_item.Item(config.ItemID.soap, pygame, self.screen, self.soap, self.my_raccoon, self.soap_location[0], self.soap_location[1])
        self.wand = self.sprite_sheet.get_image(0, 1536, 96, 96, 1, config.BG_BLACK)
        self.wand_location = [300,500]
        self.wand_item = scene_item.Item(config.ItemID.wand, pygame, self.screen, self.wand, self.my_raccoon, self.wand_location[0], self.wand_location[1])
        self.pillow = self.sprite_sheet.get_image(0,1824,96,96,1.5,config.BG_BLACK)
        self.pillow = self.sprite_sheet.get_flipped_image(self.pillow)
        self.pillow_location = [750, 420]
        self.bowl_table = self.sprite_sheet.get_image(0,1920,96,96,2,config.BG_BLACK)
        self.bowl_table_location = [150, 400]
        self.table = self.sprite_sheet.get_image(0,2016,96,96,4,config.BG_BLACK)
        self.table_location = [700, 400]
        self.pillow_item = scene_item.Item(config.ItemID.pillow, pygame, self.screen, self.pillow, self.my_raccoon, self.pillow_location[0],self.pillow_location[1],False)
        self.broken_vase_location = [1150, 390]
        self.broken_vase = Table.Table(pygame, self.screen, self.broken_vase_location[0], self.broken_vase_location[1])
        self.broken_vase.set_current_selected_animation(config.TableActions.broken_vase.value)
        self.full_cup = self.sprite_sheet.get_image(0,864,96,96,1, config.BG_BLACK)
        self.cup_item_location = [795, 600]
        self.full_cup_item = scene_item.Item(config.ItemID.full_cup, pygame, self.screen, self.full_cup, self.my_raccoon, self.cup_item_location[0], self.cup_item_location[1])
        # Pet Timer
        self.started_game_time = pygame.time.get_ticks()
        self.dirtiness_start = pygame.time.get_ticks()
        self.not_interacted = False
        self.raccoon_misbehaving_time = 10 #seconds time before raccoon misbehaves
        self.dirtiness_time = 30 #seconds time before raccoon starts getting dirty
        self.game_over = GameOver(pygame, self.screen, self.gm, self.my_raccoon)
        self.half_full_cup = self.sprite_sheet.get_image(0,960,96,96,1, config.BG_BLACK)
        self.half_full_cup_location = [795, 600]
        self.half_full_cup_item = scene_item.Item(config.ItemID.half_cup,pygame, self.screen, self.half_full_cup, self.my_raccoon, self.half_full_cup_location[0],self.half_full_cup_location[1])
        self.item_timer_start = pygame.time.get_ticks()
        self.item_timer = 10
        self.item_on_cooldown = False
        self.list_of_items = [self.broccoli_item, self.wand_item, self.soap_item]
        self.sleep_start = pygame.time.get_ticks()
        self.sleep_time = 10

        # Thought bubble
        self.raccoon_thought = scene_item.ThoughtBubble(self.pet_stats)
        self.raccoon_made_a_mess = False
        self.pet_died = False
        # raccoon properties
        self.is_raccoon_dirty = False
        self.is_hungry = False
        self.is_thirsty = False
        self.is_sad = False
        self.is_sleeping = False
        # vase property 
        self.has_touched_vase = False

    def reset(self):
        self.my_raccoon.set_current_animation(config.RaccoonActions.idle.value)
        self.my_raccoon.set_location(self.x_location, self.y_location)
        self.not_interacted = False
        self.started_game_time = pygame.time.get_ticks()
        self.dirtiness_start = pygame.time.get_ticks()
        self.pet_stats.reset()
        self.pet_died = False
    
    def initialize_house(self):
        self.house_screen.fill(config.BLACK)
        screen_background = pygame.image.load(config.RACCOON_BACKGROUND)
        screen_background = pygame.transform.scale(screen_background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.house_screen.blit(screen_background, (0, 0))
        self.kill_pet_button.draw()
    
    def handle_event(self, is_raccoon_dirty):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.kill_pet_button.is_mouse_selection(mouse_pos):
                    self.pet_stats.health_bar.drain_health_fully()
                    
            if not is_raccoon_dirty:
                self.broccoli_item.handle_event(event,self.broccoli_location, is_raccoon_dirty)
                self.wand_item.handle_event(event, self.wand_location, is_raccoon_dirty)
                self.pillow_item.handle_event(event, self.pillow_location, is_raccoon_dirty)
                self.full_cup_item.handle_event(event, self.cup_item_location, is_raccoon_dirty)
                
            self.soap_item.handle_event(event, self.soap_location, is_raccoon_dirty)
            if not self.is_raccoon_dirty and event.type == pygame.KEYDOWN and event.key == pygame.K_r: 
                self.my_raccoon.set_location(self.x_location, self.y_location)  # Move the rock back to the center
                self.my_raccoon.set_current_animation(Config.RaccoonActions.idle.value, True)  # Set the idle animation
                self.not_interacted = False  # Reset the rock's interaction flag
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
            if(self.my_raccoon.did_overlap_with(self.wand_item) and not self.is_raccoon_dirty):
                self.started_game_time = pygame.time.get_ticks()
                self.my_raccoon.set_current_animation(Config.RaccoonActions.magic.value, True)
                self.pet_stats.fill_happiness()
            elif(self.my_raccoon.did_overlap_with(self.pillow_item) and not self.is_raccoon_dirty):
                self.is_sleeping = True
                self.started_game_time = pygame.time.get_ticks()

            if (self.is_sleeping == True) and self.sleep_start + self.sleep_time * 1000 < pygame.time.get_ticks():
                self.my_raccoon.set_location(self.x_location, self.y_location)
                self.my_raccoon.set_current_animation(Config.RaccoonActions.idle.value, True)
                self.sleep_start = pygame.time.get_ticks()
                self.started_game_time = pygame.time.get_ticks()
                self.is_sleeping = False
                
            elif(self.my_raccoon.did_overlap_with(self.full_cup_item) and not self.is_raccoon_dirty):
                self.started_game_time = pygame.time.get_ticks()
                self.my_raccoon.set_current_animation(Config.RaccoonActions.drinking.value, True)
                self.pet_stats.fill_thirst()
            
            if(self.my_raccoon.current_selected_animation == config.RaccoonActions.clean.value and self.my_raccoon.has_animation_ended()):
                self.my_raccoon.set_current_animation(Config.RaccoonActions.idle.value)
                self.my_raccoon.set_location(self.x_location, self.y_location)
                self.is_rock_dirty = False
                self.not_interacted = False
                self.started_game_time = pygame.time.get_ticks()
                self.dirtiness_start   = pygame.time.get_ticks()
                

    
    
    def update_pet_stats(self):
        if self.pet_stats.get_pet_hunger()  < 500:
            self.is_hungry = True
        if self.pet_stats.get_pet_hunger()  > 490:
            self.is_hungry = False 
        if self.pet_stats.get_pet_thirst() < 500:
            self.is_thirsty = True
        if self.pet_stats.get_pet_thirst() > 490:
            self.is_thirsty = False
        if self.pet_stats.get_pet_happiness()  < 500:
            self.is_sad = True
        if self.pet_stats.get_pet_happiness() > 490:
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
        self.screen.blit(self.pillow, self.pillow_item.get_item_location())
        self.screen.blit(self.my_raccoon.get_current_frame(), self.my_raccoon.get_location())
            
        self.screen.blit(self.bowl_table,self.bowl_table_location)
        self.screen.blit(self.table,self.table_location)
        self.screen.blit(self.broken_vase.get_current_frame(), self.broken_vase.get_location())
        for item in self.list_of_items:
            if not self.my_raccoon.did_overlap_with(item):
                self.screen.blit(item.image, item.get_item_location())      
        if self.my_raccoon.did_overlap_with(self.full_cup_item) and self.item_on_cooldown == False:
            self.item_timer_start = pygame.time.get_ticks() + (self.item_timer *1000)
            self.item_on_cooldown = True
        elif self.item_on_cooldown == False:
            self.screen.blit(self.full_cup, self.full_cup_item.get_item_location())
        if self.item_timer_start + self.item_timer * 1000 < pygame.time.get_ticks():
            self.item_on_cooldown = False
        if self.item_on_cooldown == True:
            self.screen.blit(self.half_full_cup, self.half_full_cup_location)

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
            
        if self.broken_vase.did_overlap_with(self.my_raccoon):
            # self.broken_vase.update()
            self.has_touched_vase = True
        if self.has_touched_vase and self.broken_vase.get_location()[1] < 490:
            self.broken_vase.set_location(self.broken_vase.get_location()[0],self.broken_vase.get_location()[1]+10)
            self.broken_vase.update()

        if not self.is_raccoon_dirty and self.started_game_time + self.raccoon_misbehaving_time * 1000 < pygame.time.get_ticks():
            self.my_raccoon.set_location(800,350)
            self.my_raccoon.set_current_animation(Config.RaccoonActions.fighting.value, True)
            self.started_game_time = pygame.time.get_ticks() + (self.raccoon_misbehaving_time*1000)
            self.not_interacted = True
        

    def main_frames(self):
        if self.pet_stats.get_pet_health() == 0 and not self.pet_died:
            self.my_raccoon.set_current_animation(Config.RaccoonActions.dying.value)
            x_location = config.SCREEN_WIDTH // 2 - self.my_raccoon.get_current_frame().get_width() // 2
            y_location = config.SCREEN_HEIGHT // 2 + self.my_raccoon.get_current_frame().get_height() // 3
            self.my_raccoon.set_location(x_location, y_location )
            self.pet_died = True
            self.main_music.load_track(config.game_over)
            if gc.IS_SOUND_ON:
                self.main_music.play(True)
            else:
                self.main_music.stop()

        if not self.pet_died:
            
            self.initialize_house()
            self.pet_stats_bar_icon.draw()
            if self.is_sleeping == False:
                self.pet_stats.update()
            self.pet_stats.draw(self.screen)
            
            self.display_house_to_screen()
            self.update_pet_stats()
            self.draw_pet_thought()
            self.manage_pet_dirtiness()

            self.my_raccoon.updated_frame()
            self.handle_event(self.is_raccoon_dirty)
            self.score_board.draw_score_text()
            self.score_board.add_score()
            if self.player_name != '':
                self.player_board.draw_player_name_text()
            pygame.display.flip()
            
        else:
            score = self.score_board.score_value
            self.game_over.main_frames(score)
        pygame.display.update()