from MainGame.Items.itemNew import Item
import pygame
from MainGame.Settings import gameSettings as gs
from MainGame.Items import itemHandler as ih
import numpy as np
from MainGame.Inventory.InventorySlots import slot
from MainGame.Blocks.block import Block

items = ih.fetchDict()
breakTime = ih.fetchBreakTime()
itemIDs = ih.fetchItemIDs()
blockHardness = ih.fetchBlockHardness()
itemHardness = ih.fetchItemHardness()
#Init inv with item objects
#ItemNew declaration = Item(itemID, itemDisplayName, breakTime, blockHardness, itemHardness, reqToolType, toolType, texture, isPlaceable, drops)
NullItem=Item(-1,"null",99999,5,0,"none","null","Textures/null",False,-1)
invArray=np.full(40, NullItem, dtype=Item)
#Hotbar can be the entire inv, with only the first 10 items beings being displaying in the on-screen hotbar. The player should then be able to change to order of the items.
global selected
selected = 0
fullInv=False
slots=pygame.sprite.Group()
hotBarrSprite=pygame.sprite.Group()
relative=gs.blockSize/30
global clicked
clicked=-1

#Add placeable block (Dirt, Stone, etc...)
def addBlock(block):
    id = block.itemID
    #tempItem=Item(block.itemID,itemIDs[id],breakTime[id],blockHardness[id],itemHardness[id],)
    tempItem = items[id+1]
    smallest_empty=40
    for i in range(len(invArray)):
        if( invArray[i].itemID==block.itemID):
            invArray[i].increase()
            return
        if(invArray[i].itemID==-1 and i<smallest_empty):
            smallest_empty=i
    if (smallest_empty!=40):
        invArray[smallest_empty]=tempItem
        invArray[smallest_empty].increase()

#Add non placeable item or tool (Coal, Ingots, Stone Pickaxe etc...)
def addItem(itemIn):
    id = itemIn.itemID+1
    pi = items[id]
    tempItem=Item(pi.getItemId(),pi.getItemName(),pi.getBreakTime(),pi.getBlockHardness(),pi.getItemHardness(),pi.getReqToolType(),pi.getToolType(),pi.getTexture(),pi.getIsPlaceable(),pi.getDrop())
    smallest_empty=40
    for i in range(len(invArray)):
        if( invArray[i].itemID==itemIn.itemID):
            invArray[i].increase()
            return
        if(invArray[i].itemID==-1 and i<smallest_empty):
            smallest_empty=i
    if (smallest_empty!=40):
        invArray[smallest_empty]=tempItem
        invArray[smallest_empty].increase()
    #print(invArray)


def decrease():
    #decreases currently selected item
    invArray[selected].decrease()
    if (invArray[selected].getCount()<=0):
        invArray[selected]=NullItem
   

def decreaseSpec(itemID):
    # decreases a specific item based on id
    for i in range(len( invArray)):
        if( invArray[i].itemID==itemID):
            invArray[i].decrease()
            if( invArray[i].getCount()<=0):
                invArray[i]=NullItem
            return
  
def getClicked():
    return clicked
    
def setClicked():
  global clicked
  clicked=-1

def getSelected():
    #Returns the selected item
    return invArray[selected]


#def setSelected(i):
    #selected = i

def selectNext():
    #Changes the selected item to the next element in hotbarArr
    #Loops around if too big
    global selected
    if (selected + 1 <= 9):
        selected += 1
    else:
        selected = 0

def selectPrevious():
    #Changes the selected item to the previous element in hotbarArr
    #Loops around if too small
    global selected
    if (selected == 0):
        selected = 9
    else:
        selected-=1

#Massively complex function to select an item from the hot dog bar
def selectInventory(pos):
    global selected
    selected = pos
    
def clearInv():
    NullItem=Item(-1,"null",99999,5,0,"none","null","Textures/null",False,-1)
    invArray=np.full(40, NullItem, dtype=Item)
    for i in invArray:
            if(i.amount>0):
                i.amount=0

