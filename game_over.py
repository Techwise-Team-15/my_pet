import pygame
from game_config import GameConfig as gc
from game_util import PetConfig as config, scene_items as scene_item



class GameOver():
    def __init__(self,in_pygame,in_screen,game_menu, lost_pet) -> None:
        self.gm = game_menu
        self.screen = in_screen
        self.game_over_pygame = in_pygame
        self.home_button = scene_item.Buttons(self.screen,[50,120],"Menu")
        self.font = config.FONT
        self.player_name = gc.SAVED_PET_NAMES[0] if len(gc.SAVED_PET_NAMES) > 0 else ''
        self.player_board = scene_item.PlayerName(pygame=in_pygame, screen=in_screen, player_name=self.player_name)
        self.score_board = scene_item.Score(pygame=in_pygame, screen=in_screen)
        self.background = self.game_over_pygame.image.load('../my_pet/theme_items/StartBackground.png')
        self.bg = self.game_over_pygame.transform.scale(self.background, [config.SCREEN_WIDTH, config.SCREEN_HEIGHT])
        
        self.last_update = self.game_over_pygame.time.get_ticks()
        self.animation_cooldown = config.PET_ANIMATION_COOLDOWN 
        self.loser_pet = lost_pet 
        
        self.game_over_delay = 10 #seconds to display game over message

        self.set_loser_pet_location()
        
        

    def set_loser_pet_location(self):
        x_location = config.SCREEN_WIDTH/2 - self.loser_pet.get_current_frame().get_width()/2
        y_location = config.SCREEN_HEIGHT/2 + self.loser_pet.get_current_frame().get_height()/3
        self.loser_pet.set_location(x_location, y_location)

    def display_game_over_message(self):
        
        y_offset = config.SCREEN_HEIGHT/2.8
        font = self.game_over_pygame.font.Font(self.font, 100)
        text_surface = font.render("Game Over", True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT/2+y_offset)
        self.screen.blit(text_surface, text_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.home_button.is_mouse_selection(mouse_pos):
                    self.gm.game_music.load_track(config.background_music)
                    self.gm.current_screen = "menu"

    def main_frames(self,score):
        self.game_over_pygame.display.set_caption('Game Over')
        self.score_board.score_value = score
        self.screen.blit(self.bg, (0,0))
        self.home_button.draw()
        self.display_game_over_message()
        self.score_board.draw_score_text()
        if self.player_name != '':
            self.player_board.draw_player_name_text()
        self.screen.blit(self.loser_pet.get_current_frame(), self.loser_pet.get_location())
        self.loser_pet.updated_frame()
        self.game_over_pygame.display.flip()
        self.handle_events()
        #self.game_over_pygame.time.delay(1000 * self.game_over_delay)
        #self.game_over_pygame.quit()
        #quit()

    