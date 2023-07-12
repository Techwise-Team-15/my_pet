import pygame

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
RED = (255, 0, 0)
GREEN = (0, 255, 0)
INDIGO = (75, 0, 130)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

hp_drain_time = 100

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class StatusBar():
    def __init__(self, x, y, w, h, max_hp, color, bg_color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp
        self.color = color
        self.bg_color = bg_color

    def draw(self, surface):
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, self.bg_color, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.w * ratio, self.h))

    def bar_drain(self):
        if self.hp > 0:
            pygame.time.delay(hp_drain_time)
            self.hp -= 1

    #def hp_drain(self):
        #pass

class PetStats():
    health_bar = StatusBar(100, 200, 300, 40, 1000, GREEN, RED)
    thirst_bar = StatusBar(100, 100, 300, 40, 1000, BLUE, RED)
    hunger_bar = StatusBar(100, 300, 300, 40, 1000, YELLOW, RED)

    def draw(self, surface):
        self.health_bar.draw(surface)
        self.thirst_bar.draw(surface)
        self.hunger_bar.draw(surface)

    def update(self):
        self.thirst_bar.bar_drain()
        self.hunger_bar.bar_drain()
        if self.health_bar.hp == 0 or self.thirst_bar.hp == 0:
            self.health_bar.bar_drain()
        elif self.health_bar.hp == 0 and self.thirst_bar.hp == 0:
            self.health_bar.bar_drain()

pet_stats = PetStats()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill(INDIGO)
    pet_stats.update()
    pet_stats.draw(screen)
    pygame.display.flip()

pygame.quit()