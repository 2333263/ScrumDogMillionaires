from numpy import block
import pygame
from sklearn.linear_model import GammaRegressor
from gameSettings import itemIDs, textureNames, blockSize, craftingTablePos
from CraftButtonHandler import Craft as cr
from TextHandler import Text

class Crafting():
    def __init__(self,  pos, allItems, playerItems, screen):
        self.pos = pos 
        self.allItems = allItems
        self.playerItems = playerItems
        self.screen = screen
        self.menuBackround = pygame.sprite.Group()
        self.currentItem = pygame.sprite.GroupSingle()

        self.leftArrow = Text("<", 35, "white",  "Arial", ((craftingTablePos[0] + blockSize/2) - (blockSize * 5)/2.5, craftingTablePos[1] - blockSize * 5.5))
        self.rightArrow = Text(">", 35, "white",  "Arial", ((craftingTablePos[0] + blockSize/2) + (blockSize * 5)/3, craftingTablePos[1] - blockSize * 5.5))

        self.curr = 1

        self.menuBackround.add(cr(9, ((craftingTablePos[0] + blockSize/2) - (blockSize * 5)/2, craftingTablePos[1] - blockSize * 10), blockSize * 5, blockSize * 10))
        self.menuBackround.add(self.leftArrow)
        self.menuBackround.add(self.rightArrow)
        self.menuBackround.add(Text("CRAFTING", 21, "white",  "Arial", ((craftingTablePos[0] + blockSize/2) - 55, craftingTablePos[1] - blockSize * 9.5)))

        self.currentItem.add(cr(self.curr, ((craftingTablePos[0] + blockSize/2) - 25, craftingTablePos[1] - blockSize * 6), blockSize * 1.8, blockSize * 1.8))

    def setupScreen(self) :
        print()

    def checkClick(self, pos):
        print("clicked")
        for sp in self.menuBackround:
            if (sp.rect.collidepoint(pos)):
                if(sp == self.leftArrow):
                    if(self.curr >= 1):
                        self.curr -= 1
                        self.currentItem.add(cr(self.curr, ((craftingTablePos[0] + blockSize/2) - 25, craftingTablePos[1] - blockSize * 6), blockSize * 1.8, blockSize * 1.8))
                elif(sp == self.rightArrow):
                    if(self.curr <= 8):
                        self.curr += 1    
                        self.currentItem.add(cr(self.curr, ((craftingTablePos[0] + blockSize/2) - 25, craftingTablePos[1] - blockSize * 6), blockSize * 1.8, blockSize * 1.8))
    def makeScreen(self):
        self.menuBackround.draw(self.screen)
        self.currentItem.draw(self.screen)