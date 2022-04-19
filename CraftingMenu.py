from numpy import block
import pygame
from gameSettings import itemIDs, textureNames, blockSize
from CraftButtonHandler import Craft as cr

class Crafting():
    def __init__(self,  pos, allItems, playerItems, screen):
        self.pos = pos 
        self.allItems = allItems
        self.playerItems = playerItems
        self.screen = screen

    def setupScreen(self) :
        self.menuItems = pygame.sprite.Group()
        for i in range(5):
            butt = cr(i, True, (100 * i/2, 100))
            self.menuItems.add(butt)
        self.menuItems.draw(self.screen)
