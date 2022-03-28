import pygame



class Block(pygame.Surface):
    def __init__(self, blockSize, blockPosition, blockColour, itemID, textureName = ""):
        super().__init__((blockSize, blockSize))
        self.blockPosition = blockPosition
        self.itemID = itemID
        self.textureName = textureName
        ### FOR INVENTORY USE
        ### IF WE CHANGE FROM COLOURS CHANGE THIS TOO
        self.blockColour = blockColour
        ###

        self.fill(blockColour)
