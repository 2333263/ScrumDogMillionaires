import pygame

#a class for the block and its attributes

class Block(pygame.sprite.Sprite): #creates a block object with the required properties
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

    def getHardness(self):  #returns the hardness of the block
        return self.hardness



    
 