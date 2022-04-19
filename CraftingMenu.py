from numpy import block
import pygame
from gameSettings import itemIDs, textureNames, blockSize

class Crafting(pygame.sprite.Sprite):
    def __init__(self,  pos, allItems, playerItems, screen):
       # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        img = pygame.image.load('Textures/Tools/wooden_pickaxe.png')
        img.convert()
        img = pygame.transform.scale(img, (blockSize, blockSize))
        
        self.rect = img.get_rect()
        self.rect.center = 400, 400
        pygame.draw.rect(img, "red", [10, 10, blockSize + 10, blockSize + 10], 10)
        
        screen.blit(img, self.rect)