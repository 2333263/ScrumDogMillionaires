from perlin_noise import PerlinNoise
import numpy as np
from MainGame.Settings import gameSettings as gs
import random
import pygame
from MainGame.Blocks.block import Block
from MainGame.Items import itemHandler as ih

textureNames = ih.fetchTextureNames()
itemIDs = ih.fetchItemIDs()
blockHardness = ih.fetchBlockHardness()
breakTime = ih.fetchBreakTime()

def drawOre(world, x, y, ore):  # draw an ore in the surface
    xChange = yChange =  [-1, 0, 1]
    for xVal in xChange:
        for yVal in yChange:
            if(random.randint(0, 4) == 1):
                if ((y + yVal > 0 and y + yVal < gs.CHUNK_SIZE[1]) and (x + xVal > 1 and x + xVal < gs.CHUNK_SIZE[0] - 1)):
                    world[y + yVal][x + xVal] = ore


def drawCave(world, x, y): # create caves by leaving 'holes' in the surface
    xChange = yChange =  [-4, -3, -2, -1, 0, 1, 2, 3, 4]
    for xVal in xChange:
        for yVal in yChange:
            if(random.randint(0, 3) == 1):
                if ((y + yVal > 0 and y + yVal < gs.CHUNK_SIZE[1]) and (x + xVal > 1 and x + xVal < gs.CHUNK_SIZE[0] - 1)):
                    world[y + yVal][x + xVal] = " "

#Defines a general shape of a tree using a 2D array, where the index is the position in the world 
def drawTree(world, y, x): # create a tree in the world 
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

def getWorldSprites(world, generatePos): #converts array of blocks into a sprite groups of sprites
    worldGroup = pygame.sprite.Group()
    for i in range(gs.CHUNK_SIZE[0]):
        for j in range(gs.CHUNK_SIZE[1]):
            currHeight = i * gs.blockSize
            currWidth = j * gs.blockSize
            if(world[j][i] == ' '):
                continue
             #Create a block using the current number in the level
            currItemID = int(ih.converterIDs[world[j][i]])
            if(itemIDs.__contains__(currItemID)):
                if(currItemID == 5): #Deal with crafting table
                    b = Block(gs.blockSize, (currHeight + (generatePos * gs.blockSize), currWidth), currItemID, textureNames[itemIDs[currItemID]], blockHardness[currItemID], breakTime[currItemID])
                else: #Deal with all other blocks in the world
                    b = Block(gs.blockSize, (currHeight + (generatePos * gs.blockSize), currWidth), currItemID, textureNames[itemIDs[currItemID]], blockHardness[currItemID], breakTime[currItemID])
                worldGroup.add(b)
    return worldGroup

def generateChunk(generatePos, worldBlocks): # create the surface/chunk using a perlin noise object/function
    noise = PerlinNoise(gs.octaves, gs.seed + generatePos) #Create a new noise object
    xpix, ypix = gs.CHUNK_SIZE[0], 6
    heightNoise = (np.array([noise([2, j/ypix]) for j in range(xpix)]) * 10).astype(int)

    h = int(gs.height/2 / gs.blockSize) - 5

    world =np.empty((gs.CHUNK_SIZE[1], gs.CHUNK_SIZE[0]), dtype='str')
    world[:] = ' '
    random.seed(gs.seed) #Set the seed for the random number generator

    for y in range(gs.CHUNK_SIZE[1]):
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
                elif(random.randint(1,80)==1):#if a tree fails to spawn, there is a 1 in 80 chance that a crafting tabel will spawn in its place (1/2000 chance of spawning)
                    world[y][x]='T' #set that block to be a table 
            if(y > h + heightNoise[x] and y > h + heightNoise[x] + 12):
                if(random.randint(1, 150) == 69):
                    drawCave(world, x, y)
            #randomly spawn the different elements within the surface in a range of where they should spawn in
            if(y > h + heightNoise[x] - 1 and y > h + heightNoise[x] + int(gs.CHUNK_SIZE[1]/2)):
                diamondRand = random.randint(1, 120) 
                if (diamondRand == 1):
                    drawOre(world, x, y, "M")
                elif(diamondRand == 69):
                    drawOre(world, x, y, "D")
                
            if(y > h + heightNoise[x] - 1 and y > h + heightNoise[x] + 16):
                ironRand = random.randint(1, 35)
                if (ironRand == 1):
                    drawOre(world, x, y, "I")
                elif(ironRand == 5):
                    drawOre(world, x, y, "D")
            if(y > h + heightNoise[x] - 1 and y > h + heightNoise[x] + 30):
                goldRand = random.randint(1, 100)
                if (goldRand == 1):
                    drawOre(world, x, y, "A")
                elif(goldRand == 69):
                    drawOre(world, x, y, "D")
            if(y > h + heightNoise[x] - 1 and y > h + heightNoise[x] + 10):
                if (random.randint(1, 28) == 1):
                    drawOre(world, x, y, "C")
    
    for i in range(gs.CHUNK_SIZE[0]):
        world[gs.CHUNK_SIZE[1] - 1][i] = "B"

    worldGroup = getWorldSprites(world, generatePos)

    worldBlocks.add(worldGroup)
    
    return worldGroup