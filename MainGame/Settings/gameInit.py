
#THIS FILE IS IN THE PROCESS OF BEING CREATED, might not be this sprint but will fix anything surrounding it.

import math
import random
from turtle import width

def setSeed(string):   
    global seed
    if len(string)!=0:
        seed = int(hasher(string))
    else:
        seed = random.randint(-10000, 10000)
    return seed

def hasher(string):
    hash=""
    for char in string:
        hash+=str(ord(char))
    return hash

generatedChunks = {}


#Width and Height and Blocksize defined in json. Temp logic here.
width = 0
height = 0
blockSize = 0
craftingTablePos = [int(width/2) - 5 * blockSize, int(height/2) + 12 * blockSize]

#Moved to GS for global access
def getPos(pos): #Takes in pygame position coordinates returns block coordinates based system ---> returns block_size*floor(pyPos/block_size) tuple transform
    pos = blockSize*math.floor(pos[0]/blockSize),blockSize*math.floor(pos[1]/blockSize)
    return pos

#Moved to GS for global access
def distance(player, python_pos): #Takes in player position and coords and returns distance
    playerPos = getPos(player.getPlayerPos())
    blockPos = getPos(python_pos)
    return math.sqrt(pow((playerPos[0] - blockPos[0]), 2) + (pow((playerPos[1] - blockPos[1]), 2)))
