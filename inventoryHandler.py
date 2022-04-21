from item import Item
from gameSettings import itemIDs

#Init inv with item objects
hotbarArr = []

#Will have to change this when we add full inventory
#Should only allow +- 10 different item types in the hotbar
for item in itemIDs:
    hotbarArr.append(Item(itemIDs[item], item))

global selected;
selected = 0;

def addBlock(block):
    #Updates based on ItemID - need to ensure hotbar arr has all items added first
    hotbarArr[block.itemID].increase()


def decrease():
    #decreases currently selected item
    hotbarArr[selected].decrease()


def decreaseSpec(i):
    # decreases a specific item based on id
    hotbarArr[i].decrease()


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

def getHotBar():
    return hotbarArr

def getItemCount(itemID):
    return hotbarArr[itemID].amount
