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


class HouseScreen:
    def __init__(self, screen):
        self.house_screen = screen
        self.thought_bubble_radius = 40  
        self.thought_bubble_color = (255, 255, 255)  
        

    def draw(self):
        self.house_screen.fill(config.BLACK)
        screen_background = pygame.image.load(config.ROCK_HOUSE_BG_PATH)
        screen_background = pygame.transform.scale(screen_background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.house_screen.blit(screen_background, (0, 0))

class RockHouse:
    def __init__(self,screen):
        self.house_screen = screen
        self.thought_bubble_radius = 50  
        self.thought_bubble_color = config.WHITE
    

        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.house = HouseScreen(self.screen)
        self.pet_stats = scene_item.PetStats()
        self.pet_stats_bar_icon = scene_item.BarIcons(pygame, self.screen)
        self.sprite_sheet_img = pygame.image.load(config.ITEM_PATH).convert_alpha() #SpriteSheet('../my_pet/assets/items_sheet.png')
        self.sprite_sheet = SpriteSheet(self.sprite_sheet_img)


        self.last_update = pygame.time.get_ticks()  
        self.animation_cooldown = 100

        self.my_rock = PetRock(pygame, self.screen)
        self.my_rock.set_location(600, 600)
        self.my_rock.set_current_animation(Config.RockActions.idle.value, True)

        self.broccoli = self.sprite_sheet.get_image(0,384,96,96,1,config.BG_BLACK)
        self.broccoli_location = [475, 175]
        self.broccoli_item = scene_item.Item(config.ItemID.broccoli, pygame, self.screen, self.broccoli,self.my_rock, self.broccoli_location[0], self.broccoli_location[1])
        self.watering_can = self.sprite_sheet.get_image(0, 288, 96, 96, 2, config.BG_BLACK)
        self.watering_can_location = [150, 600]
        self.watering_can_item = scene_item.Item( config.ItemID.watering_can, pygame, self.screen, self.watering_can,self.my_rock, self.watering_can_location[0], self.watering_can_location[1])
        self.ball = self.sprite_sheet.get_image(0, 1248, 96, 96, 2, config.BG_BLACK)
        self.ball_location = [300,400]
        self.ball_item = scene_item.Item( config.ItemID.ball,pygame, self.screen, self.ball,self.my_rock, self.ball_location[0], self.ball_location[1])
        self.bed = self.sprite_sheet.get_image(0,480,96,96,6.5,config.BG_BLACK)
        self.bed_location = [875, 295]
        self.bed_item = scene_item.Item(config.ItemID.bed, pygame, self.screen,self.bed,self.my_rock, self.bed_location[0],self.bed_location[1],False)
        self.lamp_table_location = [800, 350]
        self.lamp_table = Table.Table(pygame, self.screen, self.lamp_table_location[0], self.lamp_table_location[1])
        self.full_cup = self.sprite_sheet.get_image(0,864,96,96,2, config.BG_BLACK)
        self.cup_item_location = [150, 400]
        self.full_cup_item = scene_item.Item(config.ItemID.full_cup, pygame, self.screen, self.full_cup, self.my_rock, self.cup_item_location[0], self.cup_item_location[1])

        self.started_game_time = pygame.time.get_ticks()
        self.dirtiness_start = pygame.time.get_ticks()
        self.not_interacted = False
        self.rock_misbehaving_time = 10 #seconds
        self.dirtiness_time = 7
        self.game_over = GameOver(pygame, self.screen, self.my_rock)

        #scaled thought bubble objects
        self.thought_of_watering_can = self.sprite_sheet.get_image(0, 288, 96, 96, 1, config.BG_BLACK)
        self.thought_of_ball = self.sprite_sheet.get_image(2, 288, 96, 96, 1, config.BG_BLACK)
        self.thought_of_full_cup = self.sprite_sheet.get_image(0,864,96,96,1, config.BG_BLACK)

        self.rock_made_a_mess = False
        self.pet_died = False
        self.is_rock_dirty = False
        self.is_hungry = False
        self.is_thirsty = False
        self.is_sad = False

    def draw_thought_bubble(self, screen, pet_rock_location, image): 
        bubble_offset = (0, 50)  # Offset for the first bubble (above the rock)
        bubble_x = pet_rock_location[0] + bubble_offset[0] - self.thought_bubble_radius
        bubble_y = pet_rock_location[1] + bubble_offset[1] - self.thought_bubble_radius

    # Draw the first bubble (above the rock)
        pygame.draw.circle(screen, config.WHITE, (bubble_x + self.thought_bubble_radius, bubble_y + self.thought_bubble_radius), self.thought_bubble_radius//2)

    # Update the bubble_offset for the second bubble (below the first bubble)
        bubble_offset = (0, -50)  
        bubble_x = pet_rock_location[0] + bubble_offset[0] - self.thought_bubble_radius
        bubble_y = pet_rock_location[1] + bubble_offset[1] - self.thought_bubble_radius

    # Draw the second bubble (below the first bubble)
        pygame.draw.circle(screen, config.WHITE, (bubble_x + self.thought_bubble_radius, bubble_y + self.thought_bubble_radius), self.thought_bubble_radius)

    # Draw the broccoli sprite inside the main thought bubble
        item_x = bubble_x + (self.thought_bubble_radius - self.broccoli_item.rect.width // 2)
        item_y = bubble_y + (self.thought_bubble_radius - self.broccoli_item.rect.height // 2)
        screen.blit(image, (item_x, item_y))




    def handle_event(self, is_rock_dirty):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if is_rock_dirty == False:
                self.broccoli_item.handle_event(event,self.broccoli_location, is_rock_dirty)
                self.ball_item.handle_event(event, self.ball_location, is_rock_dirty)
                self.bed_item.handle_event(event, self.bed_location, is_rock_dirty)
                self.full_cup_item.handle_event(event, self.cup_item_location, is_rock_dirty)
                
            self.watering_can_item.handle_event(event, self.watering_can_location, is_rock_dirty)

            if(self.watering_can_item.get_collision_item() == config.ItemID.watering_can):
                self.started_game_time = pygame.time.get_ticks()
                #self.my_rock.set_current_animation(Config.RockActions.idle.value, True)
                self.is_rock_dirty = False
                self.not_interacted = False 
            elif(self.broccoli_item.get_collision_item() == config.ItemID.broccoli):
                self.started_game_time = pygame.time.get_ticks()
                self.pet_stats.fill_hunger()
            elif(self.ball_item.get_collision_item() == config.ItemID.ball):
                self.started_game_time = pygame.time.get_ticks()
                self.pet_stats.fill_happiness()
            elif(self.bed_item.get_collision_item() == config.ItemID.bed):
                self.started_game_time = pygame.time.get_ticks()
                self.pet_stats.fill_health()
            elif(self.full_cup_item.get_collision_item() == config.ItemID.full_cup):
                self.started_game_time = pygame.time.get_ticks()
                self.pet_stats.fill_thirst()
    
    def rock_collide_table(self):
        if self.my_rock.get_location()[0] + self.my_rock.get_current_frame().get_width() >= self.lamp_table.get_location()[0] and self.my_rock.get_location()[0] <= self.lamp_table.get_location()[0] + self.lamp_table.get_current_frame().get_width():
            if self.my_rock.get_location()[1] + self.my_rock.get_current_frame().get_height() >= self.lamp_table.get_location()[1] and self.my_rock.get_location()[1] <= self.lamp_table.get_location()[1] + self.lamp_table.get_current_frame().get_height():
                return True
        return False
    
    def main_frames(self):
        if self.pet_stats.get_pet_health() == 0 and not self.pet_died:
            self.my_rock.set_current_animation(Config.RockActions.dying.value)
            x_location = config.SCREEN_WIDTH // 2 - self.my_rock.get_current_frame().get_width() // 2
            y_location = config.SCREEN_HEIGHT // 2 + self.my_rock.get_current_frame().get_height() // 3
            self.my_rock.set_location(x_location, y_location )
            self.pet_died = True

        if not self.pet_died:
            self.house.draw()
            self.pet_stats_bar_icon.draw()
            self.pet_stats.update()
            self.pet_stats.draw(self.screen)
            
            self.screen.blit(self.my_rock.get_current_frame(), self.my_rock.get_location())
            self.screen.blit(self.watering_can_item.image, self.watering_can_item.rect.topleft)
            self.screen.blit(self.broccoli, self.broccoli_item.rect.topleft)
            self.screen.blit(self.ball, self.ball_item.rect.topleft)
            self.screen.blit(self.bed, self.bed_item.rect.topleft)
            self.screen.blit(self.full_cup,self.full_cup_item.rect.topleft)
            self.screen.blit(self.lamp_table.get_current_frame(), self.lamp_table.get_location())
            self.current_frame = self.my_rock.get_current_frame()
            self.my_rock_rect = self.current_frame.get_rect()
            self.my_rock_rect.topleft = self.my_rock.get_location()
            
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
            
            if self.is_rock_dirty == True:
                self.draw_thought_bubble(self.screen, self.my_rock.get_location(),self.thought_of_watering_can)
            if self.is_rock_dirty == False and self.is_hungry == True:
                self.draw_thought_bubble(self.screen, self.my_rock.get_location(),self.broccoli_item.image)
            if self.is_rock_dirty == False and self.is_hungry == False and self.is_thirsty == True:
                self.draw_thought_bubble(self.screen, self.my_rock.get_location(), self.thought_of_full_cup)
            if self.is_rock_dirty == False and self.is_hungry == False and self.is_thirsty == False and self.is_sad == True:
                self.draw_thought_bubble(self.screen, self.my_rock.get_location(), self.thought_of_ball)


            if (self.not_interacted and not self.is_rock_dirty) and self.my_rock.get_location()[0] < 1100:
                self.my_rock.set_location(self.my_rock.get_location()[0]+30, self.my_rock.get_location()[1])
            elif (self.not_interacted and not self.is_rock_dirty) and self.my_rock.get_location()[0] >= 1100:
                self.my_rock.set_current_animation(Config.RockActions.dirty.value, False)
                self.is_rock_dirty = True
            if not self.is_rock_dirty and self.dirtiness_start + self.dirtiness_time * 1000 < pygame.time.get_ticks():
                self.my_rock.set_current_animation(Config.RockActions.dirty.value, False)
                self.is_rock_dirty = True
                self.dirtiness_start = pygame.time.get_ticks() + (self.dirtiness_time*1000)
            self.my_rock.updated_frame()
            if self.rock_collide_table():
                self.lamp_table.update()
            if not self.is_rock_dirty and self.started_game_time + self.rock_misbehaving_time * 1000 < pygame.time.get_ticks():
                self.my_rock.set_location(600,350)
                self.my_rock.set_current_animation(Config.RockActions.jumping.value, True)
                self.started_game_time = pygame.time.get_ticks() + (self.rock_misbehaving_time*1000)
                self.not_interacted = True
            self.handle_event(self.is_rock_dirty)
            pygame.display.flip()
            
        else:
            self.game_over.main_frames()
        pygame.display.update()