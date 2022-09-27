import pygame
from gameSettings import blockSize
import itemHandler as ih
import gameSettings as gs
from TextHandler import Text
from itemNew import Item
import recipeHandler as rh
import numpy as np
from inventoryHandler import addBlock, addItem, decreaseSpec, getClicked, invArray, setClicked
from InventorySlots import slot

itemIDs = ih.fetchItemIDs()
textureNames = ih.fetchTextureNames()
isPlaceable = ih.fetchIsPlaceable()
itemHardness = ih.fetchItemHardness()
items = ih.fetchDict()
slots = pygame.sprite.Group()
relative = gs.blockSize/30
buttonFont = pygame.font.Font('Minecraft.ttf', 40)  # font for button
# invArray=np.full(40,NullItem,dtype=Item)
NullItem = items[0]


class Crafting():
    def __init__(self, screen):
        self.craftArray = np.full([3, 3], NullItem, dtype=Item)
        self.relativeSize = blockSize * 3  # must be between 0 and window size
        self.recipes = rh.RecipeHandler()  # already tested
        self.allItems = self.recipes.getAllItemIDs()  # Must be a list
        self.screen = screen  # Must be of data type pygame screen
        self.canCraft = False  # Must be a boolean
        self.craftID = -1  # ID of item to be crafted
        self.itemsNeeded = dict() # items needed to craft an item
    def drawCraft(self):
        # draw background rectangle of crafting table
        pygame.draw.rect(self.screen, (173, 139, 120), [
                         900*relative, 140*relative, 255*relative, 100*relative*4], 0)
        # draw the blocks of the crafting table
        slots.draw(self.screen)
        colour = (255, 255, 255)
        if(self.canCraft):
            # if you can craft an item
            # change the colour of craft from white to green
            colour = (0, 255, 0)
            # place the craftable item next to the word craft
            tempItem = items[self.craftID+1]
            #tempItem = Item(itemIDs[self.craftID], self.craftID)
            currTexture = tempItem.texture
            currTexture = pygame.transform.scale(
                pygame.image.load(currTexture), (50*relative, 50*relative))
            self.screen.blit(currTexture, (928*relative, 463*relative))
        else:
            # question mark is displayed until an item can be craftaed
            # it is then replaced with the item that can be crafted
            questionMark = buttonFont.render('?', True, (255, 255, 255))
            pygame.draw.rect(self.screen, (0, 0, 0), [
                             928*relative, 463*relative, 50*relative, 50*relative])
            self.screen.blit(questionMark, (943*relative, 475*relative))

        craftText = buttonFont.render('CRAFT', True, colour)
        self.screen.blit(craftText, (1000*relative, 475*relative))

        # traverse through craft array and add in the corresponding block textures to the crafting  table
        for j in range(3):
            for i in range(3):
                if(self.craftArray[j][i].itemID != -1):
                    currTexture = self.craftArray[j][i].texture
                    currTexture = pygame.transform.scale(pygame.image.load(currTexture), (50*relative, 50*relative))
                    self.screen.blit(currTexture, (917*relative+(i)*85*relative, 65*relative + relative * (j+1)*100))

   # initlize the slots as a sprite group

    def initGroup(self):
        for j in range(3):
            for i in range(3):
                s = slot((0, 0, 0), 907*relative+i*85*relative, 150 *
                         relative+j*100*relative, 70*relative, 80*relative)
                slots.add(s)
        # 'slot' that is used as the button to craft an item
        s = slot((71, 45, 45), 907*relative, 150*relative +
                 3*100*relative, 240*relative, 80*relative)
        slots.add(s)

    # checks if the block placement within the table matches any valid recipes
    def checkCanCraft(self):
        # IDs of items in the crafting table as a matrix
        craftIDArray = np.full([3, 3], -1)
        for i in range(3):
            for j in range(3):
                craftIDArray[i][j] = self.craftArray[i][j].itemID
                if(self.craftArray[i][j].itemID!=-1):
                    print(self.craftArray[i][j].itemID,"\n")

        for i in self.allItems:
            # compares crafting table to all recipe matrices
            if(np.array_equal(craftIDArray, self.recipes.getCraftingMatrix(i))):
                self.canCraft = True
                self.craftID = i
                return
        # only runs if no match is found
        self.canCraft = False
        self.craftID = -1

    def doCraft(self):
        # this function crafts the craftable item
        self.checkCanCraft()
        if(self.canCraft):
            for i in range(self.recipes.getCraftingAmount(self.craftID)):
             # If item is a placeable object, it is then counted as a block
                if (isPlaceable[self.craftID]):
                    newTempItem = items[self.craftID+1]
                    #newTempItem = Item(itemIDs[self.craftID], self.craftID)
                    addBlock(newTempItem)
                # Else the item is added as an item with an item hardness, defined in gameSettings.py
                else:
                    #newTempItem = Item(
                        #itemIDs[self.craftID], self.craftID, itemHardness[self.craftID])
                    newTempItem = items[self.craftID+1]
                    addItem(newTempItem)
            self.emptyTable()

    def onClick(self, pos):
        # checks which bloc in the crafting table has been clicked by the user- acts accordingly
        i = 0
        j = 0
        clicked = getClicked()
        # loop through all slots
        for box in slots:

            # if a sprite collides with where you clicked
            if(box.rect.collidepoint(pos)):
                if (j == 3):
                    self.doCraft()
                else:
                    craftItem = self.craftArray[j][i]
                    # if the inventory is open and nothing has been selected previously
                    if(clicked != -1):
                        # if a slot was previously selected in the inventory, place that selected item in the
                        # chosen block in the crafting table
                        inventoryItem = invArray[clicked]
                        id = inventoryItem.getItemId()
                        tempItem = items[id+1]
                        self.craftArray[j][i] = Item(id
                                                    ,tempItem.getItemName()
                                                    ,tempItem.getBreakTime()
                                                    ,tempItem.getBlockHardness()
                                                    ,tempItem.getItemHardness()
                                                    ,tempItem.getReqToolType()
                                                    ,tempItem.getToolType()
                                                    ,tempItem.getTexture()
                                                    ,tempItem.getIsPlaceable()
                                                    ,tempItem.getDrop())
                        decreaseSpec(inventoryItem.getItemId())
                        if(craftItem.getItemId() != -1):
                            # replace the item in the crafting table with one of item in the inventory
                            addItem(craftItem)
                            self.craftArray[j][i] = inventoryItem

                        setClicked()  # set the clicked item to -1 in inventory

                    else:  # if nothing was previously selected and if selecet craft item slot not null
                        if(craftItem.getItemId() != -1):
                            # aWSdd the item to the inventory
                            addItem(craftItem)
                            self.craftArray[j][i] = NullItem
                    self.checkCanCraft()  # check if the crafting table matches any valid recipes
                break
            i += 1
            if(i == 3):  # if you have gone through all the slots in the row, go to the next row
                i = 0
                j += 1

    # empty's the crafting table when an item is crafted so resources are used up
    def emptyTable(self):

        # empty the crafting table
        self.craftArray = np.full([3, 3], NullItem, dtype=Item)
        self.canCraft = False  # can't craft an item
        self.craftID = -1  # no item to craft

    def craftSpec(self, craftingID, playerInventory):
        # This function checks if the player has the required items to craft the item
        # It returns true if the player has the required item and adds to inventory, false otherwise
        itemID = self.recipes.getItemIDFromCraftingID(craftingID)
        if(itemID == -1):
            return False
        if(len(playerInventory) == 0):
            return False
        self.itemsNeeded = self.recipes.getRecipe(itemID)
        for resource in self.itemsNeeded:
            found = False
            for item in playerInventory:
                if(item.itemID == resource):
                    found = True
                    if(item.amount < self.itemsNeeded[resource]):
                        return False
            if (not found):
                return False
        for item in self.itemsNeeded:
            for i in range(self.itemsNeeded[item]):
                if(item> 0):
                    decreaseSpec(item)
        tempItem = Item(
            itemIDs[itemID], itemID)
        for i in range(self.recipes.getCraftingAmount(itemID)):
            # If item is a placeable object, it is then counted as a block
            if (isPlaceable[tempItem.getItemId()]):
                addBlock(tempItem)
            # Else the item is added as an item with an item hardness, defined in gameSettings.py
            else:
                newTempItem = Item(
                    tempItem.itemName, tempItem.itemID, itemHardness[tempItem.getItemId()])
                addItem(newTempItem)
        return True
