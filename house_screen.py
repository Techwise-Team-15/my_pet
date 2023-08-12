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



class RockHouse:
    def __init__(self,screen):
        self.house_screen = screen
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.score_board = scene_item.Score(pygame=pygame, screen=screen)
        self.pet_stats = scene_item.PetStats()
        self.pet_stats_bar_icon = scene_item.Icons(pygame, self.screen)
        self.sprite_sheet_img = pygame.image.load(config.ITEM_PATH).convert_alpha() #SpriteSheet('../my_pet/assets/items_sheet.png')
        self.sprite_sheet = SpriteSheet(self.sprite_sheet_img)


        self.last_update = pygame.time.get_ticks()  
        self.animation_cooldown = 100

        self.my_rock = PetRock(pygame, self.screen)
        self.my_rock.set_location(600, 600)
        self.my_rock.set_current_animation(Config.RockActions.idle.value )

        self.broccoli = self.sprite_sheet.get_image(0,384,96,96,1,config.BG_BLACK)
        self.broccoli_location = [475, 175]
        self.broccoli_item = scene_item.Item(config.ItemID.broccoli, pygame, self.screen, self.broccoli,self.my_rock, self.broccoli_location[0], self.broccoli_location[1])
        self.watering_can = self.sprite_sheet.get_image(0, 288, 96, 96, 2, config.BG_BLACK)
        self.watering_can_location = [150, 600]
        self.watering_can_item = scene_item.Item( config.ItemID.watering_can, pygame, self.screen, self.watering_can,self.my_rock, self.watering_can_location[0], self.watering_can_location[1])
        self.ball = self.sprite_sheet.get_image(0, 1248, 96, 96, 2, config.BG_BLACK)
        self.ball_vanish = self.sprite_sheet.get_image(-1, 1248, 96, 96, 2, config.BLACK)
        self.ball_location = [300,400]
        self.ball_item = scene_item.Item( config.ItemID.ball,pygame, self.screen, self.ball,self.my_rock, self.ball_location[0], self.ball_location[1])
        self.bed = self.sprite_sheet.get_image(0,480,96,96,6.5,config.BG_BLACK)
        self.bed_location = [875, 295]
        self.bed_item = scene_item.Item(config.ItemID.bed, pygame, self.screen,self.bed,self.my_rock, self.bed_location[0],self.bed_location[1],False)
        self.lamp_table_location = [800, 350]
        self.lamp_table = Table.Table(pygame, self.screen, self.lamp_table_location[0], self.lamp_table_location[1])
        self.full_cup = self.sprite_sheet.get_image(0,864,96,96,2, config.BG_BLACK)
        self.cup_item_location = [70, 400]
        self.full_cup_item = scene_item.Item(config.ItemID.full_cup, pygame, self.screen, self.full_cup, self.my_rock, self.cup_item_location[0], self.cup_item_location[1])
        self.list_of_items = [self.full_cup_item, self.broccoli_item, self.ball_item, self.watering_can_item]
        # Pet Timer
        self.started_game_time = pygame.time.get_ticks()
        self.dirtiness_start = pygame.time.get_ticks()
        self.not_interacted = False
        self.rock_misbehaving_time = 10 #seconds time before rock misbehaves
        self.dirtiness_time = 30 #seconds time before rock starts getting dirty
        self.game_over = GameOver(pygame, self.screen, self.my_rock)
        self.item_timer = 10

        # Thought bubble
        self.rock_thought = scene_item.ThoughtBubble(self.pet_stats)
        self.rock_made_a_mess = False
        self.pet_died = False
        self.is_rock_dirty = False
        self.is_hungry = False
        self.is_thirsty = False
        self.is_sad = False

    def initialize_house(self):
        self.house_screen.fill(config.BLACK)
        screen_background = pygame.image.load(config.ROCK_HOUSE_BG_PATH)
        screen_background = pygame.transform.scale(screen_background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.house_screen.blit(screen_background, (0, 0))
    
    def handle_event(self, is_rock_dirty):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if not is_rock_dirty:
                self.broccoli_item.handle_event(event,self.broccoli_location, is_rock_dirty)
                self.ball_item.handle_event(event, self.ball_location, is_rock_dirty)
                self.bed_item.handle_event(event, self.bed_location, is_rock_dirty)
                self.full_cup_item.handle_event(event, self.cup_item_location, is_rock_dirty)
                
            self.watering_can_item.handle_event(event, self.watering_can_location, is_rock_dirty)
            if not self.is_rock_dirty and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                x_location = config.SCREEN_WIDTH // 2 - self.my_rock.get_current_frame().get_width() // 2
                y_location = config.SCREEN_HEIGHT // 2 + self.my_rock.get_current_frame().get_height() // 3
                self.my_rock.set_location(x_location, y_location)  # Move the rock back to the center
                self.my_rock.set_current_animation(Config.RockActions.idle.value, True)  # Set the idle animation
                self.not_interacted = False  # Reset the rock's interaction flag
                self.started_game_time = pygame.time.get_ticks()  # Reset the game time
            
            if(self.my_rock.did_overlap_with(self.watering_can_item)):
                self.my_rock.set_current_animation(Config.RockActions.very_dirty_shower.value, True)
                self.not_interacted = False  
                self.is_rock_dirty = False
                self.started_game_time = pygame.time.get_ticks()
            elif(self.my_rock.did_overlap_with(self.broccoli_item) and not self.is_rock_dirty):
                self.started_game_time = pygame.time.get_ticks()
                self.my_rock.set_current_animation(Config.RockActions.eating.value, True)
                self.pet_stats.fill_hunger()
            elif(self.my_rock.did_overlap_with(self.ball_item) and not self.is_rock_dirty):
                self.started_game_time = pygame.time.get_ticks()
                self.my_rock.set_current_animation(Config.RockActions.playing.value, True)
                self.pet_stats.fill_happiness()
            elif(self.my_rock.did_overlap_with(self.bed_item) and not self.is_rock_dirty):
                self.started_game_time = pygame.time.get_ticks()
                
            elif(self.my_rock.did_overlap_with(self.full_cup_item) and not self.is_rock_dirty):
                self.started_game_time = pygame.time.get_ticks()
                self.my_rock.set_current_animation(Config.RockActions.drinking.value, True)
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
        if self.is_rock_dirty == True:
            self.rock_thought.draw_thought_bubble(self.screen, self.my_rock.get_location(),self.pet_stats_bar_icon.get_watering_can_icon())
        if self.is_rock_dirty == False and self.is_hungry == True:
            self.rock_thought.draw_thought_bubble(self.screen, self.my_rock.get_location(),self.pet_stats_bar_icon.get_broccoli_icon())
        if self.is_rock_dirty == False and self.is_hungry == False and self.is_thirsty == True:
            self.rock_thought.draw_thought_bubble(self.screen, self.my_rock.get_location(), self.pet_stats_bar_icon.get_full_cup_icon())
        if self.is_rock_dirty == False and self.is_hungry == False and self.is_thirsty == False and self.is_sad == True:
            self.rock_thought.draw_thought_bubble(self.screen, self.my_rock.get_location(), self.pet_stats_bar_icon.get_ball_icon())

    def display_house_to_screen(self):
        self.screen.blit(self.my_rock.get_current_frame(), self.my_rock.get_location())
        self.screen.blit(self.bed, self.bed_item.get_item_location())
        self.screen.blit(self.lamp_table.get_current_frame(), self.lamp_table.get_location())
        for item in self.list_of_items:
            if not self.my_rock.did_overlap_with(item):
                self.screen.blit(item.image, item.get_item_location())
                
    def manage_pet_dirtiness(self):
        if (self.not_interacted and not self.is_rock_dirty) and self.my_rock.get_location()[0] < 1100:
            self.my_rock.set_location(self.my_rock.get_location()[0]+30, self.my_rock.get_location()[1])
        elif (self.not_interacted and not self.is_rock_dirty) and self.my_rock.get_location()[0] >= 1100:
            self.my_rock.set_current_animation(Config.RockActions.dirty.value, False)
            self.is_rock_dirty = True
        if not self.is_rock_dirty and self.dirtiness_start + self.dirtiness_time * 1000 < pygame.time.get_ticks():
            self.my_rock.set_current_animation(Config.RockActions.dirty.value, False)
            self.is_rock_dirty = True
            self.dirtiness_start = pygame.time.get_ticks() + (self.dirtiness_time*1000)
            
        if self.lamp_table.did_overlap_with(self.my_rock):
            self.lamp_table.update()
        if not self.is_rock_dirty and self.started_game_time + self.rock_misbehaving_time * 1000 < pygame.time.get_ticks():
            self.my_rock.set_location(600,350)
            self.my_rock.set_current_animation(Config.RockActions.jumping.value, True)
            self.started_game_time = pygame.time.get_ticks() + (self.rock_misbehaving_time*1000)
            self.not_interacted = True

    def main_frames(self):
        if self.pet_stats.get_pet_health() == 0 and not self.pet_died:
            self.my_rock.set_current_animation(Config.RockActions.dying.value)
            x_location = config.SCREEN_WIDTH // 2 - self.my_rock.get_current_frame().get_width() // 2
            y_location = config.SCREEN_HEIGHT // 2 + self.my_rock.get_current_frame().get_height() // 3
            self.my_rock.set_location(x_location, y_location )
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

            self.my_rock.updated_frame()
            self.handle_event(self.is_rock_dirty)
            self.score_board.draw_score_text()
            self.score_board.add_score()
            pygame.display.flip()
            
        else:
            score = self.score_board.score_value
            self.game_over.main_frames(score)
        pygame.display.update()