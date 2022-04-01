import pygame
from game_settings import block_size
class Block(pygame.Surface):
    def __init__(self, blockSize, blockPosition, itemID, textureName):
        super().__init__((blockSize, blockSize))
        self.blockPosition = blockPosition
        self.itemID = itemID
        self.textureName = textureName
        self.Image = pygame.image.load("Tiles/" + self.textureName)
        self.Image = pygame.transform.scale(self.Image, (block_size, block_size))


 