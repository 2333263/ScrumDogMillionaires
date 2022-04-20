import pygame
from gameSettings import itemIDs, textureNames, blockSize, craftingTablePos, req
from CraftButtonHandler import Craft as cr
from TextHandler import Text
from inventoryHandler import getInventoryItems
from item import Item
import recipeHandler as rh



class Crafting():
    def __init__(self, screen):
        self.recipies = rh.RecipeHandler()
        self.allItems = self.recipies.getAllItemIDs()
        self.screen = screen
        self.menuBackround = pygame.sprite.Group()
        self.currentItem = pygame.sprite.GroupSingle()
        self.currentRequirements = pygame.sprite.GroupSingle()
        self.currentItemName = pygame.sprite.GroupSingle()
        self.leftArrow = Text("<", 35, "white",  ((craftingTablePos[0] + blockSize/2) - (blockSize * 5)/2.5, craftingTablePos[1] - blockSize * 5.5))
        self.rightArrow = Text(">", 35, "white", ((craftingTablePos[0] + blockSize/2) + (blockSize * 5)/3, craftingTablePos[1] - blockSize * 5.5))

        self.curr = 0

        self.menuBackround.add(cr(9, ((craftingTablePos[0] + blockSize/2) - (blockSize * 5)/2, craftingTablePos[1] - blockSize * 10), blockSize * 5, blockSize * 10))
        self.menuBackround.add(self.leftArrow)
        self.menuBackround.add(self.rightArrow)
        self.menuBackround.add(Text("CRAFTING", 21, "white",  ((craftingTablePos[0] + blockSize/2) - 55, craftingTablePos[1] - blockSize * 9.5)))

        self.currentItem.add(cr(self.allItems[self.curr], ((craftingTablePos[0] + blockSize/2) - blockSize/1.2, craftingTablePos[1] - blockSize * 8), blockSize * 1.8, blockSize * 1.8))

        self.getItemName(self.allItems[self.curr])
        self.getRequirements(self.allItems[self.curr])

    def checkClick(self, pos):
        for sp in self.menuBackround:
            if (sp.rect.collidepoint(pos)):
                if(sp == self.leftArrow):
                    if(self.curr >= 1):
                        self.curr -= 1
                        self.currentItem.add(cr(self.allItems[self.curr], ((craftingTablePos[0] + blockSize/2) - blockSize/1.2, craftingTablePos[1] - blockSize * 8), blockSize * 1.8, blockSize * 1.8))
                        self.getItemName(self.allItems[self.curr])
                        self.getRequirements(self.allItems[self.curr])
                elif(sp == self.rightArrow):
                    if(self.curr < len(self.allItems) - 1):
                        self.curr += 1    
                        self.currentItem.add(cr(self.allItems[self.curr], ((craftingTablePos[0] + blockSize/2) - blockSize/1.2, craftingTablePos[1] - blockSize * 8), blockSize * 1.8, blockSize * 1.8))
                        self.getItemName(self.allItems[self.curr])
                        self.getRequirements(self.allItems[self.curr])
                        
    def getItemName(self, itemID):
        tempText = Text(itemIDs[itemID], 10, "white", ((craftingTablePos[0] + blockSize/2) - blockSize/0.85, craftingTablePos[1] - blockSize * 5))
        self.currentItemName.add(tempText)

    def getRequirements(self, itemID):
        currentRecipe = self.recipies.getRecipe(itemID)
        allRecipeInfo = self.recipies.getRecipeInfo(itemID)
        curr_col = "lime"

        tempRequirements = pygame.sprite.GroupSingle()

        for positional, item in enumerate(currentRecipe):
            tempItem = Item(itemIDs[item], item)
            tempItem.amount = currentRecipe[item]

            if(not self.isCraftable(tempItem, getInventoryItems())):
                curr_col = "red"
            
            tempRequirements.add(Text(tempItem.itemName + " : " + str(tempItem.amount ), 14, curr_col, ((craftingTablePos[0] + blockSize) - blockSize*2.5, craftingTablePos[1] - blockSize*4  + blockSize * positional/2)))

        self.currentRequirements.add(tempRequirements)

           

    #Takes in the current item and the player inventory and checks if the player has enough items
    def isCraftable(self, item, playerItems):
        for resource in playerItems:
            if(resource.itemName == item.itemName):
                if (resource.amount >= item.amount):
                    return True
        return False

    def makeScreen(self):
        self.menuBackround.draw(self.screen)
        self.currentItem.draw(self.screen)
        self.currentItemName.draw(self.screen)
        self.currentRequirements.draw(self.screen)
        


