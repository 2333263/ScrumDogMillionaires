import pygame
import math
import game_settings as gs

class Block(pygame.Surface):
    def __init__(self, blockSize, blockPosition, blockColour):
        super().__init__((blockSize, blockSize))
        self.blockPosition = blockPosition
        self.fill(blockColour)