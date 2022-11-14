import json
from MainGame.Items.itemNew import Item

#WHEN USING items = [] FROM THE fetchDict() FUNCTION, ENSURE YOU ADD ONE TO ALL THE ENTRIES

#initialise various dictionaries and arrays 
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

#dictionary of crrafting item IDs
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

#dictionary of converted IDs
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
    file = open("MainGame/Items/items.json")
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
    file.close()
    return items
#returns a dictionary of item ids
def fetchItemIDs():
    file = open("MainGame/Items/items.json")
    data = json.load(file)
    for i in data:
        itemIDs[data[i]['itemID']] = data[i]['itemDisplayName']
        tempItem = None
    file.close()
    return itemIDs
#returns if an item is placeable or not
def fetchIsPlaceable():
    file = open("MainGame/Items/items.json")
    data = json.load(file)
    for i in data:
        isPlaceable[data[i]['itemID']] = data[i]['isPlaceable']
    file.close()
    return isPlaceable
#returns a blocs hardness level
def fetchBlockHardness():
    file = open("MainGame/Items/items.json")
    data = json.load(file)
    for i in data:
        blockHardness[data[i]['itemID']] = data[i]['blockHardness']
    file.close()
    return blockHardness
#returns a tools break time for variable breaking speed
def fetchBreakTime():
    file = open("MainGame/Items/items.json")
    data = json.load(file)
    for i in data:
        breakTime[data[i]['itemID']] = data[i]['breakTime']
    file.close()
    return breakTime
#returns a blocs hardness level
def fetchItemHardness():
    file = open("MainGame/Items/items.json")
    data = json.load(file)
    for i in data:
        itemHardness[data[i]['itemID']] = data[i]['itemHardness']
    file.close()
    return itemHardness
#returns the texture name
def fetchTextureNames():
    file = open("MainGame/Items/items.json")
    data = json.load(file)
    for i in data:
        textureNames[data[i]['itemDisplayName']] = data[i]['texture']
    file.close()
    return textureNames




