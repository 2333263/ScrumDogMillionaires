from perlin_noise import PerlinNoise
import numpy as np
from scipy import rand
import gameSettings as gs
import random

def generateWorld():
    noise = PerlinNoise(gs.octaves, gs.seed)
    xpix, ypix = gs.noXBlocks, 6
    heightNoise = (np.array([noise([2, j/ypix]) for j in range(xpix)]) * 10).astype(int)

    h = int(gs.height/2 / gs.blockSize) - 5

    x_vals = []

    world = np.zeros((gs.noYBlocks, gs.noXBlocks))
    random.seed(gs.seed)

    craftingTableX = random.randint(0, gs.noXBlocks) 

    tree = np.array([['#', 'V', '#'],
                    ['V', 'V', 'V'],
                    ['V', 'V', 'V'],
                    ['V', 'L', 'V'],
                    ['#', 'L', '#'], 
                    ['#', 'L', '#']])
    
    def drawTree(world):
        for y in range(gs.noYBlocks):
            for x in range(gs.noXBlocks):
                if world[y][x] == -2:
                    world[y][x] = 7
                    world[y - 1][x] = 7
                    world[y - 2][x] = 7
                    world[y - 2][x - 1] = 6
                    world[y - 2][x + 1] = 6
                    world[y - 3][x] = 6
                    world[y - 3][x + 1] = 6
                    world[y - 3][x - 1] = 6
                    world[y - 4][x] = 6
                    world[y - 4][x + 1] = 6
                    world[y - 4][x - 1] = 6
                    world[y - 5][x] = 6

            
        
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
                
            if(x == craftingTableX and y == h + heightNoise[x] - 1):
                world[y][x] = 5 #Crafting Table

    drawTree(world)
    translated_world  = np.empty((gs.noYBlocks, gs.noXBlocks), dtype='str')
    translated_world[:] = ' '
    
    #Translate the world array to letters
    for i, row in enumerate(world):
        for j, col in enumerate(row):
            if   (col == 0):
                translated_world[i][j] = "G"
            elif (col == 1):
                translated_world[i][j] = "D"
            elif (col == 2):
                translated_world[i][j] = "S"
            elif(col == 7):
                translated_world[i][j] = "L"
            elif(col == 6):
                translated_world[i][j] = "V"
            elif(col == 5):
                translated_world[i][j] = "T"
        
    #Add bedrock to the bottom of the world
    for i in range(gs.noXBlocks):
        translated_world[gs.noYBlocks - 1][i] = "B"

    return translated_world

