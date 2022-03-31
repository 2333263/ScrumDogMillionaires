level_name = "level"

with open('Levels/'+level_name+'.txt') as f:
    level_array = f.readlines()

block_size = 24

width = round(block_size * len(level_array[0])) - block_size
height = round(block_size * len(level_array))

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