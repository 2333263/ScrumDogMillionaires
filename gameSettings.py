#When random world gen is done, could just feel level into levelName to avoid exsessive code changes
levelName = "level"

with open('Levels/' + levelName + '.txt') as f:
    levelArray = f.readlines()

blockSize = 24
playerRange = 7

width = round(blockSize * len(levelArray[0])) - blockSize
height = round(blockSize * len(levelArray))

itemIDs = {
    0 : "Grass",
    1 : "Dirt",
    2 : "Stone",
    3 : "Cloud"
}


#In future this will need to be updated to use the file names for the textures
textureNames = {
    "Grass" : "grass.png",
    "Stone" : "stone.png",
    "Dirt" : "dirt.png",
    "Cloud" : "cloud.png"
}

colorNames = {
    #Capitalised colours to align with Item.item_name
    "Sky" : (135, 206, 250),
}