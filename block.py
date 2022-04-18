import pygame
from gameSettings import blockSize
class Block(pygame.Surface):
    def __init__(self, blockSize, blockPosition, itemID, textureName):
        super().__init__((blockSize, blockSize))
        self.blockPosition = blockPosition
        self.itemID = itemID
        self.textureName = textureName
        self.Image = pygame.image.load("Textures/Blocks/" + self.textureName)
        self.Image = pygame.transform.scale(self.Image, (blockSize, blockSize))


 