import pygame
import sys
import game_util
from game_util import PetConfig as config

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
        self.image = start_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        pygame.display.flip()

    def is_mouse_on_button(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.button_rect.collidepoint(mouse_pos)
    

class StartScreen:
    def __init__(self):
        self.screen = screen
        self.start_button = Button(595, 500, start_img) 

    def draw(self):
        self.screen.fill(BLACK)
        screen_background = pygame.image.load('../my_pet/theme_items/StartBackground.png')
        self.screen.blit(screen_background, (0,0))
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

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for item in self.menu_items:
                if item.is_mouse_selection(mouse_pos):
                    self.select_option(item.text)

    def select_option(self, option):
        if option == "Start Game":
            print("Start Game clicked!")
            # Start code goes here

        elif option == "Load Game":
            print("Load Game clicked!")
            # Load game code goes here

        elif option == "Options":
            print("Options clicked!")
            # Options menu code goes here

        elif option == "Quit":
            print("Quit clicked!")
            pygame.quit()
            sys.exit()

    def draw(self):
        self.screen.fill(BLACK)
        screen_background = pygame.image.load(background)
        self.screen.blit(screen_background, (0,0))

        title_text_rect = self.title_text.get_rect(center=(screen_width // 2, screen_height // 4))
        self.screen.blit(self.title_text, title_text_rect)

        for item in self.menu_items:
            self.screen.blit(item.rendered_text, item.rect)

        pygame.display.flip()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pet Game")
        self.start_screen = StartScreen()
        self.main_menu = MainMenu()
        self.show_start_screen = True

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.show_start_screen:
                    transition_to_menu = self.start_screen.handle_event(event)
                    if transition_to_menu:
                        self.show_start_screen = False
                else:
                    self.main_menu.handle_event(event)

            if self.show_start_screen:
                self.start_screen.draw()
            else:
                self.main_menu.draw()


game = Game()
game.run()