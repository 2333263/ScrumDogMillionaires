from matplotlib.pyplot import hot
from item import Item
import pygame
import gameSettings as gs
#Init inv with item objects
hotbarArr = []
itemIDs=gs.itemIDs
#Will have to change this when we add full inventory
#Should only allow +- 10 different item types in the hotbar
for item in itemIDs:
    if(Item(itemIDs[item],item).getCount()>0):
     hotbarArr.append(Item(itemIDs[item], item))

global selected;
selected = 0;

def addBlock(block):
    tempItem=Item(itemIDs[block.itemID],block.itemID)
    for i in hotbarArr:
         if( i.itemId==block.itemID):
                i.increase()
                return
    
    hotbarArr.append(tempItem)
    hotbarArr[len(hotbarArr)-1].increase()
    #Updates based on ItemID - need to ensure hotbar arr has all items added first
   # else:
   #     for i in hotbarArr:
    #         if( i.itemID==block.itemID):
    #            i.increase()
    #            break


def decrease():
    #decreases currently selected item
    hotbarArr[selected].decrease()
    if (hotbarArr[selected].getCount()<=0):
        hotbarArr.pop(selected)
        if(len(hotbarArr)!=0):
            selectPrevious()
   

def decreaseSpec(i):
    # decreases a specific item based on id
    hotbarArr[i].decrease()
    if(hotbarArr[i].getCount()<=0):
        hotbarArr.pop(i)
  




def getSelected():
    #Returns the selected item
    return hotbarArr[selected]


def setSelected(i):
    selected = i

def selectNext():
    #Changes the selected item to the next element in hotbarArr
    #Loops around if too big
    global selected
    if (selected + 1 <= len(hotbarArr)-1):
        selected += 1
    else:
        selected = 0


def selectPrevious():
    #Changes the selected item to the previous element in hotbarArr
    #Loops around if too small
    global selected
    if (selected == 0):
        selected = len(hotbarArr) - 1
    else:
        selected-=1
def drawHotBar(screen):
    
    pygame.draw.rect(screen,(90,90,90),[5,20,850,100],0)
    skip=0
    for i in range(10):
        pygame.draw.rect(screen,(0,0,0),[12+i*85,30,70,80],0)

    for i in range(len(hotbarArr)):
        currTexture = hotbarArr[i].texture
        currTexture=pygame.transform.scale(currTexture,(50,50))
        screen.blit(currTexture,(22+(i)*85,45))
        font = pygame.font.Font('Minecraft.ttf', 16)
        count=hotbarArr[i].getCount()
        text2 = font.render(str(count), 1, (255, 255,255))
        shift=0
        if(count>=10) :
            shift-=5
        if(count>=100):
             shift-=5
        screen.blit(text2,(42+(i)*85+shift,95))
        if (i==selected):
            pygame.draw.rect(screen, (255, 255, 0), (12+(i)*85, 30, 70, 80), 3)


                    
        
        