import pygame
from game_util import PetConfig as Config
from pets import PetRaccoon, PetRock, PetMudskipper
from assets import Table

pygame.init()

background = Config.BACKGROUND1
screen_width = Config.SCREEN_WIDTH
screen_height = Config.SCREEN_HEIGHT
font = Config.FONT
screen = pygame.display.set_mode((screen_width, screen_height))
start_img = pygame.image.load('../my_pet/theme_items/start button.png').convert_alpha()

WHITE = Config.WHITE
BLACK = Config.BLACK

class PetSelection:
    def __init__(self, screen_width, screen_height):
        self.pet_pygame = pygame
        self.pet_pygame.init()
        self.screen = self.pet_pygame.display.set_mode((screen_width, screen_height))
        self.background = self.pet_pygame.image.load('../my_pet/load_game/background_exp.PNG')
        self.bg = self.pet_pygame.transform.scale(self.background, [screen_width, screen_height])
        self.pet_pygame.display.set_caption('SpriteSheets')
        self.last_update = self.pet_pygame.time.get_ticks()
        self.animation_cooldown = 100
        self.run = False

    def create_pet_screen(self, action):
        # Create the raccoon
        My_Raccoon = PetRaccoon(input_pygame=self.pet_pygame, screen=self.screen)
        My_Raccoon.set_current_animation(action)
        My_Raccoon.set_location(100, 400)

        # Create the rock
        My_rock = PetRock(input_pygame=self.pet_pygame, screen=self.screen)
        My_rock.set_location(600, 600)
        My_rock.set_current_animation(action)

        # Create the mudskipper
        My_mudskipper = PetMudskipper(input_pygame=self.pet_pygame, screen=self.screen)
        My_mudskipper.set_current_animation(action)
        My_mudskipper.set_location(1100, 400)

        self.run = True

        while self.run:
            for event in self.pet_pygame.event.get():
                if event.type == self.pet_pygame.QUIT:
                    self.run = False

            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(My_rock.get_current_frame(), My_rock.get_location())
            My_rock.updated_frame()
            self.screen.blit(My_Raccoon.get_current_frame(), My_Raccoon.get_location())
            My_Raccoon.updated_frame()
            self.screen.blit(My_mudskipper.get_current_frame(), My_mudskipper.get_location())
            My_mudskipper.updated_frame()

            self.pet_pygame.display.update()

        self.pet_pygame.quit()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))


class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.start_button = Button(595, 500, start_img)
        self.screen_background = pygame.image.load('../my_pet/theme_items/StartBackground.png')

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.screen_background, (0, 0))
        self.start_button.draw()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.is_mouse_on_button():
                return True


class MainMenu:
    def __init__(self):
        self.font_title = pygame.font.Font(font, 80)
        self.title_text = self.font_title.render("Game Main Menu", True, WHITE)
        self.menu_items = [
            MenuItem("Choose Your Pet", (screen_width // 2, screen_height // 2)),
            MenuItem("Load Game", (screen_width // 2, screen_height // 2 + 50)),
            MenuItem("Options", (screen_width // 2, screen_height // 2 + 100)),
            MenuItem("Quit", (screen_width // 2, screen_height // 2 + 150)),
        ]
        self.selected_option = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for item in self.menu_items:
                if item.is_mouse_selection(mouse_pos):
                    self.selected_option = item.text
                    return
        self.selected_option = None

class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.display.flip()

    def is_mouse_on_button(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)


class MenuItem:
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.font_options = pygame.font.Font(font, 50)
        self.rendered_text = self.font_options.render(text, True, WHITE)
        self.rect = self.rendered_text.get_rect(center=pos)

    def is_mouse_selection(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.start_screen = StartScreen(self.screen)
        self.main_menu = MainMenu()
        self.pet_selection = PetSelection(screen_width, screen_height)
        self.current_screen = "start_screen"

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.current_screen == "start_screen":
                    transition_to_menu = self.start_screen.handle_event(event)
                    if transition_to_menu:
                        self.current_screen = "main_menu"

                elif self.current_screen == "main_menu":
                    self.main_menu.handle_event(event)
                    if self.main_menu.selected_option == "Choose Your Pet":
                        self.current_screen = "pet_selection"

            if self.current_screen == "start_screen":
                self.start_screen.draw()
            elif self.current_screen == "main_menu":
                self.draw_main_menu()
            elif self.current_screen == "pet_selection":
                self.pet_selection.create_pet_screen(Config.RaccoonActions.walking.value)
                self.current_screen = "start_screen"

    def draw_main_menu(self):
        self.screen.fill(BLACK)
        screen_background = pygame.image.load(background)
        self.screen.blit(screen_background, (0, 0))

        title_text_rect = self.main_menu.title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        self.screen.blit(self.main_menu.title_text, title_text_rect)

        for item in self.main_menu.menu_items:
            self.screen.blit(item.rendered_text, item.rect)

        pygame.display.flip()


game = Game(screen_width, screen_height)
game.run()