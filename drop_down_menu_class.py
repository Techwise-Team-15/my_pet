import pygame
import random

class PetNameSelectionApp:
    def __init__(self):
        pygame.init()

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Pet Name Selection")

        self.SCREEN_MAIN = 0
        self.SCREEN_SAVED_NAMES = 1

        self.pet_names = ["Fluffy", "Buddy", "Max", "Charlie", "Luna", "Bella", "Rocky", "Daisy", "Simba", "Milo", "Honey"]
        self.pet_name = self.generate_random_name()

        self.background_image = pygame.image.load('theme_items/general_background1.png').convert_alpha()
        self.background_image_scale = pygame.transform.scale(self.background_image, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 255)

        self.font = pygame.font.Font(None, 30)
        self.input_box_font = pygame.font.Font(None, 24)
        self.notification_font = pygame.font.Font(None, 20)

        self.screen_center_x = self.SCREEN_WIDTH // 2
        self.screen_center_y = self.SCREEN_HEIGHT // 2

        self.dropdown_width = 200
        self.dropdown_height = 30
        self.dropdown_rect = pygame.Rect(self.screen_center_x - self.dropdown_width // 2, self.screen_center_y - 50, self.dropdown_width, self.dropdown_height)
        self.dropdown_options_rect = [pygame.Rect(self.dropdown_rect.x, self.dropdown_rect.y + (i * self.dropdown_height), self.dropdown_width, self.dropdown_height) for i in range(len(self.pet_names))]
        self.is_dropdown_open = False

        self.saved_names_file = "saved_names.txt"
        self.saved_names = self.load_saved_names()

        self.input_box_width = 200
        self.input_box_height = 30
        self.input_box_rect = pygame.Rect(self.screen_center_x - self.input_box_width // 2, self.screen_center_y + 50, self.input_box_width, self.input_box_height)
        self.input_box_active = False
        self.input_box_text = ""

        self.show_notification = False
        self.notification_text = ""

        self.current_screen = self.SCREEN_MAIN
        self.show_save_screen = False

        self.max_saved_names = 3

        self.delete_button_width = 60
        self.delete_button_height = 30
        self.delete_buttons_rect = []

        self.running = True

    def generate_random_name(self):
        return random.choice(self.pet_names)

    def load_saved_names(self):
        try:
            with open(self.saved_names_file, "r") as file:
                return file.read().splitlines()
        except FileNotFoundError:
            return []

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_mouse_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                self.handle_key_down(event.key)

    def handle_mouse_click(self, mouse_pos):
        if self.current_screen == self.SCREEN_MAIN:
            if self.dropdown_rect.collidepoint(mouse_pos):
                self.is_dropdown_open = not self.is_dropdown_open
            else:
                for i, option_rect in enumerate(self.dropdown_options_rect):
                    if option_rect.collidepoint(mouse_pos):
                        self.handle_pet_name_selection(i)
                if self.save_button_rect.collidepoint(mouse_pos):
                    self.show_save_screen = True
                    self.current_screen = self.SCREEN_SAVED_NAMES
        elif self.current_screen == self.SCREEN_SAVED_NAMES:
            if self.go_back_button_rect.collidepoint(mouse_pos):
                self.show_save_screen = False
                self.current_screen = self.SCREEN_MAIN
            for i, delete_button_rect in enumerate(self.delete_buttons_rect):
                if delete_button_rect.collidepoint(mouse_pos):
                    self.handle_delete_saved_name(i)

    def handle_pet_name_selection(self, index):
        self.pet_name = self.pet_names[index]
        self.is_dropdown_open = False
        if self.pet_name not in self.saved_names:
            with open(self.saved_names_file, "a") as file:
                file.write(self.pet_name + "\n")
            self.show_notification = True
            self.notification_text = "Name saved!"

    def handle_delete_saved_name(self, index):
        deleted_name = self.saved_names.pop(index)
        with open(self.saved_names_file, "w") as file:
            file.write("\n".join(self.saved_names))
        self.show_notification = True
        self.notification_text = f"{deleted_name} deleted."

    def handle_key_down(self, key):
        if key == pygame.K_s:
            self.show_save_screen = not self.show_save_screen
            if self.show_save_screen:
                self.input_box_active = False
                self.input_box_text = ""
        elif key == pygame.K_c:
            self.input_box_active = True
            self.input_box_text = ""
        elif self.input_box_active and key == pygame.K_RETURN:
            self.handle_input_box_return()
        elif self.input_box_active and key == pygame.K_ESCAPE:
            self.input_box_active = False
        elif self.input_box_active and key == pygame.K_BACKSPACE:
            self.input_box_text = self.input_box_text[:-1]
        elif self.input_box_active:
            self.input_box_text += pygame.key.name(key)

    def handle_input_box_return(self):
        if self.input_box_text.strip() != "":
            pet_name = self.input_box_text.strip()
            self.handle_pet_name_selection(len(self.pet_names))  # Add the new custom name
            self.input_box_active = False

    def handle_dropdown_options_hover(self):
        for i, option_rect in enumerate(self.dropdown_options_rect):
            if option_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, (0, 0, 150), option_rect)

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.flip()

        pygame.quit()

    def draw(self):
        self.screen.blit(self.background_image_scale, (0, 0))

        if self.current_screen == self.SCREEN_MAIN:
            pygame.draw.rect(self.screen, self.WHITE, self.dropdown_rect, 2)
            dropdown_text = self.font.render(self.pet_name, True, self.BLACK)
            dropdown_text_rect = dropdown_text.get_rect(center=self.dropdown_rect.center)
            self.screen.blit(dropdown_text, dropdown_text_rect)

            choose_text = self.font.render("Choose Your Pet Name", True, self.BLACK)
            choose_text_rect = choose_text.get_rect(center=(self.screen_center_x, self.dropdown_rect.top - 20))
            self.screen.blit(choose_text, choose_text_rect)

            if self.is_dropdown_open:
                for i, option_rect in enumerate(self.dropdown_options_rect):
                    pygame.draw.rect(self.screen, self.BLUE, option_rect)
                    option_text = self.font.render(self.pet_names[i], True, self.WHITE)
                    option_text_rect = option_text.get_rect(center=option_rect.center)
                    self.screen.blit(option_text, option_text_rect)

            self.save_button_rect = pygame.Rect(self.SCREEN_WIDTH // 2 - 50, self.screen_center_y + 150, 100, 30)
            pygame.draw.rect(self.screen, self.BLUE, self.save_button_rect)
            save_button_text = self.font.render("Save", True, self.WHITE)
            save_button_text_rect = save_button_text.get_rect(center=self.save_button_rect.center)
            self.screen.blit(save_button_text, save_button_text_rect)

        elif self.current_screen == self.SCREEN_SAVED_NAMES:
            saved_screen_text = self.font.render("Saved Pet Names:", True, self.BLACK)
            self.screen.blit(saved_screen_text, (self.screen_center_x - saved_screen_text.get_width() // 2, 50))

            self.delete_buttons_rect = []
            for i, name in enumerate(self.saved_names[:self.max_saved_names]):
                name_text = self.font.render(name, True, self.BLACK)
                name_text_rect = name_text.get_rect(center=(self.screen_center_x, 100 + i * 30))
                self.screen.blit(name_text, name_text_rect)

                delete_button_position = (name_text_rect.right + 10, name_text_rect.centery - self.delete_button_height // 2)
                delete_button_rect = pygame.Rect(delete_button_position[0], delete_button_position[1], self.delete_button_width, self.delete_button_height)
                pygame.draw.rect(self.screen, self.BLUE, delete_button_rect)
                delete_button_text = self.font.render("Delete", True, self.WHITE)
                delete_button_text_rect = delete_button_text.get_rect(center=delete_button_rect.center)
                self.screen.blit(delete_button_text, delete_button_text_rect)

                self.delete_buttons_rect.append(delete_button_rect)

            go_back_button_position = (self.SCREEN_WIDTH // 2 - 60, self.screen_center_y + 150)
            self.go_back_button_rect = pygame.Rect(go_back_button_position[0], go_back_button_position[1], 120, 30)
            pygame.draw.rect(self.screen, self.BLUE, self.go_back_button_rect)
            go_back_button_text = self.font.render("Go Back", True, self.WHITE)
            go_back_button_text_rect = go_back_button_text.get_rect(center=self.go_back_button_rect.center)
            self.screen.blit(go_back_button_text, go_back_button_text_rect)

        if self.input_box_active and not self.show_save_screen:
            pygame.draw.rect(self.screen, self.WHITE, self.input_box_rect, 2)
            input_box_surface = self.input_box_font.render(self.input_box_text, True, self.BLACK)
            input_box_surface_rect = input_box_surface.get_rect(center=self.input_box_rect.center)
            self.screen.blit(input_box_surface, input_box_surface_rect)

            pygame.draw.rect(self.screen, self.BLUE, self.input_box_rect, 2)

            custom_name_label = self.font.render("Enter Custom Name:", True, self.BLACK)
            custom_name_label_rect = custom_name_label.get_rect(center=(self.screen_center_x, self.screen_center_y + 100))
            self.screen.blit(custom_name_label, custom_name_label_rect)

        if self.show_notification:
            notification_surface = self.notification_font.render(self.notification_text, True, self.BLACK)
            notification_rect = notification_surface.get_rect(center=(self.screen_center_x, self.screen_center_y + 100))
            self.screen.blit(notification_surface, notification_rect)
            self.show_notification = False
            pygame.time.set_timer(pygame.USEREVENT, 2000)


if __name__ == "__main__":
    app = PetNameSelectionApp()
    app.run()


