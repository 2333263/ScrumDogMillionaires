from perlin_noise import PerlinNoise
import numpy as np
import gameSettings as gs
import random
import pygame
from block import Block

def drawOre(world, x, y, ore):
    xChange = yChange =  [-1, 0, 1]
    for xVal in xChange:
        for yVal in yChange:
            if(random.randint(0, 4) == 1):
                if ((y + yVal > 0 and y + yVal < gs.noYBlocks) and (x + xVal > 1 and x + xVal < gs.CHUNK_SIZE[0] - 1)):
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

def getWorldSprites(world, generatePos):
    worldGroup = pygame.sprite.Group()
    for i in range(gs.CHUNK_SIZE[0]):
        for j in range(gs.noYBlocks):
            currHeight = i * gs.blockSize
            currWidth = j * gs.blockSize
            if(world[j][i] == ' '):
                continue
             #Create a block using the current number in the level
            currItemID = int(gs.converterIDs[world[j][i]])
            if(gs.itemIDs.__contains__(currItemID)):
                if(currItemID == 5): #Deal with crafting table
                    b = Block(gs.blockSize, (currHeight + (generatePos * gs.blockSize), currWidth), currItemID, gs.textureNames[gs.itemIDs[currItemID]], gs.blockHardness[currItemID])
                else: #Deal with all other blocks in the world
                    b = Block(gs.blockSize, (currHeight + (generatePos * gs.blockSize), currWidth), currItemID, gs.textureNames[gs.itemIDs[currItemID]], gs.blockHardness[currItemID])
                worldGroup.add(b)
    return worldGroup




def generateChunk(generatePos, worldBlocks):
    noise = PerlinNoise(gs.octaves, gs.seed + generatePos)
    xpix, ypix = gs.CHUNK_SIZE[0], 6
    heightNoise = (np.array([noise([2, j/ypix]) for j in range(xpix)]) * 10).astype(int)

    h = int(gs.height/2 / gs.blockSize) - 5

    world =np.empty((gs.noYBlocks, gs.CHUNK_SIZE[0]), dtype='str')
    world[:] = ' '
    random.seed(gs.seed)

    for y in range(gs.noYBlocks):
        for x in range(gs.CHUNK_SIZE[0]):
            dirt = random.randint(2, 5)
            if(y == h + heightNoise[x]):
                world[y][x] = 'G' #Grass
            elif(y > h + heightNoise[x] and y <= h + heightNoise[x] + dirt):
                world[y][x] = 'D' #Dirt
            elif(y > h + heightNoise[x] and y > h + heightNoise[x] + dirt):
                world[y][x] = 'S' #Stone
            else:
                world[y][x] = ' ' #Sky
            if(y == h + heightNoise[x] - 1 and (x > 0 and x < gs.CHUNK_SIZE[0] - 3)):
                if (random.randint(1, 25) == 1):
                    drawTree(world, y, x) #Tree
            

            if(y > h + heightNoise[x] - 1 and y > h + heightNoise[x] + 36):
                if (random.randint(1, 120) == 1):
                    drawOre(world, x, y, "M")
            if(y > h + heightNoise[x] - 1 and y > h + heightNoise[x] + 16):
                if (random.randint(1, 35) == 1):
                    drawOre(world, x, y, "I")
            if(y > h + heightNoise[x] - 1 and y > h + heightNoise[x] + 30):
                if (random.randint(1, 100) == 1):
                    drawOre(world, x, y, "A")
            if(y > h + heightNoise[x] - 1 and y > h + heightNoise[x] + 10):
                if (random.randint(1, 28) == 1):
                    drawOre(world, x, y, "C")
    
    for i in range(gs.CHUNK_SIZE[0]):
        world[gs.noYBlocks - 1][i] = "B"

    worldGroup = getWorldSprites(world, generatePos)

    for b in worldGroup:
        worldBlocks.add(b)
    
    return worldGroup