level_name = "level"

with open('Levels/'+level_name+'.txt') as f:
    level_array = f.readlines()

block_size = 24

width = round(block_size * len(level_array[0])) - block_size
height = round(block_size * len(level_array))

customColours = {
    "sky" : (135, 206, 250), 
    "grass" : (14, 154, 60),
    "stone" : (105, 105, 105),
    "cloud" : (255, 255, 255)
}