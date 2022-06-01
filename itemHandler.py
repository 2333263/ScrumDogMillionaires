import json

itemIDs = {} #itemID -> itemDisplayName
blockHardness = {} #itemID -> blockHardness
itemHardness = {} #itemID -> itemHardness
isPlaceable = {} #itemID -> isPlaceable
textureNames = {} #itemDisplayName -> textureDirectory

#Pre-defined (These will slowly be phased out, one step at a time.)
immovableBlocks = [3, 5]
clickableBlocks = [5]

craftingIDs = {
    0 : "Wooden Planks", 
    1 : "Wooden Pickaxe", 
    2 : "Stone Pickaxe",
    3 : "Stone Shovel"
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
    "C" : 13, #Coal Ore
    "I" : 14, #Iron Ore
    "A" : 15, #Gold Ore
    "M" : 16 #Diamond Ore
}   #This dictionary genuinly makes me feel sick, aswell as the craftingIDs but this sprint is like 10 seconds long so deal

#Populate Dictionaries
def populateDictionaries():
    file = open("items.json")
    data = json.load(file)
    for i in data:
        itemIDs[data[i]['itemID']] = data[i]['itemDisplayName']
        blockHardness[data[i]['itemID']] = data[i]['blockHardness']
        itemHardness[data[i]['itemID']] = data[i]['itemHardness']
        isPlaceable[data[i]['itemID']] = data[i]['isPlaceable']
        textureNames[data[i]['itemDisplayName']] = data[i]['texture']
    return

#populateDictionaries()
#for itemID,itemDisplayName in textureNames.items():
    #print(itemID,":",itemDisplayName)




