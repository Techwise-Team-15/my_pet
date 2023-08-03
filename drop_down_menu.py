import pygame
import random

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pet Name Selection")


SCREEN_MAIN = 0
SCREEN_SAVED_NAMES = 1

pet_names = ["Fluffy", "Buddy", "Max", "Charlie", "Luna", "Bella", "Rocky", "Daisy", "Simba", "Milo","Honey"]


def generate_random_name():
    return random.choice(pet_names)

pet_name = generate_random_name()

background_image = pygame.image.load('theme_items/general_background1.png').convert_alpha()
background_image_scale = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

font = pygame.font.Font(None, 30)


screen_center_x = SCREEN_WIDTH // 2
screen_center_y = SCREEN_HEIGHT // 2


dropdown_width = 200
dropdown_height = 30
dropdown_rect = pygame.Rect(screen_center_x - dropdown_width // 2, screen_center_y - 50, dropdown_width, dropdown_height)
dropdown_options_rect = [pygame.Rect(dropdown_rect.x, dropdown_rect.y + (i * dropdown_height), dropdown_width, dropdown_height) for i in range(len(pet_names))]
is_dropdown_open = False


saved_names_file = "saved_names.txt"


saved_names = []
try:
    with open(saved_names_file, "r") as file:
        saved_names = file.read().splitlines()
except FileNotFoundError:
    pass


input_box_width = 200
input_box_height = 30
input_box_rect = pygame.Rect(screen_center_x - input_box_width // 2, screen_center_y + 50, input_box_width, input_box_height)
input_box_active = False
input_box_text = ""
input_box_font = pygame.font.Font(None, 24)


notification_font = pygame.font.Font(None, 20)
show_notification = False
notification_text = ""

current_screen = SCREEN_MAIN
show_save_screen = False  


max_saved_names = 3
delete_button_width = 60
delete_button_height = 30


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
           
            if dropdown_rect.collidepoint(event.pos):
                is_dropdown_open = not is_dropdown_open
            else:
               
                for i, option_rect in enumerate(dropdown_options_rect):
                    if option_rect.collidepoint(event.pos):
                        pet_name = pet_names[i]
                        is_dropdown_open = False  
                      
                        if pet_name not in saved_names:
                            with open(saved_names_file, "a") as file:
                                file.write(pet_name + "\n")
                       
                        show_notification = True
                        notification_text = "Name saved!"

            if current_screen == SCREEN_MAIN:
                
                if save_button_rect.collidepoint(event.pos):
                    show_save_screen = True
                    current_screen = SCREEN_SAVED_NAMES

            elif current_screen == SCREEN_SAVED_NAMES:
               
                if go_back_button_rect.collidepoint(event.pos):
                    show_save_screen = False
                    current_screen = SCREEN_MAIN

                for i, delete_button_rect in enumerate(delete_buttons_rect):
                    if delete_button_rect.collidepoint(event.pos):
                        deleted_name = saved_names.pop(i)
                        with open(saved_names_file, "w") as file:
                            file.write("\n".join(saved_names))
                       
                        show_notification = True
                        notification_text = f"{deleted_name} deleted."
                        break

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                
                show_save_screen = not show_save_screen
                if show_save_screen:
                 
                    input_box_active = False
                    input_box_text = ""

            elif event.key == pygame.K_c:
                
                input_box_active = True
                input_box_text = ""

            elif input_box_active and event.key == pygame.K_RETURN:
              
                if input_box_text.strip() != "":
                    pet_name = input_box_text.strip()
                    is_dropdown_open = False
                    
                    if pet_name not in saved_names:
                        with open(saved_names_file, "a") as file:
                            file.write(pet_name + "\n")
                  
                    show_notification = True
                    notification_text = "Name saved!"
                    input_box_active = False

            elif input_box_active and event.key == pygame.K_ESCAPE:
                
                input_box_active = False

            elif input_box_active and event.key == pygame.K_BACKSPACE:
            
                input_box_text = input_box_text[:-1]

            elif input_box_active:
            
                input_box_text += event.unicode

    screen.blit(background_image_scale, (0, 0))

    if current_screen == SCREEN_MAIN:
       
        pygame.draw.rect(screen, WHITE, dropdown_rect, 2)
        dropdown_text = font.render(pet_name, True, BLACK)
        dropdown_text_rect = dropdown_text.get_rect(center=dropdown_rect.center)
        screen.blit(dropdown_text, dropdown_text_rect)

        choose_text = font.render("Choose Your Pet Name", True, BLACK)
        choose_text_rect = choose_text.get_rect(center=(screen_center_x, dropdown_rect.top - 20))
        screen.blit(choose_text, choose_text_rect)

        if is_dropdown_open:
            for i, option_rect in enumerate(dropdown_options_rect):
                pygame.draw.rect(screen, BLUE, option_rect)
                option_text = font.render(pet_names[i], True, WHITE)
                option_text_rect = option_text.get_rect(center=option_rect.center)
                screen.blit(option_text, option_text_rect)

        save_button_position = (SCREEN_WIDTH // 2 - 50, screen_center_y + 150)
        save_button_rect = pygame.Rect(save_button_position[0], save_button_position[1], 100, 30)
        pygame.draw.rect(screen, BLUE, save_button_rect)
        save_button_text = font.render("Save", True, WHITE)
        save_button_text_rect = save_button_text.get_rect(center=save_button_rect.center)
        screen.blit(save_button_text, save_button_text_rect)

    elif current_screen == SCREEN_SAVED_NAMES:
     
        saved_screen_text = font.render("Saved Pet Names:", True, BLACK)
        screen.blit(saved_screen_text, (screen_center_x - saved_screen_text.get_width() // 2, 50))


        delete_buttons_rect = []
        for i, name in enumerate(saved_names[:max_saved_names]):
            name_text = font.render(name, True, BLACK)
            name_text_rect = name_text.get_rect(center=(screen_center_x, 100 + i * 30))
            screen.blit(name_text, name_text_rect)

            delete_button_position = (name_text_rect.right + 10, name_text_rect.centery - delete_button_height // 2)
            delete_button_rect = pygame.Rect(delete_button_position[0], delete_button_position[1], delete_button_width, delete_button_height)
            pygame.draw.rect(screen, BLUE, delete_button_rect)
            delete_button_text = font.render("Delete", True, WHITE)
            delete_button_text_rect = delete_button_text.get_rect(center=delete_button_rect.center)
            screen.blit(delete_button_text, delete_button_text_rect)

            delete_buttons_rect.append(delete_button_rect)

        go_back_button_position = (SCREEN_WIDTH // 2 - 60, screen_center_y + 150)
        go_back_button_rect = pygame.Rect(go_back_button_position[0], go_back_button_position[1], 120, 30)
        pygame.draw.rect(screen, BLUE, go_back_button_rect)
        go_back_button_text = font.render("Go Back", True, WHITE)
        go_back_button_text_rect = go_back_button_text.get_rect(center=go_back_button_rect.center)
        screen.blit(go_back_button_text, go_back_button_text_rect)

    
    if input_box_active and not show_save_screen:  
        pygame.draw.rect(screen, WHITE, input_box_rect, 2)
        input_box_surface = input_box_font.render(input_box_text, True, BLACK)
        input_box_surface_rect = input_box_surface.get_rect(center=input_box_rect.center)
        screen.blit(input_box_surface, input_box_surface_rect)

        pygame.draw.rect(screen, BLUE, input_box_rect, 2)

      
        custom_name_label = font.render("Enter Custom Name:", True, BLACK)
        custom_name_label_rect = custom_name_label.get_rect(center=(screen_center_x, screen_center_y + 100))
        screen.blit(custom_name_label, custom_name_label_rect)

 
    if show_notification:
        notification_surface = notification_font.render(notification_text, True, BLACK)
        notification_rect = notification_surface.get_rect(center=(screen_center_x, screen_center_y + 100))
        screen.blit(notification_surface, notification_rect)
        show_notification = False 
        pygame.time.set_timer(pygame.USEREVENT, 2000)

    pygame.display.flip()

pygame.quit()













