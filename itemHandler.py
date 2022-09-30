import json
from itemNew import Item

#WHEN USING items = [] FROM THE fetchDict() FUNCTION, ENSURE YOU ADD ONE TO ALL THE ENTRIES
items = []
itemIDs = {}
isPlaceable = {}
blockHardness = {}
breakTime = {}
itemHardness = {}
textureNames = {}

#Pre-defined (These will slowly be phased out, one step at a time.)
immovableBlocks = [3, 5]
clickableBlocks = [5]

craftingIDs = {
    0 : "Wooden Planks",
    1 : "Wooden Pickaxe",
    2 : "Stone Pickaxe",
    3 : "Diamond",
    4 : "Emerald",
    5 : "Gold Ingot",
    6 : "Diamond Block",
    7 : "Gold Block",
    8 : "End Game Block"
}

converterIDs = {
    'G' : 0, #Grass
    'D' : 1, #Dirt
    'S' : 2, #Stone
    #'C' : 3, #Clouds
    'B' : 4, #Bedrock
    'T' : 5, #Crafting Table
    'V' : 6, #Leaves
    'L' : 7, #Logs,
    "C" : 41, #Coal Ore
    "I" : 43, #Iron Ore
    "A" : 46, #Gold Ore
    "M" : 49, #Diamond Ore
    "E" : 78, #Emerald Ore
    "O" : 67, #Diamond Block
    "R" : 63, #Emerald Block
    "U" : 64, #Gold Block
    "X" : 83 #End Game Block
}

#Populate Dictionary
def fetchDict():
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
    return items

def fetchItemIDs():
    file = open("items.json")
    data = json.load(file)
    for i in data:
        itemIDs[data[i]['itemID']] = data[i]['itemDisplayName']
        tempItem = None
    return itemIDs

def fetchIsPlaceable():
    file = open("items.json")
    data = json.load(file)
    for i in data:
        isPlaceable[data[i]['itemID']] = data[i]['isPlaceable']
    return isPlaceable

def fetchBlockHardness():
    file = open("items.json")
    data = json.load(file)
    for i in data:
        blockHardness[data[i]['itemID']] = data[i]['blockHardness']
    return blockHardness

def fetchBreakTime():
    file = open("items.json")
    data = json.load(file)
    for i in data:
        breakTime[data[i]['itemID']] = data[i]['breakTime']
    return breakTime

def fetchItemHardness():
    file = open("items.json")
    data = json.load(file)
    for i in data:
        itemHardness[data[i]['itemID']] = data[i]['itemHardness']
    return itemHardness

def fetchTextureNames():
    file = open("items.json")
    data = json.load(file)
    for i in data:
        textureNames[data[i]['itemDisplayName']] = data[i]['texture']
    return textureNames
# fetchDicts()
# for i in items:
#     print("Item ID:\t" + str(i.getItemId()))                                #getItemId()
#     print("\tItem Name:\t\t " + str(i.getItemName()))                       #getItemName()
#     print("\tBreak Time:\t\t " + str(i.getBreakTime()))                     #getBreakTime()
#     print("\tBlock Hardness:\t " + str(i.getBlockHardness()))               #getBlockHardness()
#     print("\tItem Hardness:\t " + str(i.getItemHardness()))                 #getItemHardness
#     print("\tReq Tool Type:\t " + str(i.getReqToolType()))                  #getReqToolType()
#     print("\tSelf Tool Type:\t " + str(i.getToolType()))                    #getToolType()
#     print("\tTexture Path:\t " + str(i.getTexture()))                       #getTexture() -- Returns a file path as a string
#     print("\tIs Placeable:\t " + str(i.getIsPlaceable()))                   #getIsPlaceable()
#     print("\tDrops:\t\t\t " + str(items[i.getDrop()+1].getItemName()))      #getDrop() returns the item ID of the dropped item, add one to index in items array




