from matplotlib.pyplot import text
from numpy import block
import pygame
from gameSettings import itemIDs, textureNames, blockSize
class Craft(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, itemID, isCraftable, pos):
       # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(textureNames[itemIDs[itemID]]).convert()
        self.image = pygame.transform.scale(self.image, (blockSize, blockSize))

        self.rect = self.image.get_rect()

        

        self.rect.x = pos[0]
        self.rect.y = pos[1]
        #self.rect = pygame.Rect(pos[0], pos[1], 100, 100)
