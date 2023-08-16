import pygame
import sys
from game_util import PetConfig as config, MusicPlayer as MP
from pet_selection import PetSelection
from game_over import GameOver
from pets import PetRaccoon, PetRock, PetMudskipper
from house_screen import RockHouse
from raccoon_screen import RaccoonHouse
from load_name import PetNameSelectionApp
from game_config import GameConfig as gc 




pygame.init()
pygame.mixer.init()


background = config.BACKGROUND1
screen_width = config.SCREEN_WIDTH
screen_height = config.SCREEN_HEIGHT
font = config.FONT
screen = pygame.display.set_mode((screen_width, screen_height))
start_img = pygame.image.load('../my_pet/theme_items/start button.png').convert_alpha()

WHITE = config.WHITE

class MenuItem:
    def __init__(self,menu_item_id, text, pos):
        self.menu_item_id = menu_item_id
        self.text = text
        self.pos = pos
        self.font_options = pygame.font.Font(font, 50)
        self.rendered_text = self.font_options.render(text, True, WHITE)
        self.rect = self.rendered_text.get_rect(center=pos)

    def change_text(self, text):
        self.text = text
        self.rendered_text = self.font_options.render(text, True, WHITE)
        self.rect = self.rendered_text.get_rect(center=self.pos)

    def is_mouse_selection(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    

class Button():
    def __init__(self, x, y, image):
        self.image = image 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.display.flip()

    def is_mouse_on_button(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    

class StartScreen:
    def __init__(self):
        self.start_screen = screen
        start_img_scaled = pygame.transform.scale(start_img, (start_img.get_width() // 2, start_img.get_height() // 2))
        self.start_button = Button(0, 0, start_img_scaled) 
        self.start_button.rect.center = (screen_width // 2, (screen_height // 2) + 130)
        
    def draw(self):
        self.start_screen.fill(config.BLACK)
        screen_background = pygame.image.load('../my_pet/theme_items/StartBackground.png')
        screen_background = pygame.transform.scale(screen_background, [screen_width, screen_height])
        self.start_screen.blit(screen_background, (0, 0))
        self.start_button.draw()

    def start_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.start_button.is_mouse_on_button(mouse_pos):
                pygame.time.delay(500)
                return True 

class MainMenu:
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.font_title = pygame.font.Font(font, 80)
        self.title_text = self.font_title.render("Game Main Menu", True, WHITE)
        self.menu_items = [
            MenuItem("pet_select", "Choose Your Pet", (screen_width // 2, screen_height // 2)),
            MenuItem("load_name", "Load Name", (screen_width // 2, screen_height // 2 + 100)),
            MenuItem("sound", "Sound: " + "ON" if gc.IS_SOUND_ON else "OFF", (screen_width // 2, screen_height // 2 + 200)),
            MenuItem("quit", "Quit", (screen_width // 2, screen_height // 2 + 300)),
        ]
        self.select_option = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for item in self.menu_items:
                if item.is_mouse_selection(mouse_pos):
                    self.select_option = item.menu_item_id
                    pygame.time.delay(500)
                    return
        self.select_option = None
    
    def draw(self):
        self.screen.fill(config.BLACK)
        screen_background = pygame.image.load(background)
        screen_background = pygame.transform.scale(screen_background, [screen_width, screen_height])
        self.screen.blit(screen_background, (0, 0))

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
        self.my_rock = PetRock(input_pygame=pygame, screen=screen)
        self.my_raccoon = PetRaccoon(input_pygame=pygame, screen=screen)
        raccoon_x_location = config.SCREEN_WIDTH // 2 - self.my_raccoon.get_current_frame().get_width() // 2
        racccoon_y_location = config.SCREEN_HEIGHT // 2 + self.my_raccoon.get_current_frame().get_height() // 3
        x_location = config.SCREEN_WIDTH // 2 - self.my_rock.get_current_frame().get_width() // 2
        y_location = config.SCREEN_HEIGHT // 2 + self.my_rock.get_current_frame().get_height() // 3
        self.my_raccoon.set_location(raccoon_x_location, racccoon_y_location)
        self.my_rock.set_location(x_location, y_location)
        self.load_name_screen = PetNameSelectionApp(screen)
        self.game_over_screen = GameOver(pygame, screen, self.my_rock)
        self.current_screen = "start"
        self.pet_rock_house = None
        self.pet_raccon_house = None
        #self.background_music = pygame.mixer.Sound('../my_pet/assets/rock_sound_effects/Game_Background_music.mp3')
        #self.background_music.play(-1)
        self.game_music = MP()
        self.game_music.load_track(config.background_music)
        if gc.IS_SOUND_ON:
            self.game_music.play(loop=True)
        else:
            self.game_music.stop()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.current_screen == "start":
                self.start_screen.draw()
                if self.start_screen.start_clicked(event):
                    self.current_screen = "menu"
            elif self.current_screen == "menu":
                self.main_menu.draw()
                self.main_menu.handle_event(event)
                if self.main_menu.select_option == "pet_select":
                    self.current_screen = "pet_selection"
                elif self.main_menu.select_option == "sound":
                    if gc.IS_SOUND_ON:
                        self.game_music.stop()
                        gc.IS_SOUND_ON = False
                        self.main_menu.menu_items[2].change_text("Sound: Off")
                    else:
                        self.game_music.play(loop=True)
                        gc.IS_SOUND_ON = True
                        self.main_menu.menu_items[2].change_text("Sound: On")
                elif self.main_menu.select_option == "load_name":
                    self.current_screen = "load_name"
                elif self.main_menu.select_option == "quit":
                    self.background_music.stop()
                    pygame.quit()
                    sys.exit()
            elif self.current_screen == "pet_selection":
                self.my_pet_screen.main_frames()
                scan_clicked_pet = self.my_pet_screen.handle_events()
                if scan_clicked_pet is not None and scan_clicked_pet.get_pet_id() == self.my_rock.get_pet_id():
                    self.current_screen = "rock_house"
                    self.pet_rock_house = RockHouse(screen, self.game_music)
                if scan_clicked_pet is not None and scan_clicked_pet.get_pet_id() == self.my_raccoon.get_pet_id():
                    self.current_screen = "raccoon_house"
                    self.pet_raccoon_house = RaccoonHouse(screen, self.game_music)
            elif self.current_screen == "rock_house":
                self.pet_rock_house.main_frames() 
            elif self.current_screen== "raccoon_house":
                self.pet_raccoon_house.main_frames()
            elif self.current_screen == "load_name":
                self.load_name_screen.main_frames()
            pygame.display.update()

game = Game()
game.run()