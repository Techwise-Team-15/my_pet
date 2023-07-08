# -*- coding: utf-8 -*-
"""

@author: donny
"""

import pygame
import sys

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pet Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font_title = pygame.font.Font(None, 80)
font_options = pygame.font.Font(None, 50)


class MenuItem:
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.rendered_text = font_options.render(text, True, WHITE)
        self.rect = self.rendered_text.get_rect(center=pos)

    def is_mouse_selection(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class StartScreen:
    def __init__(self):
        self.title_text = font_title.render("Pet Game", True, WHITE)
        self.start_button = MenuItem("Play", (screen_width // 2, screen_height // 2 + 100))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.start_button.is_mouse_selection(mouse_pos):
                return True  # Return True to indicate transition to the main menu

    def draw(self):
        screen.fill(BLACK)

        title_text_rect = self.title_text.get_rect(center=(screen_width // 2, screen_height // 4))
        screen.blit(self.title_text, title_text_rect)

        screen.blit(self.start_button.rendered_text, self.start_button.rect)

        pygame.display.flip()


class MainMenu:
    def __init__(self):
        self.title_text = font_title.render("Game Main Menu", True, WHITE)
        self.menu_items = [
            MenuItem("Start Game", (screen_width // 2, screen_height // 2)),
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
        screen.fill(BLACK)

        title_text_rect = self.title_text.get_rect(center=(screen_width // 2, screen_height // 4))
        screen.blit(self.title_text, title_text_rect)

        for item in self.menu_items:
            screen.blit(item.rendered_text, item.rect)

        pygame.display.flip()


class Game:
    def __init__(self):
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