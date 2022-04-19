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
        self.menuItems = pygame.sprite.Group()

    def setupScreen(self) :
        shelf = blockSize
        xc = 100
        for i in range(8):
            if( i == 4):
                shelf = blockSize * 2
                xc = 100

            xc += blockSize
            butt = cr(i, (xc , shelf))
            self.menuItems.add(butt)

    def checkClick(self, pos):
        for sp in self.menuItems:
            if (sp.rect.collidepoint(pos)):
                self.menuItems.remove(sp)

    def makeScreen(self):
        self.menuItems.draw(self.screen)