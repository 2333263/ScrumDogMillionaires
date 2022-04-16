#When random world gen is done, could just feel level into levelName to avoid exsessive code changes
levelName = "level"

with open('Levels/' + levelName + '.txt') as f:
    levelArray = f.readlines()

blockSize = 24
playerRange = 7

drawCrafting = False
craftingPos = (0, 0)

width = round(blockSize * len(levelArray[0])) - blockSize
height = round(blockSize * len(levelArray))

itemIDs = {
    0 : "Grass",
    1 : "Dirt",
    2 : "Stone",
    3 : "Cloud",
    4 : "Bedrock",
    5 : "Crafting Table",
    6 : "Leaves",
    7 : "Logs",
    8 : "Wooden Pickaxe",
    9 : "Wooden Planks"
}

#IDs for the crafting table
#when json file is loaded into an array, say like data, data[0] will refer to the wooden planks recipe
#data[0]['toolName'] would return wooden planks 

craftingIDs = {
    0 : "wooden planks", 
    1 : "wooden pickaxe", 
    2 : "wood and stone pickaxe", 
    3 : "stone pickaxe"
}

converterIDs = {
    'G' : 0,
    'D' : 1,
    'S' : 2,
    'C' : 3,
    'B' : 4,
    'T' : 5,
    'V' : 6,
    'L' : 7
}

textureNames = {
    "Grass" : "grass.png",
    "Stone" : "stone.png",
    "Dirt" : "dirt.png",
    "Cloud" : "cloud.png",
    "Bedrock" : "bedrock.png",
    "Crafting Table" : "crafting.png",
    "Leaves" : "leaves_dense.png",
    "Logs" : "wood_log.png",
    "Wooden Pickaxe" : "wooden_pickaxe.png"
}

colorNames = {
    #Capitalised colours to align with Item.item_name
    "Sky" : (135, 206, 250),
}

immovableBlocks = [3, 4, 5]
clickableBlocks = [5]