from turtle import back
import pygame
pygame.font.init()

class Text(pygame.sprite.Sprite):
    def __init__(self, text, fontSize, color, pos, background = None):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
       
        my_font = pygame.font.Font("Minecraft.ttf", fontSize)
        self.words = text
        self.image = my_font.render(self.words, True, color, background)

        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        