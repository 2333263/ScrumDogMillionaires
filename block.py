from cgitb import text
import pygame



class Block(pygame.Surface):
    def __init__(self, blockSize, blockPosition,  itemID, textureName):
        super().__init__((blockSize, blockSize))
        self.blockPosition = blockPosition
        self.itemID = itemID
        self.textureName = textureName

 