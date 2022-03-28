import pygame



class Block(pygame.Surface):
    def __init__(self, blockSize, blockPosition, blockColour):
        super().__init__((blockSize, blockSize))
        self.blockPosition = blockPosition

        ### FOR INVENTORY USE
        ### IF WE CHANGE FROM COLOURS CHANGE THIS TOO
        self.blockColour = blockColour
        ###

        self.fill(blockColour)
