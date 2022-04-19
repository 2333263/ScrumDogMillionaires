from matplotlib.pyplot import text
from numpy import block
import pygame
from gameSettings import itemIDs, textureNames, blockSize
class Craft(pygame.sprite.Sprite):
    def __init__(self, itemID, pos, width, height):
       # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.itemID = itemID
        self.pos = pos

        self.image = pygame.image.load(textureNames[itemIDs[itemID]]).convert()
        self.image = pygame.transform.scale(self.image, (width, height))

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        
