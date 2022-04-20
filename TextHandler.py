import pygame
from gameSettings import blockSize
pygame.font.init()

class Text(pygame.sprite.Sprite):
    def __init__(self, text, fontSize, color, font, pos):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        my_font = pygame.font.Font("Minecraft.ttf", fontSize)  
        self.image = my_font.render(text, True, color)

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        