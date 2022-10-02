import math
import random

#sets seed taken from user text input or a random number if no seed is given
seed = 1

actionSpace = {
    "MOVEMENT" : [i for i in range(-1, 5, 1)] ,
    "WORLD" : [i for i in range(5, 25, 1)],
    "HOTBAR" : [i for i in range(25, 65, 1)],
    "CRAFTING" : [i for i in range(65, 75, 1)]
}

def setSeed(string):   
    global seed
    if len(string)!=0:
        seed = abs(int(hasher(string)))
    else:
        seed = abs(random.randint(-10000, 10000))
    return seed

def hasher(string):
    hash=""
    for char in string:
        hash+=str(ord(char))
    return hash

octaves = 1


blockSize = 30 #tested values: [12, 16, 20,24, 32]otherwise collision issues (possibly all multiples of 4 work)
playerRange = 7

width = 1280
height = 720

generatedChunks = {}
CHUNK_SIZE = [34, 70]
visibleChunks = [-1, 0, 1]

drawCrafting = False
craftingTablePos = [int(width/2) - 5 * blockSize, int(height/2) + 12 * blockSize]

endGamePlaced = False
drawPortal = True
endGamePos = [-1, -1]


#Moved to GS for global access
def getPos(pos): #Takes in pygame position coordinates returns block coordinates based system ---> returns block_size*floor(pyPos/block_size) tuple transform
    pos = blockSize*math.floor(pos[0]/blockSize),blockSize*math.floor(pos[1]/blockSize)
    return pos

#Moved to GS for global access
def distance(player, python_pos): #Takes in player position and coords and returns distance
    playerPos = getPos(player.getPlayerPos())
    blockPos = getPos(python_pos)
    return math.sqrt(pow((playerPos[0] - blockPos[0]), 2) + (pow((playerPos[1] - blockPos[1]), 2)))