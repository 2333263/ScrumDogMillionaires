import json
from itemNew import Item

items = []

#Pre-defined (These will slowly be phased out, one step at a time.)
immovableBlocks = [3, 5]
clickableBlocks = [5]

craftingIDs = {
    0 : "Wooden Planks", 
    1 : "Wooden Pickaxe", 
    2 : "Stone Pickaxe",
    3 : "Stone Shovel"
}


#Populate Dictionaries
def fetchDicts():
    file = open("items.json")
    data = json.load(file)
    for i in data:
        tempItem = Item(data[i]['itemID'],
                        data[i]['itemDisplayName'],
                        data[i]['breakTime'],
                        data[i]['blockHardness'],
                        data[i]['itemHardness'],
                        data[i]['reqToolType'],
                        data[i]['toolType'],
                        data[i]['texture'],
                        data[i]['isPlaceable'],
                        data[i]['drops'])
        items.append(tempItem)
        tempItem = None
    return items, immovableBlocks, clickableBlocks, craftingIDs

fetchDicts()
for i in items:
    print("Item ID:\t" + str(i.getItemId()))                                #getItemId()
    print("\tItem Name:\t\t " + str(i.getItemName()))                       #getItemName()
    print("\tBreak Time:\t\t " + str(i.getBreakTime()))                     #getBreakTime()
    print("\tBlock Hardness:\t " + str(i.getBlockHardness()))               #getBlockHardness()
    print("\tItem Hardness:\t " + str(i.getItemHardness()))                 #getItemHardness
    print("\tReq Tool Type:\t " + str(i.getReqToolType()))                  #getReqToolType()
    print("\tSelf Tool Type:\t " + str(i.getToolType()))                    #getToolType()
    print("\tTexture Path:\t " + str(i.getTexture()))                       #getTexture() -- Returns a file path as a string
    print("\tIs Placeable:\t " + str(i.getIsPlaceable()))                   #getIsPlaceable()
    print("\tDrops:\t\t\t " + str(items[i.getDrop()+1].getItemName()))      #getDrop() returns the item ID of the dropped item, add one to index in items array




