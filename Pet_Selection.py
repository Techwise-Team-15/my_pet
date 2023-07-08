import pygame

from Pets.Pet_Raccoon import Pet_Raccoon
from Pets.Pet_Rock import Pet_Rock
from Pets.Pet_Mudskipper import Pet_Mudskipper

import Config

pygame.init()

screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
pygame.display.set_caption('SpriteSheets')

My_Raccoon = Pet_Raccoon(input_pygame= pygame, screen=screen)
# My_Raccoon.animation(action=Config.RaccoonActions.walking.value)

My_Rock = Pet_Rock(input_pygame= pygame, screen=screen)
# My_Rock.animation(action=Config.RockActions.clean.value)

My_Mudskipper = Pet_Mudskipper(input_pygame= pygame, screen=screen)
# My_Mudskipper.animation(action=Config.MudskipperActions.walking.value)


"""
sprite_sheet_images = [
    pygame.image.load('../Sprites/racoonpet.png').convert_alpha(),
    pygame.image.load('../Sprites/rockpet.png').convert_alpha(),
    pygame.image.load('../Sprites/petmudskipper.png').convert_alpha()
]

sprite_sheets = [
    spritesheet.SpiteSheet(sprite_sheet_images[0]),
    spritesheet.SpiteSheet(sprite_sheet_images[1]),
    spritesheet.SpiteSheet(sprite_sheet_images[2])
]

animation_lists = [[] for _ in range(3)] 
animation_steps = 3
animation_cooldown = 100


for sheet_index, sprite_sheet in enumerate(sprite_sheets):
    for x in range(animation_steps):
        for _ in range(animation_steps):
            animation_lists[sheet_index].append(sprite_sheet.get_image(x, 96, 96, 2, BLACK))


frames = [0, 0, 0]
last_update = [pygame.time.get_ticks() for _ in range(3)]

run = True
while run:
    screen.fill(BG)

    current_time = pygame.time.get_ticks()


    for sheet_index in range(3):
        if current_time - last_update[sheet_index] >= animation_cooldown:
            frames[sheet_index] += 1
            last_update[sheet_index] = current_time
            if frames[sheet_index] >= len(animation_lists[sheet_index]):
                frames[sheet_index] = 0

        screen.blit(animation_lists[sheet_index][frames[sheet_index]], (100 + sheet_index * 250, 150))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
"""
