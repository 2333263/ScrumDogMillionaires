from numpy import block
import pygame
from sklearn.linear_model import GammaRegressor
from gameSettings import itemIDs, textureNames, blockSize, craftingTablePos
from CraftButtonHandler import Craft as cr

class Crafting():
    def __init__(self,  pos, allItems, playerItems, screen):
        self.pos = pos 
        self.allItems = allItems
        self.playerItems = playerItems
        self.screen = screen
        self.menuItems = pygame.sprite.Group()
        
        self.menuItems.add(cr(9, ((craftingTablePos[0] + blockSize/2) - (blockSize * 5)/2, craftingTablePos[1] - blockSize * 10), blockSize * 5, blockSize * 10))
       
    def setupScreen(self) :
        shelf = craftingTablePos[1] - blockSize * 10
        xc = (craftingTablePos[0] + blockSize/2) - (blockSize * 5)/2
        for i in range(8):
            if((i + 1) % 3 == 0):
                shelf = craftingTablePos[1] - blockSize * 9 + 10
                xc = (craftingTablePos[0] + blockSize/2) - (blockSize * 5)/2

            xc += blockSize + 10
            
            butt = cr(i, (xc , shelf), blockSize, blockSize)
            self.menuItems.add(butt)

    def checkClick(self, pos):
        for sp in self.menuItems:
            if (sp.rect.collidepoint(pos)):
                print()

    def makeScreen(self):
        self.menuItems.draw(self.screen)