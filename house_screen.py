import pygame
from game_util import PetConfig as Config
from pets import PetRaccoon, PetRock, PetMudskipper
from game_util import PetConfig as config, scene_items as scene_item
from pet_selection import PetSelection
from game_over import GameOver
from game_util.sprite_sheet import SpriteSheet


class HouseScreen:
    def __init__(self, screen):
        self.house_screen = screen

    def draw(self):
        self.house_screen.fill(config.BLACK)
        screen_background = pygame.image.load(config.ROCK_HOUSE_BG_PATH)
        screen_background = pygame.transform.scale(screen_background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.house_screen.blit(screen_background, (0, 0))

class RockHouse:
    def __init__(self):
        self.pygame = pygame.init()


        self.font = config.FONT
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.house = HouseScreen(self.screen)
        self.pet_stats = scene_item.PetStats()
        self.sprite_sheet_img = pygame.image.load('../my_pet/assets/items_sheet.png').convert_alpha() #SpriteSheet('../my_pet/assets/items_sheet.png')
        self.sprite_sheet = SpriteSheet(self.sprite_sheet_img)

        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 100

        self.my_rock = PetRock(pygame, self.screen)
        self.my_rock.set_location(600, 600)
        self.my_rock.set_current_animation(Config.RockActions.jumping.value, True)

        self.broccoli = self.sprite_sheet.get_image(0,384,96,96,1,config.RED)
        self.broccoli_item = scene_item.Item(config.ItemID.broccoli, pygame, self.screen, self.broccoli,self.my_rock, 475, 175)
        self.watering_can = self.sprite_sheet.get_image(0, 288, 96, 96, 2, config.RED)
        self.watering_can_item = scene_item.Item( config.ItemID.watering_can, pygame, self.screen, self.watering_can,self.my_rock, 150, 600)
        self.ball = self.sprite_sheet.get_image(2, 288, 96, 96, 2, config.RED)
        self.ball_item = scene_item.Item( config.ItemID.ball,pygame, self.screen, self.ball,self.my_rock,  300, 300)
        self.bed = self.sprite_sheet.get_image(0,480,96,96,6.5,config.RED)
        self.bed_item = scene_item.Item(config.ItemID.bed, pygame, self.screen,self.bed,self.my_rock, 875,295,False)



        self.game_over = GameOver(pygame, self.screen, self.my_rock)

        self.pet_died = False
        self.running = True
        self.moving = False
        self.clock = pygame.time.Clock()

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            self.watering_can_item.handle_event(event)
            if(self.watering_can_item.get_collision_item() == config.ItemID.watering_can):
                self.pet_stats.fill_thirst()
            self.broccoli_item.handle_event(event)
            if(self.broccoli_item.get_collision_item() == config.ItemID.broccoli):
                self.pet_stats.fill_hunger()
            self.ball_item.handle_event(event)
            if(self.ball_item.get_collision_item() == config.ItemID.ball):
                self.pet_stats.fill_happiness()
            self.bed_item.handle_event(event)
            if(self.bed_item.get_collision_item() == config.ItemID.bed):
                self.pet_stats.fill_health()

    def main_frames(self):
        if self.pet_stats.get_pet_health() == 0 and not self.pet_died:
            self.my_rock.set_current_animation(Config.RockActions.dying.value)
            x_location = config.SCREEN_WIDTH // 2 - self.my_rock.get_current_frame().get_width() // 2
            y_location = config.SCREEN_HEIGHT // 2 + self.my_rock.get_current_frame().get_height() // 3
            self.my_rock.set_location(x_location, y_location )
            self.pet_died = True

        if not self.pet_died:
            self.house.draw()
            self.pet_stats.update()
            self.pet_stats.draw(self.screen)
            self.screen.blit(self.my_rock.get_current_frame(), self.my_rock.get_location())
            self.screen.blit(self.watering_can_item.image, self.watering_can_item.rect.topleft)
            self.screen.blit(self.broccoli, self.broccoli_item.rect.topleft)
            self.screen.blit(self.ball, self.ball_item.rect.topleft)
            self.screen.blit(self.bed, self.bed_item.rect.topleft)
            self.my_rock.updated_frame()

            self.handle_event()
            pygame.display.flip()
            
        else:
            self.game_over.main_frames()
        pygame.display.update()