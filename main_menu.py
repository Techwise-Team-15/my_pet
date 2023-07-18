import pygame
import sys
from game_util import PetConfig as config
from pet_selection import PetSelection
from game_over import GameOver
from pets import PetRaccoon

pygame.init()

background = config.BACKGROUND1
screen_width = config.SCREEN_WIDTH
screen_height = config.SCREEN_HEIGHT
font = config.FONT
screen = pygame.display.set_mode((screen_width, screen_height))
start_img = pygame.image.load('../my_pet/theme_items/start button.png').convert_alpha()


WHITE = config.WHITE
BLACK = config.BLACK

class MenuItem:
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.font_options = pygame.font.Font(font, 50)
        self.rendered_text = self.font_options.render(text, True, WHITE)
        self.rect = self.rendered_text.get_rect(center=pos)

    def is_mouse_selection(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    

class Button():
    def __init__(self, x, y, image):
        self.image = image 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.display.flip()

    def is_mouse_on_button(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)
    

class StartScreen:
    def __init__(self):
        self.start_screen = screen
        start_img_scaled = pygame.transform.scale(start_img, (start_img.get_width()/2, start_img.get_height()/2))# 765X748
        self.start_button = Button(0,0, start_img_scaled) 
        self.start_button.rect.center = (screen_width / 2, (screen_height / 2) + 130)
        
        

    def draw(self):
        self.start_screen.fill(BLACK)
        screen_background = pygame.image.load('../my_pet/theme_items/StartBackground.png')
        screen_background = pygame.transform.scale(screen_background, [screen_width, screen_height])
        self.start_screen.blit(screen_background, (0,0))
        self.start_button.draw()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.is_mouse_on_button():
                return True 

class MainMenu:
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.font_title = pygame.font.Font(font, 80)
        self.title_text = self.font_title.render("Game Main Menu", True, WHITE)
        self.menu_items = [
            MenuItem("Choose Your Pet", (screen_width // 2, screen_height // 2)),
            MenuItem("Load Game", (screen_width // 2, screen_height // 2 + 50)),
            MenuItem("Options", (screen_width // 2, screen_height // 2 + 100)),
            MenuItem("Quit", (screen_width // 2, screen_height // 2 + 150)),
        ]
        self.select_option = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for item in self.menu_items:
                if item.is_mouse_selection(mouse_pos):
                    self.select_option = item.text
                    return
        self.select_option = None
    

    def draw(self):
        self.screen.fill(BLACK)
        screen_background = pygame.image.load(background)
        screen_background = pygame.transform.scale(screen_background, [screen_width, screen_height])
        self.screen.blit(screen_background, (0,0))

        title_text_rect = self.title_text.get_rect(center=(screen_width // 2, screen_height // 4))
        self.screen.blit(self.title_text, title_text_rect)

        for item in self.menu_items:
            self.screen.blit(item.rendered_text, item.rect)

        pygame.display.flip()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pet Patrol")
        self.start_screen = StartScreen()
        self.main_menu = MainMenu()
        self.my_pet_screen = PetSelection(pygame, screen)
        self.my_pet_screen.initialize_pets()
        self.My_Raccoon = PetRaccoon(input_pygame=pygame, screen=screen)
        self.My_Raccoon.set_current_animation(config.RaccoonActions.dying.value)
        x_location = config.SCREEN_WIDTH/2 - self.My_Raccoon.get_current_frame().get_width()/2
        y_location = config.SCREEN_HEIGHT/2 + self.My_Raccoon.get_current_frame().get_height()/3
        self.My_Raccoon.set_location(x_location, y_location)
        self.game_over_screen = GameOver(pygame, screen, self.My_Raccoon)
        self.current_screen = "start"

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.current_screen == "start":
                    transition_to_menu = self.start_screen.handle_event(event)
                    if transition_to_menu:
                        self.current_screen = "menu"

                elif self.current_screen == "menu":
                    self.main_menu.handle_event(event)
                    if self.main_menu.select_option == "Choose Your Pet":
                        self.current_screen = "pet_selection"
                else:
                    self.main_menu.handle_event(event)

            if self.current_screen == "start":
                self.start_screen.draw()
            elif self.current_screen == "menu":
                self.main_menu.draw()
            elif self.current_screen == "pet_selection":
                self.my_pet_screen.main_frames()
                self.my_pet_screen.handle_events()
                #self.game_over_screen.main_frames()
            else:
                self.main_menu.draw()


game = Game()
game.run()