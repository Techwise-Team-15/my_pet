import pygame
from .pet_config import PetConfig as config

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image
    
    def get_image(self, frame, animationHeight, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0,0), ((frame * width),animationHeight, width, height))
        image = pygame.transform.scale(image, (width* scale, height* scale))
        image.set_colorkey(color)

        return image
    
    def get_image_mask(self):
        img_mask = pygame.mask.from_surface(self.sheet)
        mask_sheet = img_mask.to_surface()

        return mask_sheet
    
    def get_flipped_image(self,frame_to_blit):
        frame_to_blit = pygame.transform.flip(frame_to_blit, True, False)
        frame_to_blit.set_colorkey(config.BG_BLACK)
        return frame_to_blit