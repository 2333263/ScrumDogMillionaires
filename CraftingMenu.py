import pygame
from gameSettings import itemIDs, blockSize, isPlaceable, itemHardness
import gameSettings as gs
from TextHandler import Text
from item import Item
import recipeHandler as rh
import numpy as np
from inventoryHandler import  addBlock, addItem, decreaseSpec, getClicked, invArray, setClicked
from InventorySlots import slot

slots=pygame.sprite.Group()
relative=gs.blockSize/30
buttonFont = pygame.font.Font('Minecraft.ttf', 40)  # font for button
#invArray=np.full(40,NullItem,dtype=Item)
NullItem=Item("null",-1)
craftArray=np.full([3,3],NullItem,dtype=Item)


class Crafting():
    def __init__(self, screen):
        
        self.relativeSize = blockSize * 3 #must be between 0 and window size
        self.recipes = rh.RecipeHandler() #already tested 
        self.allItems = self.recipes.getAllItemIDs() #Must be a list 
        self.screen = screen #Must be of data type pygame screen 
        self.canCraft = False #Must be a boolean 
        self.craftID=-1 #ID of item to be crafted
        
            
    def drawCraft(self):
        #draw background rectangle of crafting table
        pygame.draw.rect(self.screen,(173,139,120),[900*relative,140*relative,255*relative,100*relative*4],0)
        #draw the blocks of the crafting table 
        slots.draw(self.screen)
        colour=(255, 255, 255)
        if(self.canCraft):
            #if you can craft an item
            #change the colour of craft from white to green
            colour= (0,255,0)
            #place the craftable item next to the word craft
            tempItem=Item(itemIDs[self.craftID],self.craftID)
            currTexture =tempItem.texture
            currTexture=pygame.transform.scale(currTexture,(50*relative,50*relative))
            self.screen.blit(currTexture,(928*relative,463*relative))
        
        craftText = buttonFont.render('CRAFT', True, colour)
        self.screen.blit(craftText, (1000*relative, 475*relative))
        #traverse through craft array and add in the corresponding block textures to the crafting  table
        for j in range (3):
            for i in range(3):
                if(craftArray[j][i].itemID!=-1):
                    currTexture = craftArray[j][i].texture
                    currTexture=pygame.transform.scale(currTexture,(50*relative,50*relative))
                    self.screen.blit(currTexture,(917*relative+(i)*85*relative,65*relative + relative* (j+1)*100))
        
              
   #initlize the slots as a sprite group
    def initGroup(self):
        for j in range (3):
            for i in range(3):
                s=slot((0,0,0),907*relative+i*85*relative,150*relative+j*100*relative,70*relative,80*relative)
                slots.add(s)
        #'slot' that is used as the button to craft an item       
        s=slot((71,45,45),907*relative,150*relative+3*100*relative,240*relative,80*relative)
        slots.add(s)
    def checkCanCraft(self): #checks if the block placement within the table matches any valid recipes
        craftIDArray=np.full([3,3],-1) #IDs of items in the crafting table as a matrix
        for i in range (3):
            for j in range( 3):
                craftIDArray[i][j]=craftArray[i][j].itemID

        
        for i in self.allItems:
            if(np.array_equal(craftIDArray,self.recipes.getCraftingMatrix(i))): #compares crafting table to all recipe matrices
                self.canCraft=True
                self.craftID=i
                return
        #only runs if no match is found
        self.canCraft=False 
        self.craftID=-1
        
    def doCraft(self):
        #this function crafts the craftable item
        self.checkCanCraft()
        if(self.canCraft):
            for i in range(self.recipes.getCraftingAmount(self.craftID)):
             #If item is a placeable object, it is then counted as a block
                if (isPlaceable[self.craftID]):
                            newTempItem = Item(itemIDs[self.craftID], self.craftID)
                            addBlock(newTempItem)
                #Else the item is added as an item with an item hardness, defined in gameSettings.py
                else:
                            newTempItem = Item(itemIDs[self.craftID], self.craftID, itemHardness[self.craftID])   
                            addItem(newTempItem)
            self.emptyTable()

    def onClick(self,pos):
        #checks which bloc in the crafting table has been clicked by the user- acts accordingly
        i=0
        j=0
        clicked=getClicked()
        #loop through all slots
        for box in slots:
          
            #if a sprite collides with where you clicked
            if(box.rect.collidepoint(pos)):
                if (j==3):
                    self.doCraft()
                else:
                    craftItem=craftArray[j][i]
                    #if the inventory is open and nothing has been selected previously
                    if(clicked!=-1):
                        #if a slot was previously selected in the inventory, place that selected item in the 
                        #chosen block in the crafting table
                        inventoryItem=invArray[clicked]
                        craftArray[j][i]=Item(inventoryItem.getItemName(),inventoryItem.getItemId())
                        decreaseSpec(inventoryItem.getItemId())
                        if(craftItem.getItemId()!=-1):
                            #replace the item in the crafting table with one of item in the inventory
                            addItem(craftItem)
                            craftArray[j][i]=inventoryItem 
                        
                
                        setClicked() #set the clicked item to -1 in inventory
                    
                    else: #if nothing was previously selected and if selecet craft item slot not null
                        if(craftItem.getItemId()!=-1):
                            addItem(craftItem) #add the item to the inventory
                            craftArray[j][i]=NullItem
                    self.checkCanCraft() #check if the crafting table matches any valid recipes
                break
            i+=1
            if(i==3):#if you have gone through all the slots in the row, go to the next row
                i=0
                j+=1


    def emptyTable(self): #empty's the crafting table when an item is crafted so resources are used up
        global craftArray
        craftArray=np.full([3,3],NullItem,dtype=Item) #empty the crafting table
        self.canCraft=False #can't craft an item
        self.craftID=-1 #no item to craft



   

   
    

        