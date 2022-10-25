import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, blockSize, blockPosition, itemID, textureName, hardness, breakTime):
        super().__init__()
        self.blockPosition = blockPosition
        self.itemID = itemID
        self.textureName = textureName
        self.breakTime = breakTime
        self.hardness = hardness
        self.image = pygame.image.load(self.textureName)
        self.image = pygame.transform.scale(self.image, (blockSize, blockSize))
        self.rect = self.image.get_rect()
        self.rect.x = blockPosition[0]
        self.rect.y = blockPosition[1]

    def getHardness(self): 
        return self.hardness



    
 