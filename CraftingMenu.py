import pygame
from gameSettings import itemIDs, blockSize, craftingTablePos
from CraftButtonHandler import Button
from TextHandler import Text
from item import Item
import recipeHandler as rh
from inventoryHandler import getHotBar, addBlock, decreaseSpec, getItemCount


class Crafting():
    def __init__(self, screen):
        self.relativeSize = blockSize * 3
        self.recipies = rh.RecipeHandler()
        self.allItems = self.recipies.getAllItemIDs()
        self.screen = screen
        self.menuBackround = self.makeBackground()
        self.craftables = self.populatePossibleItems()
        self.itemName = pygame.sprite.GroupSingle()
        self.itemRecipe = pygame.sprite.Group()
        self.itemsNeeded = dict()
        self.canCraft = False
        self.createdItem = -1
        self.craftButton = pygame.sprite.Group()
        
    def makeScreen(self):
        self.menuBackround.draw(self.screen)
        self.craftables.draw(self.screen)
        self.itemName.draw(self.screen)
        self.itemRecipe.draw(self.screen)
        self.craftButton.draw(self.screen)

    def makeBackground(self):
        tempBackround = pygame.sprite.Group()

        # When there are more items to craft that require more pages, uncomment the below 4 lines and make sure to have a page tracker
        # leftArrow = Text("<", int(self.relativeSize), pygame.Color(76, 76, 76),  (craftingTablePos[0] - self.relativeSize * 4, craftingTablePos[1] - self.relativeSize * 5.5/2))
        # rightArrow = Text(">", int(self.relativeSize), pygame.Color(76, 76, 76),  (craftingTablePos[0] , craftingTablePos[1] - self.relativeSize * 5.5/2))
        close = Text("X", int(self.relativeSize/2), pygame.Color(76, 76, 76),  (craftingTablePos[0] + self.relativeSize * 5,  craftingTablePos[1] - 4.9* self.relativeSize ))
        tempBackround.add(Button(9, (craftingTablePos[0] - self.relativeSize * 4.5, craftingTablePos[1] -
                          self.relativeSize * 5.5), self.relativeSize * 10, self.relativeSize * 5))
        tempBackround.add(close)
        # tempBackround.add(rightArrow)

        return tempBackround

    def populatePossibleItems(self):
        craftableItems = self.recipies.getAllItemIDs()
        tempItemList = pygame.sprite.Group()

        baseX, baseY = (craftingTablePos[0] - self.relativeSize *
                        3.55), (craftingTablePos[1] - self.relativeSize * 4.4)
        countX, countY = 0, 0

        for item in (craftableItems):
            if(countX != 0 and (countX) % 3 == 0):
                countX = 0
                countY += 1

            tempBut = Button(item, (baseX + self.relativeSize * 1.1 * countX, baseY +
                             self.relativeSize * 1.1 * countY), self.relativeSize/1.2, self.relativeSize/1.2)
            tempItemList.add(tempBut)
            countX += 1

        return tempItemList

    def populateRecipe(self, itemID):
        self.itemRecipe.empty()
        recipeItems = self.recipies.getCraftingShape(itemID)

        baseX, baseY = (craftingTablePos[0] + self.relativeSize *
                        1.5), (craftingTablePos[1] - self.relativeSize * 4.4)
        countX, countY = 0, 0

        for item in (recipeItems):
            if(item == -1):
                continue

            if(countX != 0 and (countX) % 3 == 0):
                countX = 0
                countY += 1

            tempBut = Button(item, (baseX + self.relativeSize * 1.1 * countX, baseY +
                             self.relativeSize * 1.1 * countY), self.relativeSize/1.2, self.relativeSize/1.2)
            self.itemRecipe.add(tempBut)
            countX += 1

    def resetTable(self):
        self.itemRecipe.empty()
        self.craftButton.empty()

    def checkClick(self, pos):
        for menuItem in self.craftables:
            if (menuItem.rect.collidepoint(pos)):
                tempText = Text(itemIDs[menuItem.itemID], int(self.relativeSize/2), pygame.Color(76, 76, 76),
                                (craftingTablePos[0] + self.relativeSize * 2.88, craftingTablePos[1] - self.relativeSize * 5))
                self.itemName.add(tempText)
                self.populateRecipe(menuItem.itemID)
                self.createdItem = menuItem.itemID

                if(self.isCraftable(menuItem.itemID, getHotBar())):
                    self.craftButton.empty()
                    craftBut = Text("CRAFT", int(self.relativeSize/2), "lime",
                                    (craftingTablePos[0] + self.relativeSize/2.25, craftingTablePos[1] - self.relativeSize * 1), pygame.Color(198, 198, 198))
                    self.craftButton.add(craftBut)
                    self.canCraft = True

                else:
                    self.craftButton.empty()
                    craftBut = Text("CRAFT", int(self.relativeSize/2), "red",
                                    (craftingTablePos[0] + self.relativeSize/2.25, craftingTablePos[1] - self.relativeSize * 1), pygame.Color(198, 198, 198))
                    self.craftButton.add(craftBut)
                    self.canCraft = False

    def makeItem(self, pos):
        for sp in self.craftButton:
            if (sp.rect.collidepoint(pos) and self.canCraft):
                if(self.createdItem != -1):
                    tempItem = Item(
                        itemIDs[self.createdItem], self.createdItem)
                    for item in self.itemsNeeded:
                        for i in range(self.itemsNeeded[item]):
                            if(getItemCount(item) > 0):
                                decreaseSpec(item)
                            else:
                                self.canCraft = False
                                self.resetTable()
                                return
                            if(getItemCount(item) == 0):
                                self.canCraft = False
                                self.resetTable()
                    for i in range(self.recipies.getCraftingAmount(self.createdItem)):
                        addBlock(tempItem)
                    self.resetTable()

   # Takes in the current item and the player inventory and checks if the player has enough items
    def isCraftable(self, itemID, playerInventory):
        if(len(playerInventory) == 0):
            return False
        self.itemsNeeded = self.recipies.getRecipe(itemID)
        for resource in self.itemsNeeded:
            found = False
            for item in playerInventory:
                if(item.itemID == resource):
                    found = True
                    if(item.amount < self.itemsNeeded[resource]):
                        return False
            if (not found):
                return False
        return True
    
    def closeTable():
        