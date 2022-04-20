import pygame
from gameSettings import itemIDs, textureNames, blockSize, craftingTablePos, req
from CraftButtonHandler import Craft as cr
from TextHandler import Text
from inventoryHandler import getInventoryItems
from item import Item

class Crafting():
    def __init__(self, allItems, playerItems, screen):
        self.allItems = allItems
        self.playerItems = playerItems
        self.screen = screen
        self.menuBackround = pygame.sprite.Group()
        self.currentItem = pygame.sprite.GroupSingle()
        self.currentRequirements = pygame.sprite.GroupSingle()

        self.leftArrow = Text("<", 35, "white",  "Arial", ((craftingTablePos[0] + blockSize/2) - (blockSize * 5)/2.5, craftingTablePos[1] - blockSize * 5.5))
        self.rightArrow = Text(">", 35, "white",  "Arial", ((craftingTablePos[0] + blockSize/2) + (blockSize * 5)/3, craftingTablePos[1] - blockSize * 5.5))

        self.curr = 1

        self.menuBackround.add(cr(9, ((craftingTablePos[0] + blockSize/2) - (blockSize * 5)/2, craftingTablePos[1] - blockSize * 10), blockSize * 5, blockSize * 10))
        self.menuBackround.add(self.leftArrow)
        self.menuBackround.add(self.rightArrow)
        self.menuBackround.add(Text("CRAFTING", 21, "white",  "Arial", ((craftingTablePos[0] + blockSize/2) - 55, craftingTablePos[1] - blockSize * 9.5)))

        self.currentRequirements.add(self.getRequirements(""))
       
        #self.currentItem.add(cr(self.curr, ((craftingTablePos[0] + blockSize/2) - blockSize/1.2, craftingTablePos[1] - blockSize * 6), blockSize * 1.8, blockSize * 1.8))


    def checkClick(self, pos):
        for sp in self.menuBackround:
            if (sp.rect.collidepoint(pos)):
                if(sp == self.leftArrow):
                    if(self.curr >= 1):
                        self.curr -= 1
                        self.currentItem.add(cr(self.curr, ((craftingTablePos[0] + blockSize/2) - blockSize/1.2, craftingTablePos[1] - blockSize * 6), blockSize * 1.8, blockSize * 1.8))
                elif(sp == self.rightArrow):
                    if(self.curr <= 7):
                        self.curr += 1    
                        self.currentItem.add(cr(self.curr, ((craftingTablePos[0] + blockSize/2) - blockSize/1.2, craftingTablePos[1] - blockSize * 6), blockSize * 1.8, blockSize * 1.8))
    
    #Takes in the current item and the player inventory and checks if the player has enough items
    def isCraftable(self, item, playerItems):
        for resource in playerItems:
            if(resource.itemName == item.itemName):
                if (resource.amount >= item.amount):
                    return True
        return False

    def getRequirements(self, item):
        textItems = pygame.sprite.Group()
        ps = 1
        for resource in req:
            textItems.add(Text(itemIDs[resource] + " : " + str(req[resource]), 16, "white", "Mc", ((craftingTablePos[0] + blockSize/2) - blockSize/1.2, craftingTablePos[1] - blockSize * 5)))
            ps+= 2
        return textItems

    def makeScreen(self):
        self.menuBackround.draw(self.screen)
        self.currentItem.draw(self.screen)
        self.currentRequirements.draw(self.screen)