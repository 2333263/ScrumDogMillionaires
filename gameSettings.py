#When random world gen is done, could just feel level into levelName to avoid exsessive code changes
levelName = "level"

with open('Levels/' + levelName + '.txt') as f:
    levelArray = f.readlines()

blockSize = 24
playerRange = 7

drawCrafting = False

width = round(blockSize * len(levelArray[0])) - blockSize
height = round(blockSize * len(levelArray))

itemIDs = {
    0 : "Grass",
    1 : "Dirt",
    2 : "Stone",
    # 3 : "Cloud",
    4 : "Bedrock",
    5 : "Crafting Table",
    6 : "Leaves",
    7 : "Logs",
    8 : "Wooden Planks"
}

#IDs for the crafting table
#when json file is loaded into an array, say like data, data[0] will refer to the wooden planks recipe
#data[0]['toolName'] would return wooden planks 

craftingIDs = {
    0 : "wooden_planks", 
    1 : "wooden_pickaxe", 
    2 : "stone_pickaxe"
}

converterIDs = {
    'G' : 0, #Grass
    'D' : 1, #Dirt
    'S' : 2, #Stone
    # 'C' : 3, #Clouds
    'B' : 4, #Bedrock 
    'T' : 5, #Crafting Table
    'V' : 6, #Leaves 
    'L' : 7 #Logs
}

textureNames = {
    "Grass" : "Textures/Blocks/grass.png",
    "Stone" : "Textures/Blocks/stone.png",
    "Dirt" : "Textures/Blocks/dirt.png",
    "Sky" : "Textures/Blocks/sky.png",
    "Bedrock" : "Textures/Blocks/bedrock.png",
    "Crafting Table" : "Textures/Blocks/crafting.png",
    "Leaves" : "Textures/Blocks/leaves_dense.png",
    "Logs" : "Textures/Blocks/wood_log.png"
}

colorNames = {
    #Capitalised colours to align with Item.item_name
    "Sky" : (135, 206, 250),
}

immovableBlocks = [3, 4, 5]
clickableBlocks = [5]