def drawHotBar(screen):
    # draws background of hotbar
    pygame.draw.rect(screen,(90,90,90),[5*relative,20*relative,850*relative,100*relative],0)
    #if the inventory is open 
    if(fullInv):
        #draw the full inventory 
        drawInv(screen)
    else:
        #else draw just the hot bar slots
        hotBarrSprite.draw(screen)
    rangeB=0
    rangeT=10
    if(not fullInv):
        if(selected>=10 and selected<20):
            rangeB=10
            rangeT=20
        elif(selected>=20 and selected<30):
            rangeB=20
            rangeT=30
        elif(selected>=30 ):
            rangeB=30
            rangeT=40
    
    for i in range(rangeB,rangeT):
        #if the slot isnt empty
        if(invArray[i].itemID!=-1):
            #get the items texture
            currTexture = pygame.image.load(invArray[i].texture)
            #print(currTexture)
            currTexture=pygame.transform.scale(currTexture,(50*relative,50*relative))
            #draw into the slot on the hotbar
            screen.blit(currTexture,(22*relative+(i-rangeB)*85*relative,45*relative))
            #draw the number of items underneath it
            font = pygame.font.Font('../Font/Minecraft.ttf',int(16 * relative))
            count=invArray[i].getCount()
            text2 = font.render(str(count), 1*relative, (255, 255,255))
            #if the user has more than 10 items, shift the tex over slightly
            shift=0
            if(count>=10) :
                shift-=5
            if(count>=100):
                shift-=5
            screen.blit(text2,(42*relative+(i-rangeB)*85*relative+shift*relative,95*relative))
            #if the inventory is closed, draw a yellow square around the part that is selected
        if (i==selected and not fullInv):
            pygame.draw.rect(screen, (255, 255, 0), (12*relative+(i-rangeB)*85*relative, 30*relative, 70*relative, 80*relative), 3)
            #if the inventory is open, draw a green sqiare around the slot that is selected
        if(i==clicked and fullInv):
             pygame.draw.rect(screen, (0, 255, 0), (12*relative+(i)*85*relative, 30*relative, 70*relative, 80*relative), 3)
   

def getInv():
    return invArray

def getItemCount(itemID):
    for i in invArray:
         if( i.itemID==itemID):
            return i.amount
    return 0

def getItemCountFromInput(itemID, invArrayInput):
    for i in invArrayInput:
         if( i.itemID==itemID):
            return i.amount
    return 0

#same as other draw function, but draws the rest of the inventory other than the hot bar
def drawInv(screen):
    pygame.draw.rect(screen,(180,180,180),[5*relative,140*relative,850*relative,100*relative*3],0)
    slots.draw(screen)
    for j in range (3):
        for i in range(10):
            if(invArray[(j+1)*10+i].itemID!=-1):
                currTexture = pygame.image.load(invArray[(j+1)*10+i].texture)
                currTexture=pygame.transform.scale(currTexture,(50*relative,50*relative))
                screen.blit(currTexture,(22*relative+(i)*85*relative,65*relative + relative* (j+1)*100))
                font = pygame.font.Font('../Font/Minecraft.ttf',int(16 * relative))
                count=invArray[(j+1)*10+i].getCount()
                text2 = font.render(str(count), 1*relative, (255, 255,255))
                shift=0
                if(count>=10) :
                    shift-=5
                if(count>=100):
                    shift-=5
                screen.blit(text2,(42*relative+(i)*85*relative+shift*relative,115*relative+relative*(j+1)*100))
            if((j+1)*10+i==clicked and fullInv):
                pygame.draw.rect(screen, (0, 255, 0), (12*relative+(i)*85*relative, 150*relative+j*100*relative, 70*relative, 80*relative), 3)

#initlize the slots as a sprite group
def initGroup():
    #loop to add the hot bar slots
    for i in range(10):
        s=slot((0,0,0),12*relative+i*85*relative,30*relative,70*relative,80*relative)
        slots.add(s)
        hotBarrSprite.add(s)
        #loop to add the non hot bar slots
    for j in range (3):
        for i in range(10):
            s=slot((0,0,0),12*relative+i*85*relative,150*relative+j*100*relative,70*relative,80*relative)
            slots.add(s)
    cTable= Block(gs.blockSize, (0,0), 5, "Textures/Blocks/crafting.png", 999, ih.breakTime[5])
    addBlock(cTable)   
 #runs when a slot is clicked on           
def onClick(pos):
    i=0
    global clicked
    global selected
    #loop through all slots
    for box in slots:
        #if the inventory is closed and the first 10 sprites have been checked end the loop
        if(fullInv==False and i>9):
            break
        #if a sprite collides with where you clicked
        if(box.rect.collidepoint(pos)):
            #if the invetory is closed set that position in the hotbar as selected
            if(fullInv==False):
                selected=i
            #if the inventory is open and nothing has been selected previously
            elif(clicked==-1):
                #set clicked to be the slot number
                clicked= i
            else:
                #if a slot was previously selected swap the contents of those 2 slots
                invArray[[clicked,i]]=invArray[[i,clicked]]
                clicked=-1
            break    
                
        i+=1
           
           