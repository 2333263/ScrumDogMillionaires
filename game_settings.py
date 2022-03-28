level_name = "level"

with open('Levels/'+level_name+'.txt') as f:
    level_array = f.readlines()

block_size = 24

width = round(block_size * len(level_array[0])) - block_size
height = round(block_size * len(level_array))

customColours = {
    #Capitalised colours to align with Item.item_name
    "Sky" : (135, 206, 250),
    "Grass" : (14, 154, 60),
    "Stone" : (105, 105, 105),
    "Cloud" : (255, 255, 255),
    "Air" : (255, 255, 255, 0)
}