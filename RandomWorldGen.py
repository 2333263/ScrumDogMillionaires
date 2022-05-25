from perlin_noise import PerlinNoise
import numpy as np
import gameSettings as gs
import random

def generateWorld():
    noise = PerlinNoise(gs.octaves, gs.seed)
    xpix, ypix = gs.noXBlocks, 6
    heightNoise = (np.array([noise([2, j/ypix]) for j in range(xpix)]) * 10).astype(int)

    h = int(gs.height/2 / gs.blockSize) - 5

    world =np.empty((gs.noYBlocks, gs.noXBlocks), dtype='str')
    world[:] = ' '
    random.seed(gs.seed)

    craftingTableX = random.randint(0, gs.noXBlocks) 
    
    #  (0,1) (0,1) (0,1)
    #  (0,1) (0,1) (0,1)
    #  (0,1) (0,1) (0,1)

    def drawOre(world, x, y, ore):
        xChange = yChange =  [-1, 0, 1]
        for xVal in xChange:
            for yVal in yChange:
                if(random.randint(0, 4) == 1):
                    if ((y + yVal > 0 and y + yVal < gs.noYBlocks) and (x + xVal > 1 and x + xVal < gs.noXBlocks - 1)):
                        world[y + yVal][x + xVal] = ore
    

    def drawTree(world, y, x):

        world[y][x] = 'L'
        world[y - 1][x] = 'L'
        world[y - 2][x] = 'L'
        world[y - 2][x - 1] = 'V'
        world[y - 2][x + 1] = 'V'
        world[y - 3][x] = 'V'
        world[y - 3][x + 1] = 'V'
        world[y - 3][x + 2] = 'V'
        world[y - 3][x - 1] = 'V'
        world[y - 3][x - 2] = 'V'
        world[y - 4][x] = 'V'
        world[y - 4][x + 1] = 'V'
        world[y - 4][x - 1] = 'V'
        world[y - 5][x] = 'V'

#traverses through tree and builds a 2d array of the map with letters corresponding to block types
    for y in range(gs.noYBlocks):
        for x in range(gs.noXBlocks):
            dirt = random.randint(2, 5)
            if(y == h + heightNoise[x]):
                world[y][x] = 'G' #Grass
            elif(y > h + heightNoise[x] and y <= h + heightNoise[x] + dirt):
                world[y][x] = 'D' #Dirt
            elif(y > h + heightNoise[x] and y > h + heightNoise[x] + dirt):
                world[y][x] = 'S' #Stone
            else:
                world[y][x] = ' ' #Sky
            if(y == h + heightNoise[x] - 1 and (x > 0 and x < gs.noXBlocks - 3)):
                if (random.randint(1, 25) == 1):
                    drawTree(world, y, x) #Tree
            

            if(y > h + heightNoise[x] - 1 and y > h + heightNoise[x] + 36):
                if (random.randint(1, 120) == 1):
                    drawOre(world, x, y, "M")
            if(y > h + heightNoise[x] - 1 and y > h + heightNoise[x] + 40):
                if (random.randint(1, 230) == 5):
                    drawOre(world, x, y, "E")
            if(y > h + heightNoise[x] - 1 and y > h + heightNoise[x] + 16):
                if (random.randint(1, 35) == 1):
                    drawOre(world, x, y, "I")
            if(y > h + heightNoise[x] - 1 and y > h + heightNoise[x] + 30):
                if (random.randint(1, 100) == 1):
                    drawOre(world, x, y, "A")
            if(y > h + heightNoise[x] - 1 and y > h + heightNoise[x] + 10):
                if (random.randint(1, 28) == 1):
                    drawOre(world, x, y, "C")
            if(x == craftingTableX and y == h + heightNoise[x] - 1):
                world[y][x] = 'T' #Crafting Table

    for i in range(gs.noXBlocks):
        world[gs.noYBlocks - 1][i] = "B"

    return world

