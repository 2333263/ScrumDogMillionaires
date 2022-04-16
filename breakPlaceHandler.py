import gameSettings as gs
import block
import inventoryHandler
import math
from block import Block
import inventoryHandler as inv

def distance(player, python_pos):
    playerPos = getPos(player.getPlayerPos())
    blockPos = getPos(python_pos)
    return math.sqrt(pow((playerPos[0] - blockPos[0]), 2) + (pow((playerPos[1] - blockPos[1]), 2)))

def getPos(pos): #Takes in pygame position coordinates returns block coordinates based system ---> returns block_size*floor(pyPos/block_size) tuple transform
    pos = gs.blockSize*math.floor(pos[0]/gs.blockSize),gs.blockSize*math.floor(pos[1]/gs.blockSize)
    return pos

def blockBreak(python_pos, world_block, player): #Block breaking logic, and inventory handler passover
    if distance(player, python_pos) <= gs.playerRange * gs.blockSize:
        pos = getPos(python_pos)
        for block in world_block:
            if block.blockPosition == pos and block.itemID not in gs.immovableBlocks:
                #Remove block from world
                world_block.remove(block)
                #Add block to inventory
                inv.addBlock(block)


def blockPlace(python_pos, world_block, player): #Block placing logic, and inventory handler requesting
    if distance(player, python_pos) <= gs.playerRange * gs.blockSize:
        pos = getPos(python_pos)
        found = False
        for block in world_block:
            if block.blockPosition == pos:
                if(block.itemID in gs.clickableBlocks):
                    print("Open")
                found = True
        if found == False:
            #Only allow placing if player has more blocks
            if (inv.getSelected().amount >0):
                #Decrease inventory item
                inv.decrease()

                #Add block to world
                if(gs.textureNames.__contains__(gs.itemIDs[inv.selected])):
                    currTexture = gs.textureNames[gs.itemIDs[inv.selected]]
                    tempBlock = Block(gs.blockSize, pos,  inv.selected, currTexture)

                    world_block.append(tempBlock)
        
