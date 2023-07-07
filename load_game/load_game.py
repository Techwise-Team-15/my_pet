import pygame 

pygame.init()
#basic setup
background_color = (131,231,255)
background = pygame.image.load('background_exp.PNG')
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption('Saved Pets')
font = pygame.font.Font('Starborn.ttf', 84)
font2 = pygame.font.Font('Starborn.ttf', 40)
text1 = font.render('Saved Pets', True, (0, 0, 0))
textRect1 = text1.get_rect()
textRect1.center = (960, 100)
text2 = font2.render('(If empty, there is no saved pets)', True, (0, 0, 0))
textRect2 = text2.get_rect()
textRect2.center = (960, 175)


#file opening
file1 = open("first_pet.txt","r")
check1 = file1.read(1)
pet_sum1 = file1.readlines()

file2 = open("second_pet.txt","r")
check2 = file2.read(1)
pet_sum2 = file2.readlines()

file3 = open("third_pet.txt","r")
check3 = file3.read(1)
pet_sum3 = file3.readlines()


file1.close()
file2.close()
file3.close()

content = 0
def is_progress (content):
    if content != 0:
        return True
    else:
        return False

slot1 = is_progress(check1)
slot2 = is_progress(check2)
slot3 = is_progress(check3)

stars1 = int(pet_sum1[2])
stars2 = int(pet_sum2[2])
stars3 = int(pet_sum3[2])

if slot1 == True:
    
    pet1 = font2.render(check1 + pet_sum1[0], True, (0, 0, 0))
    petRect1 = pet1.get_rect()
    petRect1.center = (1280, 316)
    if stars1 <= 10:
        pet_stars1 = font2.render('a', True, (0, 0, 0))
    elif stars1 <= 50:
        pet_stars1 = font2.render('aa', True, (0, 0, 0))
    elif stars1 <= 70:
        pet_stars1 = font2.render('aaa', True, (0, 0, 0))
    elif stars1 <= 80:
        pet_stars1 = font2.render('aaaa', True, (0, 0, 0))
    else:
        pet_stars1 = font2.render('aaaaa', True, (0, 0, 0))

    pet_starsRect1 = pet_stars1.get_rect()
    pet_starsRect1.center = (1280, 416)
    

        

if slot2 == True:
    pet2 = font2.render(check2 + pet_sum2[0], True, (0, 0, 0))
    petRect2 = pet2.get_rect()
    petRect2.center = (1280, 550)
    if stars2 <= 10:
        pet_stars2 = font2.render('a', True, (0, 0, 0))
    elif stars2 <= 50:
        pet_stars2 = font2.render('aa', True, (0, 0, 0))
    elif stars2 <= 70:
        pet_stars2 = font2.render('aaa', True, (0, 0, 0))
    elif stars2 <= 80:
        pet_stars2 = font2.render('aaaa', True, (0, 0, 0))
    else:
        pet_stars2 = font2.render('aaaaa', True, (0, 0, 0))

    pet_starsRect2 = pet_stars2.get_rect()
    pet_starsRect2.center = (1280, 650)
        

if slot3 == True:
    pet3 = font2.render(check3 + pet_sum3[0], True, (0, 0, 0))
    petRect3 = pet3.get_rect()
    petRect3.center = (1280, 830)
    if stars3 <= 10:
        pet_stars3 = font2.render('a', True, (0, 0, 0))
    elif stars3 <= 50:
        pet_stars3 = font2.render('aa', True, (0, 0, 0))
    elif stars3 <= 70:
        pet_stars3 = font2.render('aaa', True, (0, 0, 0))
    elif stars3 <= 80:
        pet_stars3 = font2.render('aaaa', True, (0, 0, 0))
    else:
        pet_stars3 = font2.render('aaaaa', True, (0, 0, 0))

    pet_starsRect3 = pet_stars3.get_rect()
    pet_starsRect3.center = (1280, 930)
    

    #add stars for health
    #figure out file system


while True:
    screen.fill(background_color)
    screen.blit(background, (0,0))
    screen.blit(text1, textRect1)
    screen.blit(text2, textRect2)
    screen.blit(pet1, petRect1)
    screen.blit(pet_stars1, pet_starsRect1)
    screen.blit(pet2, petRect2)
    screen.blit(pet_stars2, pet_starsRect2)
    screen.blit(pet3, petRect3)
    screen.blit(pet_stars3, pet_starsRect3)
        


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        pygame.display.update()