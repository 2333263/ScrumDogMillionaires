import pygame
from gameSettings import blockSize

class Portal(pygame.sprite.Sprite):
    def __init__(self, blockSize, blockPosition, itemID, textureName, hardness):
        super().__init__()
        self.blockPosition = [blockPosition[0] - 4 * blockSize, blockPosition[1] - 8 * blockSize]
        self.itemID = itemID
        self.textureName = textureName
        self.hardness = hardness
        self.image = pygame.image.load(self.textureName)

        self.rect = self.image.get_rect()
        self.rect.x = blockPosition[0] - 0.4 * blockSize
        self.rect.y = blockPosition[1] -  blockSize

        self.image = pygame.transform.scale(self.image, (blockSize, blockSize))
        
        

    def getHardness(self): 
        return self.hardness