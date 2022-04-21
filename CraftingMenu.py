from numpy import block
import pygame
from gameSettings import itemIDs, textureNames, blockSize, craftingTablePos
from CraftButtonHandler import Button 
from TextHandler import Text
from item import Item
import recipeHandler as rh

class Crafting():
    def __init__(self, screen):
        self.recipies = rh.RecipeHandler()
        self.allItems = self.recipies.getAllItemIDs()
        self.screen = screen
        self.menuBackround = self.makeBackground()
        self.craftables = self.populatePossibleItems()
        self.itemName = pygame.sprite.GroupSingle()
        self.itemRecipe = pygame.sprite.Group()

       
    def makeScreen(self):
        self.menuBackround.draw(self.screen)
        self.craftables.draw(self.screen)
        self.itemName.draw(self.screen)
        self.itemRecipe.draw(self.screen)


    def makeBackground(self):
        tempBackround = pygame.sprite.Group()
        leftArrow = Text("<", int(blockSize), pygame.Color(76, 76, 76),  (craftingTablePos[0] - blockSize * 4, craftingTablePos[1] - blockSize * 5.5/2))
        rightArrow = Text(">", int(blockSize), pygame.Color(76, 76, 76),  (craftingTablePos[0] , craftingTablePos[1] - blockSize * 5.5/2))
       
        tempBackround.add(Button(9, (craftingTablePos[0] - blockSize * 4.5, craftingTablePos[1] - blockSize * 5.5), blockSize * 10, blockSize * 5))
        tempBackround.add(leftArrow)
        tempBackround.add(rightArrow)
        
        return tempBackround

    def populatePossibleItems(self):
        craftableItems = self.recipies.getAllItemIDs()
        tempItemList = pygame.sprite.Group()

        baseX, baseY = (craftingTablePos[0] - blockSize * 3.55), (craftingTablePos[1] - blockSize * 4.4)
        countX, countY = 0, 0


        for  item in (craftableItems):
            if(countX != 0 and (countX)%3 == 0):
                countX = 0
                countY += 1
    
            tempBut = Button(item, (baseX + blockSize * 1.1 * countX, baseY+ blockSize * 1.1 * countY), blockSize/1.2, blockSize/1.2)
            tempItemList.add(tempBut)
            countX += 1
        
        return tempItemList

    def populateRecipe(self, itemID):
        self.itemRecipe.empty()
        recipeItems = self.recipies.getCraftingShape(itemID)

        baseX, baseY = (craftingTablePos[0] + blockSize * 4.55), (craftingTablePos[1] - blockSize * 4.4)
        countX, countY, standardCount = 0, 0, 0

        for  item in (recipeItems):
            if(item == -1):
                countX += 1
                continue

            if(countX != 0 and (countX)%3 == 0):
                countX = 0
                countY += 1
    
            tempBut = Button(item, (baseX + blockSize * 1.1 * countX, baseY+ blockSize * 1.1 * countY), blockSize/1.2, blockSize/1.2)
            self.itemRecipe.add(tempBut)
            countX += 1

    def checkClick(self, pos):
        for menuItem in self.craftables:
            if (menuItem.rect.collidepoint(pos)):
                print(str(menuItem.itemID ) + " clicked")
                tempText = Text(itemIDs[menuItem.itemID] , int(blockSize/2), pygame.Color(76, 76, 76), (craftingTablePos[0] +  blockSize * 2.88, craftingTablePos[1] - blockSize * 5))
                self.itemName.add(tempText)
                self.populateRecipe(menuItem.itemID)
             