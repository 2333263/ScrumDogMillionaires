import pygame


import pygame

class Block(pygame.Surface):
    def __init__(self, blockSize, blockPosition, blockColour):
        super().__init__((blockSize, blockSize))
        self.blockPosition = blockPosition
        self.fill(blockColour)