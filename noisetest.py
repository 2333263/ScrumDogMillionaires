from perlin_noise import PerlinNoise
import numpy as np
from scipy import rand
import gameSettings as gs
import random


noise = PerlinNoise(gs.octaves, gs.seed)
xpix, ypix = gs.noXBlocks, 6
heightNoise = (np.array([noise([2, j/ypix]) for j in range(xpix)]) * 10).astype(int)

h = int(gs.height/2 / gs.blockSize) - 5

x_vals = []

world = np.zeros((gs.noYBlocks, gs.noXBlocks))
random.seed(gs.seed)

craftingTableX = random.randint(0, gs.noXBlocks) 

for y in range(gs.noYBlocks):
    for x in range(gs.noXBlocks):
        dirt = random.randint(2, 5)
        if(y == h + heightNoise[x]):
            world[y][x] = 0 #Grass
        elif(y > h + heightNoise[x] and y <= h + heightNoise[x] + dirt):
            world[y][x] = 1 #Dirt
        elif(y > h + heightNoise[x] and y > h + heightNoise[x] + dirt):
            world[y][x] = 2 #Stone
        else:
            world[y][x] = -1 #Sky
        if(y == h + heightNoise[x] - 1 ):
            if (random.randint(1, 25) == 1):
                world[y][x] = -2 #Tree
        if(x == craftingTableX and y == world[y][x] = 5):
            world[y][x] = 5 #Crafting Table


translated_world  = np.empty((gs.noYBlocks, gs.noXBlocks), dtype='str')
translated_world[:] = ' '

for i, row in enumerate(world):
    for j, col in enumerate(row):
        if   (col == 0):
            translated_world[i][j] = "G"
        elif (col == 1):
            translated_world[i][j] = "D"
        elif (col == 2):
            translated_world[i][j] = "S"
        elif(col == -2):
            translated_world[i][j] = "L"
        elif(col == 5):
            translated_world[i][j] = "T"
        # else: 
        #     translated_world[i][j] =" "

f = open("Levels/random.txt", "w")
for row in translated_world:
    worldRow = ""
    for letter in row:
        worldRow += letter
    worldRow += "\n"
    f.write(worldRow)

